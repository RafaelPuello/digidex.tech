from queryish.rest import APIModel, APIQuerySet
from wagtail.admin.viewsets.chooser import ChooserViewSet


class PlantSpeciesQuerySet(APIQuerySet):
    """
    Custom QuerySet to include 'kingdomKey' as a default filter for the plant kingdom.
    """

    base_url = "https://api.gbif.org/v1/species/search/"
    pagination_style = "offset-limit"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters.extend([
            ('rank', 'SPECIES'),
            ('status', 'ACCEPTED'),
            ('higherTaxonKey', 6)
        ])


class PlantSpecies(APIModel):

    base_query_class = PlantSpeciesQuerySet

    class Meta:
        detail_url = "https://api.gbif.org/v1/species/search/%s"
        fields = ["key", "scientificName", "canonicalName", "rank", "taxonomicStatus"]
        verbose_name = "Plant Species"
        verbose_name_plural = "Plant Species"

    @classmethod
    def from_query_data(cls, data):
        return cls(
            key=data.get('key'),
            canonicalName=data.get('canonicalName'),
            scientificName=data.get('scientificName')
        )

    @classmethod
    def from_individual_data(cls, data):
        return cls(
            key=data.get('key'),
            canonicalName=data.get('canonicalName'),
            scientificName=data.get('scientificName')
        )

    def __str__(self):
        if self.canonicalName and self.scientificName:
            return f"{self.canonicalName} ({self.scientificName})"
        return self.canonicalName or self.scientificName


class PlantSpeciesChooserViewSet(ChooserViewSet):
    model = PlantSpecies
    choose_one_text = "Choose a species"
    choose_another_text = "Choose another species"
    is_searchable = True


plant_species_chooser_viewset = PlantSpeciesChooserViewSet("plant_species_chooser")  # noqa