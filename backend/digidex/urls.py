from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.admin import urls as dashboard_urls
from wagtail import urls as wagtail_urls
from search.views import search
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .api import api_router


urlpatterns = [
    path("accounts/", include('allauth.urls')),
    # path("_allauth/", include("allauth.headless.urls")),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("search/", search, name="search"),
    path("link/", include('ntags.urls')),
    path('documents/', include(wagtaildocs_urls)),
    path('botany/', include('botany.urls')),
    path('admin/', admin.site.urls),
    path("dashboard/", include(dashboard_urls)),
    path('api/v2/', api_router.urls),
    path("", include(wagtail_urls)),
]

# Serve static and media files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
