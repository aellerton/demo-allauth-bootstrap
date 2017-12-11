from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic.edit import FormMixin, UpdateView

from .forms import UserEditForm


class MyModelInstanceMixin(FormMixin):
    def get_model_instance(self):
        return None

    def get_form_kwargs(self):
        kwargs = super(MyModelInstanceMixin, self).get_form_kwargs()
        instance = self.get_model_instance()
        if instance:
            kwargs.update({'instance': instance})
        return instance


class UserEditView(UpdateView):
    """Allow view and update of basic user data.

    In practice this view edits a model, and that model is
    the User object itself, specifically the names that
    a user has.

    The key to updating an existing model, as compared to creating
    a model (i.e. adding a new row to a database) by using the
    Django generic view ``UpdateView``, specifically the
    ``get_object`` method.
    """
    form_class = UserEditForm
    template_name = "auth/profile.html"
    view_name = 'account_profile'
    success_url = reverse_lazy(view_name)

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        form.save()
        messages.add_message(self.request, messages.INFO, 'User profile updated')
        return super(UserEditView, self).form_valid(form)


account_profile = login_required(UserEditView.as_view())
