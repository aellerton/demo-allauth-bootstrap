from django import forms

from .models import User


class UserEditForm(forms.ModelForm):
    """Form for viewing and editing name fields in a User object.

    A good reference for Django forms is:
    http://pydanny.com/core-concepts-django-modelforms.html
    """

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        # Do stuff with form instance here

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'display_name')


class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'display_name', 'is_staff', 'is_active', 'date_joined')

    def is_valid(self):
        return super().is_valid()
