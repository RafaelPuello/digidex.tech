from django.urls import include, path
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.admin import urls as dashboard_urls
from wagtail import urls as wagtail_urls
from search.views import search

from assistants.views import chat
from ntags.views import link

urlpatterns = [
    path("accounts/", include('allauth.urls')),
    # path("_allauth/", include("allauth.headless.urls")),
    path("search/", search, name="search"),
    path("link/", link, name="link"),
    path("assistant/", chat, name="assistant-chat"),
    path("api/", include('api.urls')),
    path('documents/', include(wagtaildocs_urls)),
    path("dashboard/", include(dashboard_urls)),
    path("", include(wagtail_urls)),
]
