from django.contrib.auth import get_user_model
from astrologers.models import AstrologerProfile
User = get_user_model()

print(f"Total users: {User.objects.count()}")
for u in User.objects.all():
    is_admin = u.is_superuser
    is_astrologer = hasattr(u, 'astrologer_profile')
    print(f"Username: {u.username}, Admin: {is_admin}, Astrologer: {is_astrologer}")
