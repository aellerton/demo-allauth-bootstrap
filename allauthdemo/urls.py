"""URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
  1. Add an import:  from my_app import views
  2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
  1. Add an import:  from other_app.views import Home
  2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
  1. Import the include() function: from django.conf.urls import url, include
  2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

from .auth.views import account_profile
from .views import member_index, member_action

urlpatterns = [
    # Landing page area
    url(r'^$', TemplateView.as_view(template_name='visitor/landing-index.html'), name='landing_index'),
    url(r'^about$', TemplateView.as_view(template_name='visitor/landing-about.html'), name='landing_about'),
    url(r'^terms/$', TemplateView.as_view(template_name='visitor/terms.html'), name='website_terms'),
    url(r'^contact$', TemplateView.as_view(template_name='visitor/contact.html'), name='website_contact'),

    # Account management is done by allauth
    url(r'^accounts/', include('allauth.urls')),

    # Account profile and member info done locally
    url(r'^accounts/profile/$', account_profile, name='account_profile'),
    url(r'^member/$', member_index, name='user_home'),
    url(r'^member/action$', member_action, name='user_action'),

    # Usual Django admin
    url(r'^admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
