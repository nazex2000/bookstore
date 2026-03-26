from django.apps import AppConfig


class BookapiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bookAPI'

    def ready(self):
        import bookAPI.signals  # noqa: F401
