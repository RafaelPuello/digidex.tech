from django.http import HttpResponseRedirect
from django.contrib import messages
from wagtail import hooks
from wagtail.snippets.models import register_snippet

from .views import plant_species_chooser_viewset
from .viewsets import UserPlantViewSet


@hooks.register('after_create_snippet')
def create_multiple_copies(request, instance):
    """
    Creates multiple copies of a snippet after the original snippet is created.
    The number of copies is determined by the user via a form field in the creation form.
    """
    # Check if 'num_copies' is in the request POST data (assuming it's sent from the form)
    num_copies = int(request.POST.get('num_copies', 1))

    if num_copies > 1:
        # Create the specified number of copies
        for i in range(num_copies - 1):  # Minus 1, as the original has already been created
            copy_instance = instance.__class__.objects.get(pk=instance.pk)
            copy_instance.pk = None  # Reset the primary key to create a new instance
            copy_instance.save()

        # Provide feedback to the user
        messages.success(
            request, f"{num_copies} copies of the snippet were created."
        )

    # Redirect to the listing view or the snippet instance's page
    return HttpResponseRedirect(request.get_full_path())


@hooks.register("register_admin_viewset")
def register_plant_species_chooser_viewset():
    return plant_species_chooser_viewset


@hooks.register("register_icons")
def register_icons(icons):
    return icons + ['botany/icons/plant.svg']


register_snippet(UserPlantViewSet)  # noqa