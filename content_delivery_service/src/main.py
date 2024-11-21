import logging
from contextlib import asynccontextmanager

import uvicorn
from elasticsearch import AsyncElasticsearch, BadRequestError
from fastapi import FastAPI, Request, status, Depends
from fastapi.responses import ORJSONResponse
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from pydantic import ValidationError
from redis.asyncio import Redis

from api.v1 import films, genres, persons
from core.config import (
    app_settings,
    elasticsearch_settings,
    jaeger_settings,
    redis_settings,
)
from core.logger import LOGGING
from db import elastic, redis
from middleware.external_auth import security_jwt


def configure_tracer() -> None:
    resource = Resource(attributes={SERVICE_NAME: "content-delivery-service"})
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
    redis.redis = Redis(**dict(redis_settings))
    elastic.es = AsyncElasticsearch(hosts=[dict(elasticsearch_settings)])
    yield
    await redis.redis.close()
    await elastic.es.close()


app = FastAPI(
    title=app_settings.project_name,
    description="A cinema API containing information about movies, genres, and persons.",
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


app.include_router(
    films.router,
    prefix="/api/v1/films",
    tags=["films"],
    dependencies=[Depends(security_jwt)],
)
app.include_router(
    genres.router,
    prefix="/api/v1/genres",
    tags=["genres"],
    dependencies=[Depends(security_jwt)],
)
app.include_router(
    persons.router,
    prefix="/api/v1/persons",
    tags=["persons"],
    dependencies=[Depends(security_jwt)],
)


@app.exception_handler(ValidationError)
async def handler_validation_error(request: Request, exc: ValidationError):
    return ORJSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content={"errors": exc.errors()}
    )


@app.exception_handler(BadRequestError)
async def handler_bad_request_error(request: Request, exc: BadRequestError):
    return ORJSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content={"errors": "Bad Request"}
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
