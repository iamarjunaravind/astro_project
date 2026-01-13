from django.shortcuts import render, get_object_or_404
from .models import AstrologerProfile, Skill
from django.db.models import Q

def astrologer_list(request):
    query = request.GET.get('q')
    skill_filter = request.GET.get('skill')
    
    astrologers = AstrologerProfile.objects.filter(is_verified=True)
    
    if skill_filter:
        astrologers = astrologers.filter(skills__name=skill_filter)
    
    if query:
        astrologers = astrologers.filter(
            Q(user__username__icontains=query) |
            Q(bio__icontains=query) |
            Q(skills__name__icontains=query)
        ).distinct()
        
    skills = Skill.objects.all()
        
    return render(request, 'astrologers/list.html', {
        'astrologers': astrologers,
        'skills': skills,
        'selected_skill': skill_filter
    })

def astrologer_detail(request, pk):
    astrologer = get_object_or_404(AstrologerProfile, pk=pk)
    return render(request, 'astrologers/detail.html', {'astrologer': astrologer})
