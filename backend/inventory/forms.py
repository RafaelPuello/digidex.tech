from django import forms
from django.contrib.contenttypes.models import ContentType

from . import get_inventory_model_classes


class InventoryFormMixin(forms.Form):
    include_all = forms.BooleanField(
        required=False,
        label="Include All",
        widget=forms.CheckboxInput()
    )
    content_type = forms.ModelChoiceField(
        choices=get_inventory_model_classes(),
        required=False,
        label="Linked Object",
        widget=forms.Select()
    )
    object_id = forms.IntegerField(
        required=False,
        widget=forms.HiddenInput()
    )
    item = forms.ModelChoiceField(
        queryset=None,
        required=False,
        label="Linked Object",
        widget=forms.Select()
    )

    class Meta:
        fields = ['include_all', 'content_type', 'object_id', 'item']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        content_type_id = self.get_content_type_id()
        object_id = self.get_object_id()

        self.populate_item_queryset(content_type_id, object_id)

    def get_content_type_id(self):
        """
        Determine content_type_id from form data or instance.
        """
        if 'content_type' in self.data:
            return self.data.get('content_type')
        elif self.instance.pk and self.instance.content_type:
            return self.instance.content_type.id
        return None

    def get_object_id(self):
        """
        Determine object_id from form data or instance.
        """
        if 'object_id' in self.data:
            return self.data.get('object_id')
        elif self.instance.pk and self.instance.object_id:
            return self.instance.object_id
        return None

    def populate_item_queryset(self, content_type_id, object_id):
        """
        Populate the 'item' field queryset and set initial value if applicable.
        """
        if content_type_id:
            try:
                content_type = ContentType.objects.get(id=content_type_id)
                model_class = content_type.model_class()
                self.fields['item'].queryset = model_class.objects.all()

                if object_id:
                    self.set_item_initial_value(model_class, object_id)
            except ContentType.DoesNotExist:
                self.fields['item'].queryset = ContentType.objects.none()
        else:
            self.fields['item'].queryset = ContentType.objects.none()

    def set_item_initial_value(self, model_class, object_id):
        """
        Set the initial value of 'item' based on object_id.
        """
        try:
            self.fields['item'].initial = model_class.objects.get(id=object_id)
        except model_class.DoesNotExist:
            pass  # Handle the case where the object_id does not exist in the model class

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Ensure object_id is saved as the ID (primary key)
        if self.cleaned_data['item']:
            instance.object_id = self.cleaned_data['item'].id
        if commit:
            instance.save()
        return instance
