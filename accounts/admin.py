from django.contrib import admin
from .models import User, UserProfile
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'groups')

admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile)