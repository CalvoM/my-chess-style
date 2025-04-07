import os

from celery import Celery

_ = os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    os.getenv("DJANGO_SETTINGS_MODULE", "my_chess_style.settings.dev"),
)
app = Celery("my_chess_style")
_ = app.config_from_object("django.conf:settings", namespace="CELERY")
_ = app.autodiscover_tasks()
