import os
import django
from django.urls import reverse
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'astro_project.settings')
django.setup()

urls_to_check = [
    'astromall:product_list',
    'astromall:view_cart',
    'astromall:checkout',
]

print("Verifying Namespaced URLs...")
all_passed = True
for url_name in urls_to_check:
    try:
        url = reverse(url_name)
        print(f"PASS: {url_name} -> {url}")
    except Exception as e:
        print(f"FAIL: {url_name}. Error: {e}")
        all_passed = False

if all_passed:
    print("\nALL NAMESPACED URLS VERIFIED SUCCESS")
else:
    print("\nSOME NAMESPACED URLS FAILED")
