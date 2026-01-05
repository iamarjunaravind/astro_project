import razorpay
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Transaction
import json

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@login_required
def create_recharge_order(request):
    if request.method == "POST":
        amount = request.POST.get('amount')
        if not amount:
            return JsonResponse({'error': 'Amount is required'}, status=400)
        
        try:
            amount = int(float(amount) * 100)  # Convert to paise
        except ValueError:
            return JsonResponse({'error': 'Invalid amount'}, status=400)

        data = {
            "amount": amount,
            "currency": "INR",
            "receipt": f"recharge_{request.user.id}",
        }
        
        try:
            order = client.order.create(data=data)
            return JsonResponse({
                'order_id': order['id'],
                'amount': order['amount'],
                'key_id': settings.RAZORPAY_KEY_ID,
                'user_name': request.user.username,
                'user_email': request.user.email,
                'user_phone': request.user.profile.phone_number if hasattr(request.user, 'profile') else ''
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request'}, status=405)

@csrf_exempt
@login_required
def verify_payment(request):
    if request.method == "POST":
        data = json.loads(request.body)
        
        try:
            # Verify signature
            client.utility.verify_payment_signature({
                'razorpay_order_id': data.get('razorpay_order_id'),
                'razorpay_payment_id': data.get('razorpay_payment_id'),
                'razorpay_signature': data.get('razorpay_signature')
            })
            
            # Signature is valid, credit the wallet
            amount = float(data.get('amount')) / 100  # Convert back from paise
            profile = request.user.profile
            profile.credit_wallet(amount, description=f"Wallet Recharge (ID: {data.get('razorpay_payment_id')})")
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'failure', 'error': str(e)}, status=400)
            
    return JsonResponse({'error': 'Invalid request'}, status=405)
