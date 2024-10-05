from django import forms
from wagtail.admin.forms import WagtailAdminModelForm
from django.contrib.contenttypes.models import ContentType

from .models import NFCTag

class NFCTagAdminForm(WagtailAdminModelForm):
    item = forms.ModelChoiceField(
        queryset=None,
        required=False,
        label="Linked Object",
        widget=forms.Select()
    )
    object_id = forms.IntegerField(
        required=False,
        widget=forms.HiddenInput()
    )

    class Meta:
        model = NFCTag
        fields = ['label', 'content_type', 'item']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['content_type'].label = 'Linked Object Type'

        # Determine the content_type and object_id
        if 'content_type' in self.data:
            content_type_id = self.data.get('content_type')
        elif self.instance.pk and self.instance.content_type:
            content_type_id = self.instance.content_type.id
        else:
            content_type_id = None

        # Fetch object_id from form data or instance if available
        if 'object_id' in self.data:
            object_id = self.data.get('object_id')
        elif self.instance.pk and self.instance.object_id:
            object_id = self.instance.object_id
        else:
            object_id = None

        # If content_type is set, populate the item queryset
        if content_type_id:
            content_type = ContentType.objects.get(id=content_type_id)
            model_class = content_type.model_class()
            self.fields['item'].queryset = model_class.objects.all()

            # If both content_type and object_id are set, set the initial value for item
            if object_id:
                try:
                    self.fields['item'].initial = model_class.objects.get(id=object_id)
                except model_class.DoesNotExist:
                    pass  # Handle the case where the object_id does not exist in the model class
        else:
            # If content_type is not set, leave the item field empty
            self.fields['item'].queryset = NFCTag.objects.none()

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Ensure object_id is saved as the ID (primary key)
        if self.cleaned_data['item']:
            instance.object_id = self.cleaned_data['item'].id
        if commit:
            instance.save()
        return instance
