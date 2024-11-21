#!/usr/bin/env sh

RUN_CMD=${RUN_CMD:='server'}

migrate()
{
    python manage.py makemigrations --noinput
    python manage.py migrate --noinput
}

collect_static()
{
    python manage.py collectstatic --noinput
}

compile_messages()
{
    python manage.py compilemessages -l en -l ru --noinput
}

create_superuser()
{
    echo "Kindly reminder: DJANGO_SUPERUSER_EMAIL, DJANGO_SUPERUSER_USERNAME and DJANGO_SUPERUSER_PASSWORD are must be set"
    python manage.py createsuperuser --noinput || true
}

start_uwsgi()
{
    exec 2>&1
    exec uwsgi --strict --ini uwsgi.ini
}

help()
{
  echo "Please, use one of the: migrate, createsuperuser, server"
  echo "Default command is server"
}


case "$RUN_CMD" in
    "migrate")
        migrate
        ;;
    "createsuperuser")
        create_superuser
        ;;
    "server")
        migrate
        collect_static
        compile_messages
        start_uwsgi
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
