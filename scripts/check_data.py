import os
import django
import sys

# Append project root to sys.path
sys.path.append(os.getcwd())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'astro_project.settings')
django.setup()

from astromall.models import Order
from astrologers.models import AstrologerProfile

print("--- Data Check ---")
print(f"Total Orders: {Order.objects.count()}")
for status, _ in Order.STATUS_CHOICES:
    count = Order.objects.filter(status=status).count()
    print(f"Orders with status '{status}': {count}")

print(f"\nTotal Astrologers: {AstrologerProfile.objects.count()}")
print(f"Verified Astrologers: {AstrologerProfile.objects.filter(is_verified=True).count()}")
print(f"Unverified Astrologers: {AstrologerProfile.objects.filter(is_verified=False).count()}")
