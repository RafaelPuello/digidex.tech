from django.urls import path, include

from .species.urls import urlpatterns as species_urls

app_name = 'botany'
urlpatterns = [
    path('species/', include(species_urls)),
]
