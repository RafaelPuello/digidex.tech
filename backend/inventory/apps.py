from django.apps import AppConfig
from django.db.models import ForeignKey


class InventoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inventory'

    def ready(self):
        from wagtail.admin.forms.models import register_form_field_override
        from .models import InventoryBox
        from .widgets import BoxChooserWidget
        register_form_field_override(ForeignKey, to=InventoryBox, override={'widget': BoxChooserWidget})
