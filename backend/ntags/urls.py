from django.urls import path

from .views import link

app_name = "ntags"
urlpatterns = [
    path("", link, name="link"),
]
