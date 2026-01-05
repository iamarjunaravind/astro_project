import os
import django
from django.template.loader import render_to_string
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'astro_project.settings')
django.setup()

templates = ['accounts/login.html', 'accounts/register.html']
print("Verifying Auth Templates...")

all_passed = True
for t in templates:
    try:
        render_to_string(t, {'form': 'MOCK_FORM'})
        print(f"PASS: {t} rendered successfully.")
    except Exception as e:
        print(f"FAIL: {t}. Error: {e}")
        all_passed = False

if all_passed:
    print("\nALL TEMPLATES VERIFIED SUCCESS")
else:
    print("\nSOME TEMPLATES FAILED")
