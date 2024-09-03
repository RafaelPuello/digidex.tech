from django.urls import include, path

from wagtail.admin import urls as dashboard_urls
from wagtail import urls as wagtail_urls

from search.views import search
from nearfieldcommunication.views import link

urlpatterns = [
    path("accounts/", include('allauth.urls')),
    path("_allauth/", include("allauth.headless.urls")),
    path("search/", search, name="search"),
    path("link/", link, name="link"),
    path("assistant/", include('assistant.urls')),
    path("dashboard/", include(dashboard_urls)),
    path("api/", include('api.urls')),
    path("", include(wagtail_urls)),
]
