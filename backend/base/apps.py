from django.apps import AppConfig
from wagtail.images.apps import WagtailImagesAppConfig
from django.db.models import ForeignKey


class BaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base'

    # def ready(self):
        # from wagtail.admin.forms.models import register_form_field_override
        # from .models import InventoryBoxPage
        # from .widgets import BoxChooserWidget
        # register_form_field_override(ForeignKey, to=InventoryBoxPage, override={'widget': BoxChooserWidget})


class BaseImagesAppConfig(WagtailImagesAppConfig):
    default_attrs = {"decoding": "async", "loading": "lazy"}
