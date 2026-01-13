import os
import sys
import django

# Add the project root to sys.path
sys.path.append(os.getcwd())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'astro_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from astrologers.models import AstrologerProfile

User = get_user_model()
profiles = AstrologerProfile.objects.all()

if profiles.exists():
    profile = profiles.first()
    u = profile.user
    u.set_password('password123')
    u.save()
    print(f"EXISTING_USER: {u.username}")
    print(f"PASSWORD: password123")
else:
    username = 'astrologer_demo'
    if User.objects.filter(username=username).exists():
         u = User.objects.get(username=username)
    else:
         u = User.objects.create_user(username=username, email='astro@example.com', password='password123')
    
    # Create profile if it doesn't exist for this user (e.g. if user existed but profile didn't)
    if not hasattr(u, 'astrologer_profile'):
        AstrologerProfile.objects.create(user=u, bio="Demo Astrologer", experience_years=5)
    else:
        # Just in case we didn't enter the first if block for some reason (shouldn't happen if profiles.exists() was false)
        pass 

    print(f"CREATED_USER: {u.username}")
    print(f"PASSWORD: password123")
