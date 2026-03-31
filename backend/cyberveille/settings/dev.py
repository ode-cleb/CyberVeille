from .base import *
from decouple import config

DEBUG = True

INSTALLED_APPS += [
    "debug_toolbar",
    "silk",
]

MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE
MIDDLEWARE += ["silk.middleware.SilkyMiddleware"]

INTERNAL_IPS = ["127.0.0.1"]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG",
    },
}