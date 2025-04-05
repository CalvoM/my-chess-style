from .base import *  # noqa: F403

DEBUG = False
# TODO: Update when in production
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
SECRET_KEY = os.getenv(  # noqa: F405
    "SECRET_KEY", "40IlPJdzR2AKYhjQ8RzxoEh82gfhmTuoFEPu90MVXSqZ2XqIZvF2E00H8VYl6NsuWaw"
)
