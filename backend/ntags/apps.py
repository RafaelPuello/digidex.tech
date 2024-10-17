from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class NtagsConfig(AppConfig):
    name = 'ntags'
    verbose_name = _("NFC Tags")
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        from wagtail.models.reference_index import ReferenceIndex
        from .models import NFCTagScan
        ReferenceIndex.register_model(NFCTagScan)  # noqa