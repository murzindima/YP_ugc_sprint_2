FROM python:3.11

WORKDIR /app

COPY requirements.txt requirements.txt

ENV POETRY_VERSION=1.6.1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

#RUN pip install --no-cache-dir poetry==${POETRY_VERSION} \
#    && poetry install --without dev --no-root && rm -rf ${POETRY_CACHE_DIR}

RUN  pip install --upgrade pip \
     && pip install -r requirements.txt

COPY . .

ENTRYPOINT ["bash", "start_service.sh"]
