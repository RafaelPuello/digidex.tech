from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class HomeConfig(AppConfig):
    name = 'home'
    verbose_name = _("Home")
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        import home.signals  # noqa: F401
