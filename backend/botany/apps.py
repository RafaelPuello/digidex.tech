from django.apps import AppConfig
from django.db.models import ForeignKey


class BotanyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'botany'
    label = 'botany'

    def ready(self):
        from wagtail.admin.forms.models import register_form_field_override
        from .models import Plant
        from .widgets import PlantChooserWidget
        register_form_field_override(ForeignKey, to=Plant, override={'widget': PlantChooserWidget})
