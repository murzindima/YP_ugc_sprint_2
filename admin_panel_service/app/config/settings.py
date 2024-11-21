import os
from pathlib import Path
from split_settings.tools import include
from dotenv import load_dotenv

load_dotenv()

include(
    "components/database.py",
    "components/debug.py",
    "components/i18n.py",
    "components/password-validation.py",
    "components/middleware.py",
    "components/templates.py",
    "components/applications.py",
)

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = (os.environ.get("SECRET_KEY"),)
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")
CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS", "").split(",")
LOCALE_PATHS = ["movies/locale"]
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "movies.User"
AUTHENTICATION_BACKENDS = ["movies.auth.CustomBackend"]
AUTH_API_LOGIN_URL = os.environ.get("AUTH_API_LOGIN_URL")
AUTH_API_USERS_URL = os.environ.get("AUTH_API_USERS_URL")
AUTH_API_ROLES_URL = os.environ.get("AUTH_API_ROLES_URL")
