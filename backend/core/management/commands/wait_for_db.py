"""
Django command to wait for the database to be available.
"""
import time

from psycopg2 import OperationalError as PsycopgError

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django wait_for_db command class. """

    def handle(self, *args, **options):
        """Entrypoint for command."""
        self.stdout.write('Waiting for database.')
        db_up = False
        while not db_up:
            try:
                self.check(databases=['default'])
                db_up = True
            except (PsycopgError, OperationalError):
                self.stdout.write('Database unavailable, waiting 2 second...')
                time.sleep(2)

        self.stdout.write(self.style.SUCCESS('Database available!'))

