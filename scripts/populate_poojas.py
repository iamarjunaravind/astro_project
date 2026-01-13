import os
import django
import sys
from decimal import Decimal

# Add the project root to the python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'astro_project.settings')
django.setup()

from astromall.models import Category, Product

def populate_poojas():
    # 1. Ensure Category Exists
    pooja_category, created = Category.objects.get_or_create(name='Pooja')
    if created:
        print(f"Created category: {pooja_category.name}")
    else:
        print(f"Found category: {pooja_category.name}")

    # 2. Define Sample Poojas
    poojas = [
        {
            "name": "Ganesh Puja",
            "description": "A sacred puja to Lord Ganesha to remove obstacles and bring success. Performed by experienced Vedic priests.",
            "price": Decimal("2100.00"),
            "stock_quantity": 999
        },
        {
            "name": "Lakshmi Kubera Puja",
            "description": "Invoke the blessings of Goddess Lakshmi and Lord Kubera for wealth, prosperity, and financial stability.",
            "price": Decimal("5100.00"),
            "stock_quantity": 999
        },
        {
            "name": "Navagraha Shanti Puja",
            "description": "Pacify the nine planets and reduce their malefic effects. Brings peace and harmony to life.",
            "price": Decimal("3500.00"),
            "stock_quantity": 999
        },
        {
            "name": "Rudra Abhishekam",
            "description": "Powerful bathing ceremony of Lord Shiva to attain peace, health, and prosperity.",
            "price": Decimal("2500.00"),
            "stock_quantity": 999
        },
        {
            "name": "Maha Mrityunjaya Homa",
            "description": "A powerful Homa for longevity and protection against severe ailments and untimely death.",
            "price": Decimal("11000.00"),
            "stock_quantity": 999
        }
    ]

    # 3. Create Products
    for item in poojas:
        product, created = Product.objects.get_or_create(
            name=item['name'],
            category=pooja_category,
            defaults={
                "description": item['description'],
                "price": item['price'],
                "stock_quantity": item['stock_quantity']
            }
        )
        if created:
            print(f"Created product: {product.name}")
        else:
            print(f"Product already exists: {product.name}")

if __name__ == '__main__':
    populate_poojas()
