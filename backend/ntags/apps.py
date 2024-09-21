from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class NtagsConfig(AppConfig):
    name = 'ntags'
    verbose_name = _("Taggit")
    default_auto_field = 'django.db.models.BigAutoField'
