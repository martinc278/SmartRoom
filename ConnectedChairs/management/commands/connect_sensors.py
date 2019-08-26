from django.core.management.base import BaseCommand, CommandError
from ConnectedChairs.views import connect_sensors

class Command(BaseCommand):
    help = 'Ping sensors and update database'

    def handle(self, *args, **options):
        connect_sensors()
