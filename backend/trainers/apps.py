from django.apps import AppConfig


class TrainersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'trainers'

    def ready(self):
        import trainers.signals  # noqa: F401 - imported for signal registration
