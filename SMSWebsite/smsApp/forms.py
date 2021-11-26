from django import forms
from .models import SMS, Recipient, RecipientGroup


class ContactForm(forms.ModelForm):
    CHOICES = (
        ("csv", "CSV File"),
        ("contact", "Single Contact"),
    )

    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    phone_number = forms.CharField(max_length=13, min_length=10, required=False)
    entry_type = forms.ChoiceField(choices=CHOICES, required=False)

    class Meta:
        model = Recipient
        fields = ['entry_type', 'first_name', 'last_name', 'phone_number', 'group_name']


class SMSForm(forms.ModelForm):
    phone_number = forms.ModelChoiceField(queryset=None)
    group_name = forms.ModelChoiceField(queryset=RecipientGroup.objects.all())

    class Meta:
        model = SMS
        fields = ['group_name', 'phone_number', 'message']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone_number'].queryset = Recipient.objects.none()

        if 'group_name' in self.data:
            try:
                group_id = int(self.data.get('group_name'))
                self.fields['phone_number'].queryset = Recipient.objects.filter(group_name_id=group_id).order_by(
                    'phone_number')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['phone_number'].queryset = self.instance.group_name.phone_number_set.order_by('phone_number')
