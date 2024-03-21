from django.core.management.base import BaseCommand
from django.core.cache import cache
from django_redis import get_redis_connection
import time


class Command(BaseCommand):
    help = "wait for Redis to be ready"

    def handle(self, *args, **options):
        self.stdout.write("Waiting for Redis...")
        redis_conn = None
        while not redis_conn:
            try:
                redis_conn = get_redis_connection("default")
                redis_conn.ping()
                self.stdout.write(self.style.SUCCESS("Redis is ready"))
                break
            except Exception as e:
                self.stdout.write(str(e))
                self.stdout.write("Redis not ready, waiting for 1 second...")
                time.sleep(1)
