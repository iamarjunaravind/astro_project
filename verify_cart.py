import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'astro_project.settings')
django.setup()

from astromall.models import Product, CartItem, Order, Category

User = get_user_model()

def verify_cart():
    print("--- Verifying Cart Logic ---")
    
    # Get or create a test user
    user, _ = User.objects.get_or_create(username='testcartuser')
    user.set_password('password123')
    user.save()
    
    # Get or create a category and product
    cat, _ = Category.objects.get_or_create(name='Test Category')
    prod1, _ = Product.objects.get_or_create(
        name='Test Product 1', 
        category=cat, 
        defaults={'price': 100, 'description': 'Test prod'}
    )
    prod2, _ = Product.objects.get_or_create(
        name='Test Product 2', 
        category=cat, 
        defaults={'price': 250, 'description': 'Test prod'}
    )
    
    # Clear existing cart for user
    CartItem.objects.filter(user=user).delete()
    
    # 1. Add to cart
    CartItem.objects.create(user=user, product=prod1, quantity=1)
    CartItem.objects.create(user=user, product=prod2, quantity=2)
    
    cart_items = CartItem.objects.filter(user=user)
    assert cart_items.count() == 2, f"Expected 2 items, got {cart_items.count()}"
    
    # 2. Total calculation
    total = sum(item.total_price for item in cart_items)
    expected_total = 100 + (250 * 2) # 600
    assert total == expected_total, f"Expected total {expected_total}, got {total}"
    print(f"PASS: Cart total calculation correct (INR {total})")
    
    # 3. Simulate Checkout (creating order)
    order = Order.objects.create(customer=user, total_amount=total)
    # in view we would create OrderItems here
    
    assert Order.objects.filter(customer=user, total_amount=total).exists()
    print(f"PASS: Order creation verified for user {user.username}")
    
    # Cleanup
    CartItem.objects.filter(user=user).delete()
    print("--- Verification Finished Successfully ---")

if __name__ == "__main__":
    try:
        verify_cart()
    except Exception as e:
        print(f"FAIL: Verification failed with error: {e}")
