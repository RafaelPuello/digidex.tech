from .views import species_chooser_viewset
from .viewsets import UserPlantViewSet

PlantChooserWidget = UserPlantViewSet.chooser_viewset_class.widget_class # noqa F405
SpeciesChooserWidget = species_chooser_viewset.widget_class # noqa F405