# A new management command to create an 'Admin' group
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = "Creates an 'Admin' group if not exists"

    def handle(self, *args, **options):
        group_name = 'Admin'
        if not Group.objects.filter(name=group_name).exists():
            Group.objects.create(name=group_name)
            self.stdout.write(self.style.SUCCESS(f"Created group: {group_name}"))
        else:
            self.stdout.write(self.style.WARNING(f"Group {group_name} already exists"))
