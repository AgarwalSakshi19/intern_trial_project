from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from myapp.models import Profile

class Command(BaseCommand):
    help = "Create missing profiles for all users"

    def handle(self, *args, **kwargs):
        for user in User.objects.all():
            Profile.objects.get_or_create(user=user)
        self.stdout.write(self.style.SUCCESS("Successfully ensured all users have profiles."))
