from django.apps import AppConfig
from django.db.models import ForeignKey


class BotanyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'botany'
    label = 'botany'

    def ready(self):
        from wagtail.admin.forms.models import register_form_field_override
        from .models import UserPlant
        from .widgets import UserPlantChooserWidget
        register_form_field_override(ForeignKey, to=UserPlant, override={'widget': UserPlantChooserWidget})
