from django.shortcuts import render
from astrologers.models import AstrologerProfile
from astromall.models import Product

def home_view(request):
    astrologers = AstrologerProfile.objects.all()[:4]
    products = Product.objects.all()[:4]
    
    context = {
        'astrologers': astrologers,
        'products': products
    }
    return render(request, 'home.html', context)
