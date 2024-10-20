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
        label="Copies",
        help_text="Number of copies to create.",
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
        if not re.match(r'^[\w\s\-]+$', name):
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
            copies = self.cleaned_data.get('copies', 0)

            if copies > 0:
                instance.create_plant_copies(instance, copies)

        return instance

    class Meta:
        fields = ['box', 'name', 'description', 'copies', 'notes']
