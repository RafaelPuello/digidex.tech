from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from .utils import generate_chat


class UserAssistant(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='assistant'
    )

    def chat(self, question):
        if not question:
            return _('Missing question parameter.')
        return generate_chat(question)

    def __str__(self):
        return f"{self.user.username}'s Assistant"

    class Meta:
        verbose_name = _('User Chat Bot')
        verbose_name_plural = _('User Chat Bots')
