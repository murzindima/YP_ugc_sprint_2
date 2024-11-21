#!/usr/bin/env sh

RUN_CMD=${RUN_CMD:='server'}

start_server()
{
    exec 2>&1
    exec gunicorn -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000
}

run_tests()
{
  pip install pytest pytest-asyncio && \
  python -m tests.functional.utils.wait_for_dependencies && \
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
