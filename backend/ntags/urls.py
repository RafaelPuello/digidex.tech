from django.urls import path

from . import views

app_name = "ntags"
urlpatterns = [
    path("", views.link, name="link"),
]
