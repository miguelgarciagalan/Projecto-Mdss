import time
from django.db import connection
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write('Waiting for database...')
        connected = False
        while not connected:
            try:
                connection.ensure_connection()
                connected = True
            except OperationalError:
                self.stdout.write('Database unavailable, waiting...')
                time.sleep(1)
        self.stdout.write('Database available!')
