from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = 'This command will setup groups and permissions'

    def handle(self, *args, **kwargs):
        try:
            gr_admin = Group.objects.get_or_create(name="Admin")[0]
            gr_mkt_driver = Group.objects.get_or_create(name="MKTDriver")[0]
            gr_moderator = Group.objects.get_or_create(name="Moderator")[0]
            print("Setup complete")
        except Exception as ex:
            raise CommandError(ex)
