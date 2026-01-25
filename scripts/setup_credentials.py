from django.contrib.auth import get_user_model
from astrologers.models import AstrologerProfile

User = get_user_model()

# 1. Reset Admin password
admin_user = User.objects.filter(is_superuser=True).first()
if admin_user:
    admin_user.set_password('admin123')
    admin_user.save()
    print(f"Admin password reset for: {admin_user.username}")
else:
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("Admin user created with password 'admin123'")

# 2. Setup Standard User
user, created = User.objects.get_or_create(username='user')
user.set_password('user123')
user.is_superuser = False
user.is_staff = False
user.save()
print(f"Standard user '{user.username}' updated/created with password 'user123'")

# 3. Setup Astrologer
astro_user, created = User.objects.get_or_create(username='astrologer')
astro_user.set_password('astro123')
astro_user.is_superuser = False
astro_user.is_staff = False
astro_user.save()

# Ensure AstrologerProfile exists
AstrologerProfile.objects.get_or_create(
    user=astro_user,
    defaults={
        'bio': 'Expert Astrologer',
        'experience_years': 5,
        'chat_price_per_minute': 10.00,
        'call_price_per_minute': 15.00
    }
)
print(f"Astrologer user '{astro_user.username}' updated/created with password 'astro123'")
