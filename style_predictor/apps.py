from django.apps import AppConfig


class StylePredictorConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "style_predictor"

    def ready(self):
        import django.contrib.postgres.signals  # noqa: F401
