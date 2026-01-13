from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, ProductForm
from django.contrib.admin.views.decorators import staff_member_required
from astromall.models import Product, Order
from astrologers.models import AstrologerProfile
from django.contrib.auth import get_user_model
from django.http import HttpResponseForbidden, JsonResponse
import json
from .authentication import verify_firebase_token
from .models import UserProfile
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum

User = get_user_model()



@login_required
def recharge_view(request):
    return render(request, 'accounts/recharge.html')

@csrf_exempt
def verify_phone_auth(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            id_token = data.get('idToken')
            action = data.get('action') # 'login' or 'register'
            
            # Verify Firebase Token
            decoded_token = verify_firebase_token(id_token)
            if not decoded_token:
                return JsonResponse({'success': False, 'message': 'Invalid OTP Token'})
            
            phone_number = decoded_token.get('phone_number')
            if not phone_number:
                 return JsonResponse({'success': False, 'message': 'Phone number not found in token'})

            if action == 'login':
                # Check if user exists with this phone number
                try:
                    profile = UserProfile.objects.get(phone_number=phone_number)
                    user = profile.user
                    login(request, user)
                    return JsonResponse({'success': True, 'redirect_url': '/'})
                except UserProfile.DoesNotExist:
                    return JsonResponse({'success': False, 'message': 'No account found with this phone number. Please register.'})
            
            elif action == 'register':
                # Registration Logic
                email = data.get('email')
                username = data.get('username')
                role = data.get('role', 'user') # Get role, default to user
                
                # Check for existing phone
                if UserProfile.objects.filter(phone_number=phone_number).exists():
                     return JsonResponse({'success': False, 'message': 'Phone number already registered. Please login.'})
                
                # Check for existing username/email by Django basics
                if User.objects.filter(username=username).exists():
                    return JsonResponse({'success': False, 'message': 'Username already taken.'})
                
                # Create User
                user = User.objects.create_user(username=username, email=email)
                
                # Fetch Profile created by signal and update phone
                profile = user.profile
                profile.phone_number = phone_number
                profile.save()
                
                # If Astrologer, create Unverified Profile with specific details
                if role == 'astrologer':
                    bio = data.get('bio', '')
                    experience = data.get('experience', 0)
                    try:
                        experience = int(experience)
                    except:
                        experience = 0
                        
                    AstrologerProfile.objects.create(
                        user=user,
                        bio=bio,
                        experience_years=experience,
                        is_verified=False
                        # skills/languages added later via profile edit or admin
                    )
                    # Astrologers don't get the welcome bonus
                    user.profile.wallet_balance = 0.00
                    user.profile.save()
                
                login(request, user)
                return JsonResponse({'success': True, 'redirect_url': '/'})
                
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
            
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

from .forms import AstrologerRegistrationForm
def register_astrologer_view(request):
    form = AstrologerRegistrationForm()
    return render(request, 'accounts/register_astrologer.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def profile_view(request):
    from astromall.models import Order
    from consultations.models import Booking
    
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')
    bookings = Booking.objects.filter(user=request.user).order_by('-scheduled_at')
    transactions = request.user.transactions.all().order_by('-timestamp')
    
    return render(request, 'accounts/profile.html', {
        'orders': orders,
        'bookings': bookings,
        'transactions': transactions
    })

@staff_member_required
def admin_dashboard(request):
    # Stats
    total_sales = Order.objects.filter(is_paid=True).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='Pending').count()
    total_users = User.objects.count()
    total_products = Product.objects.count()
    
    recent_orders = Order.objects.all().order_by('-created_at')[:5]

    context = {
        'total_sales': total_sales,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'total_users': total_users,
        'total_products': total_products,
        'recent_orders': recent_orders
    }
    return render(request, 'accounts/admin_dashboard.html', context)

@staff_member_required
def admin_product_list(request):
    products = Product.objects.all().order_by('-id')
    return render(request, 'accounts/admin_product_list.html', {'products': products})

@staff_member_required
def admin_product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('accounts:admin_product_list')
    else:
        form = ProductForm()
    return render(request, 'accounts/admin_product_form.html', {'form': form})

@staff_member_required
def admin_product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('accounts:admin_product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'accounts/admin_product_form.html', {'form': form})

@staff_member_required
def admin_astrologer_list(request):
    filter_status = request.GET.get('filter')
    astrologers = AstrologerProfile.objects.all().order_by('is_verified', '-id')
    
    if filter_status == 'verified':
        astrologers = astrologers.filter(is_verified=True)
    elif filter_status == 'unverified':
        astrologers = astrologers.filter(is_verified=False)
        
    return render(request, 'accounts/admin_astrologer_list.html', {
        'astrologers': astrologers,
        'current_filter': filter_status
    })

@staff_member_required
def admin_verify_astrologer(request, pk):
    if request.method == 'POST':
        astrologer = get_object_or_404(AstrologerProfile, pk=pk)
        action = request.POST.get('action')
        if action == 'approve':
            astrologer.is_verified = True
            astrologer.save()
        elif action == 'reject':
            astrologer.is_verified = False
            # astrologer.user.delete() # Optional: delete user if rejected? For now just unverify
            astrologer.save()
        return redirect('accounts:admin_astrologer_list')
    return redirect('accounts:admin_astrologer_list')

@staff_member_required
def admin_user_list(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'accounts/admin_user_list.html', {'users': users})

@staff_member_required
def admin_delete_user(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        if not user.is_superuser:
            user.delete()
        return redirect('accounts:admin_user_list')
    return redirect('accounts:admin_user_list')

@staff_member_required
def admin_order_list(request):
    status_filter = request.GET.get('status')
    orders = Order.objects.all().order_by('-created_at')
    
    if status_filter:
        orders = orders.filter(status=status_filter)
        
    return render(request, 'accounts/admin_order_list.html', {
        'orders': orders,
        'status_choices': [c[0] for c in Order.STATUS_CHOICES],
        'current_status': status_filter
    })

@staff_member_required
def admin_update_order_status(request, pk):
    if request.method == 'POST':
        order = get_object_or_404(Order, pk=pk)
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
    return redirect('accounts:admin_order_list')
