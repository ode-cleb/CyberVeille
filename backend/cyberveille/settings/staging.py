from .prod import *
from decouple import config

CORS_ALLOWED_ORIGINS = [
    config("FRONTEND_URL", default="https://staging.cyberveille.fr"),
]