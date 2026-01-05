from django.contrib import admin
from .models import ZodiacSign, DailyHoroscope

@admin.register(DailyHoroscope)
class DailyHoroscopeAdmin(admin.ModelAdmin):
    list_display = ('sign', 'date')
    list_filter = ('sign', 'date')

admin.site.register(ZodiacSign)
