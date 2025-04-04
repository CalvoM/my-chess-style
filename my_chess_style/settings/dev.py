from .base import *  # noqa: F403

DEBUG = True
ALLOWED_HOSTS = ["*"]
SECRET_KEY = os.getenv(  # noqa: F405
    "SECRET_KEY", "django-insecure-ed$#fl!ut48ip8(k2+2ipws*c0*=217xti!*r09emyy#22cv-d"
)
