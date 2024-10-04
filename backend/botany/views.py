import re
from queryish.rest import APIModel
from pygbif import species as species
from wagtail.admin.viewsets.chooser import ChooserViewSet


class PlantSpecies(APIModel):
    class Meta:
        base_url = "https://pokeapi.co/api/v2/pokemon/"
        detail_url = "https://pokeapi.co/api/v2/pokemon/%s/"
        fields = ["id", "name"]
        pagination_style = "offset-limit"
        verbose_name_plural = "plant species"

    @classmethod
    def from_query_data(cls, data):
        return cls(
            id=int(re.match(r'https://pokeapi.co/api/v2/pokemon/(\d+)/', data['url']).group(1)),
            name=data['name'],
        )

    @classmethod
    def from_individual_data(cls, data):
        return cls(
            id=data['id'],
            name=data['name'],
        )

    def __str__(self):
        return self.name


class PlantSpeciesChooserViewSet(ChooserViewSet):
    model = PlantSpecies
    choose_one_text = "Choose a plant"


plant_species_chooser_viewset = PlantSpeciesChooserViewSet("plant_species")
