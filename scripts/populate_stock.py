import os
import django
import random
import sys

# Add project root to sys.path
sys.path.append(os.getcwd())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'astro_project.settings')
django.setup()

from astromall.models import Product

def populate_stock():
    products = Product.objects.all()
    count = 0
    for product in products:
        # Assign random stock between 10 and 100
        stock = random.randint(10, 100)
        product.stock_quantity = stock
        product.save()
        print(f"Updated {product.name} with stock: {stock}")
        count += 1
    
    print(f"\nSuccessfully updated {count} products with random stock values.")

if __name__ == "__main__":
    populate_stock()
