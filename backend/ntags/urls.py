from django.urls import path

from .views import link_nfc_tag, get_linkable_objects

app_name = "ntags"
urlpatterns = [
    path('', link_nfc_tag, name='link'),
    path('objects/<int:objects_id>/', get_linkable_objects, name='get-linkable-objects'),
]
