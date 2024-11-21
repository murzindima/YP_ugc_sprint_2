FROM python:3.12-slim-bookworm as builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    POETRY_VERSION=1.6.1

ENV PROJECT_ROOT=/api

WORKDIR ${PROJECT_ROOT}

COPY ./pyproject.toml ./poetry.lock ./

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry==${POETRY_VERSION} \
    && poetry install --without dev --no-root && rm -rf ${POETRY_CACHE_DIR}

FROM python:3.12-slim-bookworm as production

ENV DOCKER_GROUP=app \
    DOCKER_USER=app

ENV PROJECT_ROOT=/api
ENV PROJECT_NAME="api"
ENV PYTHONPATH="$PYTHONPATH:$PROJECT_ROOT:$PROJECT_ROOT/$PROJECT_NAME"

ENV VIRTUAL_ENV=${PROJECT_ROOT}/.venv \
    PATH="${PROJECT_ROOT}/.venv/bin:${PATH}"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY src/ ${VIRTUAL_ENV}
COPY tests ${VIRTUAL_ENV}/tests
COPY docker-entrypoint.sh ${VIRTUAL_ENV}/docker-entrypoint.sh

RUN mkdir ${VIRTUAL_ENV}/logs && apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*
RUN addgroup --system ${DOCKER_GROUP} && adduser --system ${DOCKER_USER} \
    && chown -R ${DOCKER_USER}:${DOCKER_GROUP} "${PROJECT_ROOT}"
USER ${DOCKER_USER}

WORKDIR ${VIRTUAL_ENV}

ENTRYPOINT ["./docker-entrypoint.sh"]
