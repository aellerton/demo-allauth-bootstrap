from django.contrib import admin
#from django.utils.html import format_html_join
#from django.utils.safestring import mark_safe
#from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin
try:
    from django.utils.encoding import force_text
except ImportError:
    from django.utils.encoding import force_unicode as force_text

from .models import DemoUser, UserProfile
from .forms import DemoUserAdminForm


class UserProfileAdmin(admin.ModelAdmin):
    search_fields = ('user', 'dob')
    ordering = ('user',)
    list_select_related = ('user',)


admin.site.register(UserProfile, UserProfileAdmin)


class UserProfileAdminInline(admin.TabularInline):
    model = UserProfile


class DemoUserAdmin(UserAdmin):
    """The project uses a custom User model, so it uses a custom User admin model.

    Some related notes at:
    https://github.com/dabapps/django-email-as-username/blob/master/emailusernames/admin.py

    And:
    .../lib/python2.7/site-packages/django/contrib/auth/admin.py
    """

    inlines = [
        UserProfileAdminInline,
        ]

    #readonly_fields = ('private_uuid', 'public_id')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'display_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        #(_('Ids'), {'fields': ('private_uuid', 'public_id')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    list_display = ('email', 'first_name', 'last_name', 'display_name', 'is_staff')
    search_fields = ('first_name', 'last_name', 'display_name', 'email')
    ordering = ('email',)

    form = DemoUserAdminForm




# *** NOTE ***
# As the site uses email instead of username, I'm changing how a User object
# displays or identifies itself in admin. The default in Django (file is
# lib/python2.7/site-packages/django/contrib/auth/models.py) is
#
#    def __str__(self):
#        return self.get_username()
#
#    def natural_key(self):
#        return (self.get_username(),)
#
# I'm overriding that a cheap way. I'm not sure if I should replace the entire
# User object ... might be better.
#
#User.__unicode__ = lambda(u): u.email
#User.natural_key = lambda(u): (u.email,)

#admin.site.unregister(DjangoDefaultUser)
admin.site.register(DemoUser, DemoUserAdmin)
