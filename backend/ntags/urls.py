from django.urls import path

from .views import link_nfc_tag, register_nfc_tag

app_name = "ntags"
urlpatterns = [
    path('', link_nfc_tag, name='link'),
    path('register/<str:uid>', register_nfc_tag, name='register-nfc-tag'),
]
