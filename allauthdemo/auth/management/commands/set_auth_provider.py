from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Update or insert a specific allauth provider entry like Google or Facebook'

    def add_arguments(self, parser):
        parser.add_argument('provider', type=str, help="Provider ID like 'google'")
        parser.add_argument('--name', default=None, type=str, help="Display name like 'Google' (optional)")
        parser.add_argument('client_id', type=str, help="Client ID from provider (==Facebook App ID)")
        parser.add_argument('client_secret', type=str, help="Secret from provider (==Facebook App Secret)")

    def handle(self, *args, **options):
        provider = options['provider']
        name = options.get('name') or provider.title()
        client_id = options['client_id']
        client_secret = options['client_secret']

        # Delete the specific provider if it exists.
        # Note that QuerySet.update_or_create is an alternative.
        SocialApp.objects.filter(provider=provider).delete()
        a = SocialApp(provider=provider, name=name, secret=client_secret,
                      client_id=client_id, key='')
        a.save()

        # Now associate this provider with all site instances.
        sites = [i for i in Site.objects.all()]
        a.sites.add(*sites)

        self.stdout.write(self.style.SUCCESS(
            "Provider '{}' -> client ID '{}'".format(a.name, a.client_id)
        ))
        self.stdout.write(self.style.SUCCESS(
            "Associated with site(s): {}".format(', '.join(s.name for s in sites))
        ))
