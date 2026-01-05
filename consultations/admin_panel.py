from django.contrib import admin
from .models import ChatSession, ChatMessage, Booking

class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0
    readonly_fields = ('sender', 'content', 'timestamp')

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'astrologer', 'start_time', 'is_active')
    list_filter = ('is_active', 'start_time')
    inlines = [ChatMessageInline]

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'astrologer', 'scheduled_at', 'status')
    list_filter = ('status', 'scheduled_at')
    search_fields = ('user__username', 'astrologer__user__username')
