from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from .utils import generate_chat


class UserAssistant(models.Model):
    """
    A model to store the user's chat bot assistant.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='assistant'
    )

    def chat(self, question):
        """
        Chat with the user's chat bot assistant.
        """
        return generate_chat(question) if question else _('Missing question parameter.')

    def __str__(self):
        """
        A string representation of the user's chat bot assistant.
        """
        return f"{self.user.username}'s Assistant"

    class Meta:
        verbose_name = _('User Chat Bot')
        verbose_name_plural = _('User Chat Bots')
