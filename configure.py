#!/bin/env
"""Help new users configure the database for use with social networks.
"""
import os
from datetime import datetime

# Fix Python 2.x.
try:
    input = raw_input
except NameError:
    pass

import django
from django.conf import settings
from django.core.management.utils import get_random_secret_key

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# TEMPLATES structure changed in Django 1.10
settings.configure(
    DEBUG=True,
    TEMPLATES=[dict(
        # DEBUG = True,
        BACKEND='django.template.backends.django.DjangoTemplates',
        APP_DIRS=True,
        DIRS=[
            os.path.join(BASE_DIR, 'allauthdemo'),
        ],
    )],
)

try:
    django.setup()  # for Django >= 1.7
except AttributeError:
    pass  # must be < Django 1.7

from django.template.loader import get_template
from django.template import engines  # Django >= 1.11

commands_template = engines['django'].from_string("""
Run these commands:

    python manage.py makemigrations allauthdemo_auth
    python manage.py migrate
    python manage.py createsuperuser
    {% if facebook %}# Facebook
    python manage.py set_auth_provider facebook {{facebook.client_id}} {{facebook.secret}}{% endif %}
    {% if google %}# Google
    python manage.py set_auth_provider google {{google.client_id}} {{google.secret}}{% endif %}

If you have other providers you can add them in that way.
""")

settings_template = get_template("settings.template.py")


def heading(text):
    text = text.strip()
    line = '-' * len(text)
    print("\n%s\n%s\n%s\n" % (line, text, line))


def ask_yes_no(msg):
    msg = "\n" + msg.strip() + '\n\nPlease enter "yes" or "no": '
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
            pass  # raw_input('Please enter a value.')


def ask_facebook():
    secret = ask_text("Facebook App Secret")
    client_id = ask_text("Facebook App ID (not client token)")
    return dict(secret=secret, client_id=client_id)


def ask_google():
    secret = ask_text("Google Secret")
    client_id = ask_text("Google Client ID")
    return dict(secret=secret, client_id=client_id)


if __name__ == "__main__":

    context = {
        'now': str(datetime.now()),
        'secret_key': get_random_secret_key(),
    }

    heading("Facebook")
    if ask_yes_no("Do you want to configure auth via Facebook?\n"
                  "You'll need the app secret and client."):
        context['facebook'] = ask_facebook()

    heading("Google")
    if ask_yes_no("Do you want to configure auth via Google?\n"
                  "You'll need the app secret and client."):
        context['google'] = ask_google()

    heading("Rendering settings...")
    with open('allauthdemo/settings.py', 'w') as out:
        out.write(settings_template.render(context, request=None))
    print("OK")

    heading("Next steps")
    print(commands_template.render(context, request=None))
    heading("Done")
