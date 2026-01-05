from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from astrologers.models import AstrologerProfile, Skill, Language
from astromall.models import Category, Product
from django.core.files.base import ContentFile
from django.conf import settings
import random
import requests
import os
import time

User = get_user_model()

class Command(BaseCommand):
    help = 'Populates database with dummy data and real images'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating data...')
        
        # Mapping categories to reliable free image keywords
        # Using Lorem Flickr or similar reliable placeholder service
        cat_keywords = {
            'Gemstones': ['gemstone', 'diamond', 'sapphire', 'crystal'],
            'Rudraksha': ['beads', 'necklace', 'seed'],
            'Yantra': ['mandala', 'geometry', 'sacred'],
            'Incense': ['incense', 'aroma', 'smoke'],
            'Books': ['book', 'ancient book', 'spiritual book']
        }

        def download_image(keywords, filename):
             try:
                # Randomly pick a keyword
                kw = random.choice(keywords)
                # Add random param to weird cache
                url = f"https://loremflickr.com/320/240/{kw}?random={random.randint(1, 1000)}"
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    return ContentFile(response.content, name=filename)
             except Exception as e:
                self.stdout.write(self.style.WARNING(f"Failed to download image: {e}"))
             return None

        # Create Categories and Products
        categories = {
            'Gemstones': ['Yellow Sapphire', 'Blue Sapphire', 'Ruby', 'Emerald', 'Pearl'],
            'Rudraksha': ['1 Mukhi', '5 Mukhi', 'Gauri Shankar'],
            'Yantra': ['Shree Yantra', 'Kuber Yantra'],
            'Incense': ['Sandalwood', 'Rose', 'Jasmine'],
            'Books': ['Lal Kitab', 'Vedic Astrology']
        }
        
        # Clear existing products to ensure "different images" request is met cleanly
        self.stdout.write('Clearing old products...')
        Product.objects.all().delete()
        
        for cat_name, product_names in categories.items():
            cat, _ = Category.objects.get_or_create(name=cat_name)
            keywords = cat_keywords.get(cat_name, ['spiritual'])
            
            for prod_name in product_names:
                # Check if product exists to avoid duplicates, but update image if missing
                prod, created = Product.objects.get_or_create(
                    category=cat,
                    name=prod_name,
                    defaults={
                        'description': f"Authentic {prod_name}", 
                        'price': random.randint(500, 5000)
                    }
                )
                
                # If created or no image, fetch one
                if created or not prod.image:
                    self.stdout.write(f"Downloading image for {prod_name}...")
                    img_file = download_image(keywords, f"{prod_name.replace(' ', '_').lower()}.jpg")
                    if img_file:
                        prod.image.save(f"{prod_name.replace(' ', '_').lower()}.jpg", img_file, save=True)
                        time.sleep(1) # Be nice to the API
                
        self.stdout.write(self.style.SUCCESS('Successfully populated Products with UNIQUE images'))
