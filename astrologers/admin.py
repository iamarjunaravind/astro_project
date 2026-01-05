from django.contrib import admin
from .models import AstrologerProfile, Skill, Language

@admin.register(AstrologerProfile)
class AstrologerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'experience_years', 'chat_price_per_minute', 'call_price_per_minute')
    list_filter = ('skills', 'languages')
    search_fields = ('user__username', 'bio')

admin.site.register(Skill)
admin.site.register(Language)
