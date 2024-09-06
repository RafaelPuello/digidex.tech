from django.urls import include, path
from rest_framework import routers

from .views import chat
from .viewsets import UserAssistantDetail

app_name = "assistant"

router = routers.DefaultRouter()
router.register(r'assistant', UserAssistantDetail)

urlpatterns = [
    path("chat/", chat, name="assistant-chat"),
    path('api/', include(router.urls)),
]
