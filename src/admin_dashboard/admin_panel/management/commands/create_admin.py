"""
Django management command to create admin user
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Create an admin user for the dashboard'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, default='admin', help='Admin username')
        parser.add_argument('--password', type=str, default='admin123', help='Admin password')

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'User "{username}" already exists!'))
            return

        User.objects.create_superuser(username=username, password=password, email='')
        self.stdout.write(self.style.SUCCESS(f'✅ Admin user "{username}" created successfully!'))
        self.stdout.write(self.style.SUCCESS(f'   Username: {username}'))
        self.stdout.write(self.style.SUCCESS(f'   Password: {password}'))
