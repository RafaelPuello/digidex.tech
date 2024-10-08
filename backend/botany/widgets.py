from .viewsets import UserPlantChooserViewSet, species_chooser_viewset

SpeciesChooserWidget = species_chooser_viewset.widget_class
UserPlantChooserWidget = UserPlantChooserViewSet.widget_class # noqa F405