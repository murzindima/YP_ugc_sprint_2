#!/usr/bin/env sh

RUN_CMD=${RUN_CMD:='server'}

# wait_for_mongo()
# {
#     echo "Waiting for MongoDB..."
#     while ! nc -z $MONGO_HOST $MONGO_PORT; do
#       sleep 0.1
#     done
#     echo "MongoDB started"
# }

start_server()
{
    # wait_for_mongo
    exec 2>&1
    exec gunicorn -k uvicorn.workers.UvicornWorker src.main:app --bind 0.0.0.0:8000
}

# we temporary need pytest-asyncio==0.23.4a2 because of
# https://github.com/pytest-dev/pytest-asyncio/issues/737
run_tests()
{
  sleep 10
  pip install pytest-asyncio==0.23.4a2 && \
  # python -m tests.functional.utils.wait_for_dependencies && \
  pytest -vvvs tests/
}

help()
{
  echo "Please, use one of the: server, tests"
  echo "Default command is server"
}


case "$RUN_CMD" in
    "server")
        start_server
        ;;
    "tests")
        run_tests
        ;;
    "")
        echo "No command provided"
        help
        exit 1
        ;;
    *)
        echo "Unknown command --> $1"
        help
        exit 1
        ;;
esac
