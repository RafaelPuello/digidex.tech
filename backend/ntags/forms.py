from django import forms
from wagtail.admin.forms import WagtailAdminModelForm
from django.contrib.contenttypes.models import ContentType


class NFCTagRegistrationForm(forms.Form):
    confirmation = forms.BooleanField(
        required=True
    )


class NFCTagForm(WagtailAdminModelForm):
    item = forms.ModelChoiceField(
        queryset=None,
        required=False,
        label="Plant",
        widget=forms.Select()
    )
    content_type = forms.ModelChoiceField(
        queryset=ContentType.objects.all(),
        required=False,
        label="",
        widget=forms.HiddenInput()
    )
    object_id = forms.IntegerField(
        required=False,
        widget=forms.HiddenInput()
    )

    class Meta:
        fields = ['content_type', 'item', 'active']

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')

        super().__init__(*args, **kwargs)

        self.populate_item_field(self.for_user, instance)

    def populate_item_field(self, user, instance):
        from botany.models import UserPlant

        self.fields['item'].queryset = UserPlant.objects.without_nfc_tag(user)

        if instance.content_object:
            self.fields['item'].initial = instance.object_id
        return

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.cleaned_data['item']:
            instance.content_object = self.cleaned_data['item']
        if commit:
            instance.save()
        return instance
