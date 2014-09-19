#!/bin/env
"""Help new users configure the database for use with social networks.
"""
import os
from datetime import datetime

# Fix Python 2.x.
try: input = raw_input
except NameError: pass

import django
from django.conf import settings

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

settings.configure(DEBUG=True, TEMPLATE_DEBUG=True,
    TEMPLATE_DIRS=(os.path.join(BASE_DIR, 'allauthdemo'),)
)

try:
    django.setup()  # for Django >= 1.7
except AttributeError:
    pass  # must be < Django 1.7


from django.template import Template, Context
from django.template.loader import get_template
#from django.conf.settings import configure as django_configure

sql_template = Template("""
UPDATE django_site SET DOMAIN = '127.0.0.1:8000', name = 'allauthdemo' WHERE id=1;

{% if admin %}
DELETE from auth_user;  -- or just the first user?
INSERT INTO auth_user(id, password, last_login, is_superuser, first_name, last_name, email, is_staff, is_active, date_joined)
VALUES (1, '{{admin.password}}', '{{now}}', 1, '{{admin.first_name}}', '{{admin.last_name}}', '{{admin.email}}', 1, 1, '{{now}}');
{% endif %}

{% if facebook or google %}
--
-- Prep for socialapp_sites
--
DELETE FROM socialaccount_socialapp_sites;
{% endif %}

{% if facebook %}
--
-- Facebook
--
DELETE FROM socialaccount_socialapp WHERE provider='facebook';
INSERT INTO socialaccount_socialapp (provider, name, secret, client_id, `key`)
VALUES ("facebook", "Facebook", "{{facebook.secret}}", "{{facebook.client_id}}", '');

INSERT INTO socialaccount_socialapp_sites (socialapp_id, site_id) VALUES (
  (SELECT id FROM socialaccount_socialapp WHERE provider='facebook'),1);
{% endif %}

{% if google %}
--
-- Google
--
DELETE FROM socialaccount_socialapp WHERE provider='google';
INSERT INTO socialaccount_socialapp (provider, name, secret, client_id, `key`)
VALUES ("google", "Google", "{{ google.secret }}", "{{ google.client_id}}", '');

INSERT INTO socialaccount_socialapp_sites (socialapp_id, site_id) VALUES (
  (SELECT id FROM socialaccount_socialapp WHERE provider='google'),1);
{% endif %}
""")

#settings_template = Template(open("allauthdemo/settings.template.py").read())
settings_template = get_template("settings.template.py")

default_superuser_first_name='The'
default_superuser_last_name='Admin'
default_superuser_email='me@admin.test'


def heading(text):
    text = text.strip()
    line = '-' * len(text)
    print("\n%s\n%s\n%s\n" % (line, text, line))


def ask_yes_no(msg):
    msg = "\n" + msg.strip()+'\n\nPlease enter "yes" or "no": '
    confirm = input(msg)
    while True:
        confirm = confirm.strip().lower()
        if confirm not in ('yes', 'y', 'no', 'n'):
            confirm = input('Please enter either "yes" or "no": ')
            continue
        return confirm in ('yes', 'y')


def ask_text(need, default=None):
    need = need.strip()
    if default:
        msg = "\n%s? Default: [%s] > " % (need, default)
    else:
        msg = "\n%s? > " % need

    while True:
        response = input(msg)
        if response:
            return response
        elif default is not None:
            return default
        else:
            pass # raw_input('Please enter a value.')


def ask_superuser():
    from django.contrib.auth.hashers import make_password
    first_name = ask_text("Admin first name", default_superuser_first_name)
    last_name = ask_text("Admin last name", default_superuser_last_name)
    email = ask_text("Admin email", default_superuser_email)
    password = ask_text("Admin password")
    password = make_password(password)

    return dict(first_name=first_name, last_name=last_name, email=email, password=password)


def ask_facebook():
    secret = ask_text("Facebook secret")
    client_id = ask_text("Facebook client id")
    return dict(secret=secret, client_id=client_id)


def ask_google():
    secret = ask_text("Google secret")
    client_id = ask_text("Google client id")
    return dict(secret=secret, client_id=client_id)


if __name__ == "__main__":

    context = Context({
        'now': str(datetime.now())
    })

    heading("Admin User")
    if ask_yes_no("Do you want to set up a superuser?\n\n"
                  "Doing it now means you don't have to re-enter it every time\n"
                  "you rebuild the database in development."):
        context['admin'] = ask_superuser()

    heading("Facebook")
    if ask_yes_no("Do you want to configure auth via Facebook?\n"
                  "You'll need the app secret and client."):
        context['facebook'] = ask_facebook()

    heading("Google")
    if ask_yes_no("Do you want to configure auth via Google?\n"
                  "You'll need the app secret and client."):
        context['google'] = ask_google()

    with open('seed.sql', 'w') as out:
        out.write(sql_template.render(context))

    with open('allauthdemo/settings_generated.py', 'w') as out:
        out.write(settings_template.render(context))

    print("\nAll done!\n")
    print("Have a look in seed.sql\n\n")
    print("Next:\n  make rebuild\n  make run  (or ``python manage.py runserver``)")

