from django import forms
from django.core.validators import MinLengthValidator

from .models import DemoUser


class DemoUserEditForm(forms.ModelForm):
    """Form for viewing and editing name fields in a DemoUser object.

    A good reference for Django forms is:
    http://pydanny.com/core-concepts-django-modelforms.html
    """

    def __init__(self, *args, **kwargs):
        # TODO: this doesn't seem to work. Need to get to the bottom of it.
        #self.base_fields["display_name"].min_length = 2
        #self.base_fields["display_name"].validators.append(MinLengthValidator)
        #print self.base_fields['display_name'].validators
        super(forms.ModelForm, self).__init__(*args, **kwargs)

    class Meta:
        model = DemoUser
        fields = ('first_name', 'last_name', 'display_name')


class DemoUserAdminForm(forms.ModelForm):

    class Meta:
        model = DemoUser
        fields = ('email', 'first_name', 'last_name', 'display_name', 'is_staff', 'is_active', 'date_joined')

    def is_valid(self):
        #log.info(force_text(self.errors))
        return super(DemoUserAdminForm, self).is_valid()
