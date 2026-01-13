from django.shortcuts import render
from astrologers.models import AstrologerProfile
from astromall.models import Product, Category

def home_view(request):
    astrologers = AstrologerProfile.objects.all()[:4]
    # Fetch categories that have products, and prefetch products for them
    categories = Category.objects.filter(products__isnull=False).distinct().prefetch_related('products')
    
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
