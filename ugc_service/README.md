# Sprint 8

## Repository Link

https://github.com/murzindima/ugc_sprint_1

## Running via gunicorn server with gevent
```bash
gunicorn -k gevent -w 4 -b 0.0.0.0:5000 app.wsgi_app:app
```
