from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Category, CartItem, Order, OrderItem
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import razorpay
import json

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

from django.db.models import Q

def product_list(request):
    category_name = request.GET.get('category')
    query = request.GET.get('q')
    
    products = Product.objects.all()
    
    if category_name:
        products = products.filter(category__name=category_name)
    
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        ).distinct()
    
    categories = Category.objects.all()
    return render(request, 'astromall/list.html', {
        'products': products, 
        'categories': categories,
        'active_category': category_name
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'astromall/detail.html', {'product': product})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f"{product.name} added to your cart.")
    return redirect('astromall:view_cart')

@login_required
def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    CartItem.objects.get_or_create(user=request.user, product=product)
    return redirect('astromall:view_cart')

@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_amount = sum(item.total_price for item in cart_items)
    return render(request, 'astromall/cart.html', {
        'cart_items': cart_items,
        'total_amount': total_amount
    })

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    messages.info(request, "Item removed from cart.")
    return redirect('astromall:view_cart')

@login_required
def update_cart_quantity(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(CartItem, id=item_id, user=request.user)
        action = request.POST.get('action')
        
        if action == 'increment':
            item.quantity += 1
        elif action == 'decrement':
            if item.quantity > 1:
                item.quantity -= 1
            else:
                item.delete()
                messages.info(request, "Item removed from cart.")
                return redirect('astromall:view_cart')
        
        item.save()
    return redirect('astromall:view_cart')

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items:
        messages.warning(request, "Your cart is empty.")
        return redirect('astromall:product_list')
    
    total_amount = sum(item.total_price for item in cart_items)
    order = Order.objects.create(customer=request.user, total_amount=total_amount)
    
    # Import OrderDetail here to avoid circular imports if any, although here it's fine
    from .models import OrderDetail
    
    for item in cart_items:
        # Create relational order item
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity
        )
        # Create persistent order detail snapshot
        OrderDetail.objects.create(
            order=order,
            product=item.product,
            product_name=item.product.name,
            price=item.product.price,
            quantity=item.quantity
        )
    
    cart_items.delete()
    messages.success(request, f"Order {order.id} placed successfully!")
    return render(request, 'astromall/order_success.html', {'order': order})

@login_required
def initiate_payment(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items:
        return JsonResponse({'error': 'Cart is empty'}, status=400)
        
    total_amount = sum(item.total_price for item in cart_items)
    
    # Create the internal order record first
    order = Order.objects.create(customer=request.user, total_amount=total_amount)
    
    for item in cart_items:
        OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
        from .models import OrderDetail
        OrderDetail.objects.create(
            order=order, product=item.product, product_name=item.product.name, 
            price=item.product.price, quantity=item.quantity
        )
    
    # Now create Razorpay order
    data = {
        "amount": int(total_amount * 100), # amount in paise
        "currency": "INR",
        "receipt": f"order_{order.id}",
    }
    
    try:
        razorpay_order = client.order.create(data=data)
        return JsonResponse({
            'razorpay_order_id': razorpay_order['id'],
            'order_id': order.id,
            'amount': razorpay_order['amount'],
            'key_id': settings.RAZORPAY_KEY_ID,
            'user_name': request.user.username,
            'user_email': request.user.email
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@login_required
def verify_mall_payment(request):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id': data.get('razorpay_order_id'),
                'razorpay_payment_id': data.get('razorpay_payment_id'),
                'razorpay_signature': data.get('razorpay_signature')
            })
            
            order_id = data.get('order_id')
            order = get_object_or_404(Order, id=order_id, customer=request.user)
            order.is_paid = True
            order.save()
            
            # Clear cart on successful payment
            CartItem.objects.filter(user=request.user).delete()
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'failure', 'error': str(e)}, status=400)
            
    return JsonResponse({'error': 'Invalid request'}, status=405)
