from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError
import time


class Command(BaseCommand):
    help = "Wait for the database to be ready"

    def handle(self, *args, **options):
        self.stdout.write("Waiting for database to be ready...")
        db_conn = True
        while not db_conn:
            try:
                db_conn = connections['default']
                db_conn.cursor()
                self.stdout.write(self.style.SUCCESS('Database is ready'))
                break
            except OperationalError:
                self.stdout.write("Database not ready, waiting 1 second...")
                time.sleep(1)
