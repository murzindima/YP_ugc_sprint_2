import logging

import sentry_sdk
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
from starlette import status
from starlette.requests import Request

from src.api.v1 import bookmarks, reviews, likes
from src.core.config import app_settings, jaeger_settings, sentry_settings
from src.core.logger import LOGGING
from src.exceptions.handlers import authjwt_exception_handler, validation_error_handler
from src.middleware.jwt import set_current_user


def configure_tracer() -> None:
    resource = Resource(attributes={SERVICE_NAME: "ugc-operations-service"})
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


if jaeger_settings.enable_tracer:
    configure_tracer()


@AuthJWT.load_config
def get_config():
    return app_settings


if sentry_settings.enable_sdk:
    sentry_sdk.init(
        dsn=sentry_settings.dsn,
        traces_sample_rate=sentry_settings.traces_sample_rate,
        profiles_sample_rate=sentry_settings.profiles_sample_rate,
        enable_tracing=sentry_settings.enable_tracing,
    )


app = FastAPI(
    title=app_settings.project_name,
    description="A service that provides methods for generating content by users.",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)

FastAPIInstrumentor.instrument_app(app)


if jaeger_settings.enable_tracer:

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


app.include_router(
    bookmarks.router,
    prefix="/api/v1/bookmarks",
    tags=["bookmarks"],
    dependencies=[Depends(set_current_user)],
)
app.include_router(
    likes.router,
    prefix="/api/v1/likes",
    tags=["likes"],
    dependencies=[Depends(set_current_user)],
)
app.include_router(
    reviews.router,
    prefix="/api/v1/reviews",
    tags=["reviews"],
    dependencies=[Depends(set_current_user)],
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
