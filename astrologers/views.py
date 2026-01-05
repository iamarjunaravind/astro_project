from django.shortcuts import render, get_object_or_404
from .models import AstrologerProfile
from django.db.models import Q

def astrologer_list(request):
    query = request.GET.get('q')
    if query:
        astrologers = AstrologerProfile.objects.filter(
            Q(user__username__icontains=query) |
            Q(bio__icontains=query) |
            Q(skills__name__icontains=query)
        ).distinct()
    else:
        astrologers = AstrologerProfile.objects.all()
        
    return render(request, 'astrologers/list.html', {'astrologers': astrologers})

def astrologer_detail(request, pk):
    astrologer = get_object_or_404(AstrologerProfile, pk=pk)
    return render(request, 'astrologers/detail.html', {'astrologer': astrologer})
