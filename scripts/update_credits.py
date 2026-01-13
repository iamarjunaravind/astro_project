import os
import sys
import django

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'astro_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from accounts.models import UserProfile

User = get_user_model()

def apply_credits():
    users = User.objects.all()
    count = 0
    for user in users:
        # Check if user is astrologer
        if hasattr(user, 'astrologer_profile'):
            print(f"Skipping Astrologer: {user.username}")
            # Ensure they have 0 if they shouldn't have bonus (optional, but good for consistency)
            # user.profile.wallet_balance = 0
            # user.profile.save()
            continue
            
        # Get or Create Profile
        profile, created = UserProfile.objects.get_or_create(user=user)
        
        # Apply 100 credits if they have less (assuming we want to top them up or set default)
        # User request: "add same credit to existing users"
        # I'll force set to 100 if it's the default 0, or add 100?
        # Let's set to 100 if < 100.
        if profile.wallet_balance < 100:
            profile.wallet_balance = 100.00
            profile.save()
            print(f"Updated User: {user.username} - Wallet: 100.00")
            count += 1
        else:
            print(f"User {user.username} already has {profile.wallet_balance}")

    print(f"Successfully updated {count} users.")

if __name__ == "__main__":
    apply_credits()
