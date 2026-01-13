import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'astro_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from astrologers.models import AstrologerProfile

User = get_user_model()

def list_astrologers():
    profiles = AstrologerProfile.objects.all()
    if not profiles:
        print("No astrologer profiles found.")
        return

    print(f"Found {profiles.count()} astrologers:")
    for profile in profiles:
        print(f"User ID: {profile.user.id}, Username: {profile.user.username}, Email: {profile.user.email}")

if __name__ == '__main__':
    list_astrologers()
