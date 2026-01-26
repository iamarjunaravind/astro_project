from django.shortcuts import render
from astrologers.models import AstrologerProfile
from astromall.models import Product, Category

def home_view(request):
    astrologers = AstrologerProfile.objects.all()[:14]
    # Fetch categories and prefetch products for each to avoid N+1 queries
    categories = Category.objects.all().prefetch_related('products')
    
    context = {
        'astrologers': astrologers,
        'categories': categories
    }
    return render(request, 'home.html', context)

def privacy_policy(request):
    return render(request, 'legal/privacy.html')

def terms_of_service(request):
    return render(request, 'legal/terms.html')

def refund_policy(request):
    return render(request, 'legal/refund.html')
