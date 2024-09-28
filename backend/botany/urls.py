from django.urls import path, include

from .api import router

urlpatterns = [
    path('v1/', include(router.urls)),
]
