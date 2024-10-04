# views.py

import re
from queryish.rest import APIModel
from wagtail.admin.viewsets.chooser import ChooserViewSet


class Pokemon(APIModel):
    class Meta:
        base_url = "https://pokeapi.co/api/v2/pokemon/"
        detail_url = "https://pokeapi.co/api/v2/pokemon/%s/"
        fields = ["id", "name"]
        pagination_style = "offset-limit"
        verbose_name_plural = "pokemon"

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


class PokemonChooserViewSet(ChooserViewSet):
    model = Pokemon

    choose_one_text = "Choose a pokemon"
    choose_another_text = "Choose another pokemon"


pokemon_chooser_viewset = PokemonChooserViewSet("pokemon_chooser")
