from gevent import monkey

monkey.patch_all()

from app.main import app
