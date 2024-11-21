import logging
from contextlib import asynccontextmanager

import uvicorn
from async_fastapi_jwt_auth import AuthJWT
from async_fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi import Depends, FastAPI
from fastapi.responses import ORJSONResponse
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from pydantic import ValidationError
from redis.asyncio import Redis
from starlette import status
from starlette.requests import Request

from src.api.v1 import auth, permissions, roles, users
from src.core.config import app_settings, redis_settings, jaeger_settings
from src.core.logger import LOGGING
from src.db import redis
from src.exceptions.handlers import authjwt_exception_handler, validation_error_handler
from src.middleware.access_jwt import get_current_user, set_current_user


def configure_tracer() -> None:
    resource = Resource(attributes={SERVICE_NAME: "auth-service"})
    trace.set_tracer_provider(TracerProvider(resource=resource))
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(
            JaegerExporter(
                agent_host_name=jaeger_settings.host,
                agent_port=jaeger_settings.port,
            )
        )
    )
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(ConsoleSpanExporter())
    )


if app_settings.enable_tracer:
    configure_tracer()


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis.redis = Redis(**dict(redis_settings), decode_responses=True)
    yield
    await redis.redis.close()


@AuthJWT.load_config
def get_config():
    return app_settings


@AuthJWT.token_in_denylist_loader
async def check_if_token_in_denylist(decrypted_token):
    jti = decrypted_token["jti"]
    entry = await redis.redis.get(jti)
    return entry and entry == "true"


app = FastAPI(
    title=app_settings.project_name,
    description="A service providing authentication methods.",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

FastAPIInstrumentor.instrument_app(app)


if app_settings.enable_tracer:

    @app.middleware("http")
    async def before_request(request: Request, call_next):
        response = await call_next(request)
        request_id = request.headers.get("X-Request-Id")
        if not request_id:
            return ORJSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": "X-Request-Id is required"},
            )
        return response


app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(
    users.router,
    prefix="/api/v1/users",
    tags=["users"],
    dependencies=[Depends(set_current_user), Depends(get_current_user)],
)
app.include_router(
    permissions.router,
    prefix="/api/v1/permissions",
    tags=["permissions"],
    dependencies=[Depends(set_current_user), Depends(get_current_user)],
)
app.include_router(
    roles.router,
    prefix="/api/v1/roles",
    tags=["roles"],
    dependencies=[Depends(set_current_user), Depends(get_current_user)],
)

app.exception_handler(AuthJWTException)(authjwt_exception_handler)
app.exception_handler(ValidationError)(validation_error_handler)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
