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
            # ('higherTaxonKey', 6)  # 6 is the key for the Plantae kingdom
            ('higherTaxonKey', 2519)   # 2519 is the key for the Cactaceae family
        ])


class PlantSpecies(APIModel):

    base_query_class = PlantSpeciesQuerySet

    class Meta:
        base_url = "https://api.gbif.org/v1/species/search/"
        detail_url = "https://api.gbif.org/v1/species/%s"
        fields = ["id", "scientific_name", "canonical_name"]
        verbose_name = "Plant Species"
        verbose_name_plural = "Plant Species"

    @classmethod
    def from_query_data(cls, data):
        """
        Given a record returned from the listing endpoint (base_url), return an instance of the model.
        """
        return cls(
            id=data.get('key'),
            canonical_name=data.get('canonicalName'),
            scientific_name=data.get('scientificName')
        )

    @classmethod
    def from_individual_data(cls, data):
        """
        Given a record returned from the detail endpoint (detail_url), return an instance of the model.
        """
        return cls(
            id=data.get('key'),
            canonical_name=data.get('canonicalName'),
            scientific_name=data.get('scientificName')
        )

    def __str__(self):
        if self.canonical_name and self.scientific_name:
            return f"{self.canonical_name} ({self.scientific_name})"
        return self.canonical_name or self.scientific_name


class PlantSpeciesChooserViewSet(ChooserViewSet):
    model = PlantSpecies
    choose_one_text = "Choose a plant species"
    choose_another_text = "Choose another plant species"
    is_searchable = True


plant_species_chooser_viewset = PlantSpeciesChooserViewSet("plant_species_chooser")  # noqa