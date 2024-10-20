import re
from django import forms
from django.db import transaction
from django.core.exceptions import ValidationError
from wagtail.admin.forms import WagtailAdminModelForm


class UserPlantForm(WagtailAdminModelForm):
    # Adding a non-model field to the form, defaulting to hidden
    copies = forms.IntegerField(
        max_value=30,
        min_value=0,
        initial=0,
        required=False,
        label="Number of Plants",
        widget=forms.HiddenInput()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Check if the instance is being created or edited
        if self.instance.pk is None:
            # If creating, set the widget to visible
            self.fields['copies'].widget = forms.NumberInput()

    def clean_name(self):
        """
        Cleans the 'name' field to ensure it only contains alphanumeric characters and '-'.
        """
        name = self.cleaned_data.get('name', '').strip()

        # Ensure 'name' is not too short
        if len(name) < 3:
            self.add_error('name', 'Name must be at least 3 characters long.')

        # Use regex to match only allowed characters (alphanumeric and dash)
        if not re.match(r'^[\w\-]+$', name):
            raise ValidationError('Name must contain only letters, numbers, and hyphens.')

        return name

    @transaction.atomic
    def save(self, commit=True):
        """
        Override the save method to handle custom logic.
        In this case, we save the initial instance and create copies if 'copies' > 0.
        """
        instance = super().save(commit=False)

        if commit:
            instance.save()

            # Get the number of copies from cleaned_data
            copies = self.cleaned_data.get('copies', 0)

            if copies > 0:
                # Create copies starting from '-1' up to '-(copies)'
                self.create_plant_copies(instance, copies)
            else:
                instance.save()

        return instance

    class Meta:
        fields = ['box', 'name', 'description', 'copies', 'notes']

    @transaction.atomic
    def create_plant_copies(self, plant, copies):
        from .models import UserPlant

        # Start copy number from 1 and end at copies + 1
        for copy in range(1, copies + 1):
            plant_copy = UserPlant(
                box=plant.box,
                name=f"{plant.name} - {copy}",
                description=plant.description,
                notes=plant.notes,
            )
            plant_copy.save()
