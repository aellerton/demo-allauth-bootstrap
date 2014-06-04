from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import TemplateView
from django.conf.urls.static import static
from django.conf import settings

import allauthdemo.views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='visitor/landing-index.html'), name='landing_index'),
    url(r'^about$', TemplateView.as_view(template_name='visitor/landing-about.html'), name='landing_about'),
    url(r'^terms/$', TemplateView.as_view(template_name='visitor/terms.html'), name='website_terms'),
    url(r'^contact$', TemplateView.as_view(template_name='visitor/contact.html'), name='website_contact'),

    (r'^accounts/', include('allauth.urls')),
    url(r'^accounts/profile/$', 'allauthdemo.auth.views.account_profile', name='account_profile'),
 
    url(r'^member/$', allauthdemo.views.member_index, name='user_home'),
    url(r'^member/action$', allauthdemo.views.member_action, name='user_action'),

    url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
