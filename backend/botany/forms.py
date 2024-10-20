from django import forms
from django.db import transaction
from wagtail.admin.forms import WagtailAdminModelForm

class UserPlantForm(WagtailAdminModelForm):
    # Adding a non-model field to the form, defaulting to hidden
    copies = forms.IntegerField(
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

    def clean(self):
        cleaned_data = super().clean()
        
        # Ensure 'name' is not too short
        name = cleaned_data.get('name')
        if name and len(name) < 3:
            self.add_error('name', 'Name must be at least 3 characters long.')
        
        return cleaned_data

    @transaction.atomic
    def save(self, commit=True):
        """
        Override the save method to handle custom logic.
        In this case, we save the initial instance and create copies if 'copies' > 0.
        """
        instance = super().save(commit=False)

        if commit:
            # Get the number of copies from cleaned_data
            copies = self.cleaned_data.get('copies', 0)

            if copies > 1:
                instance.name = f"{instance.name} - 1"
                instance.slug = f"{instance.slug}-1"
                instance.save()
                self.create_plant_copies(instance, copies)
        
            instance.save()
        return instance

    class Meta:
        fields = ['box', 'name', 'description', 'copies', 'notes']

    @transaction.atomic
    def create_plant_copies(self, plant, copies):
        from .models import UserPlant

        for copy in range(2, copies+1):
            plant_copy = UserPlant(
                box=plant.box,
                name=f"{plant.name} - {copy}",
                slug=f"{plant.slug}-{copy}",
                description=plant.description,
                notes=plant.notes,
            )
            plant_copy.save()
