from django.db import models
from django.conf import settings

class ChatSession(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='consultations_as_customer')
    astrologer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='consultations_as_astrologer')
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Chat between {self.customer} and {self.astrologer}"

class ChatMessage(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Message by {self.sender} at {self.timestamp}"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('reschedule_proposed', 'Reschedule Proposed'),
    ]
    TYPE_CHOICES = [
        ('chat', 'Chat'),
        ('call', 'Call'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    astrologer = models.ForeignKey('astrologers.AstrologerProfile', on_delete=models.CASCADE, related_name='bookings')
    scheduled_at = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    consultation_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='chat')
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    proposed_reschedule_time = models.DateTimeField(null=True, blank=True)

    @property
    def is_reviewed(self):
        return hasattr(self, 'review')

    def __str__(self):
        return f"Booking: {self.user.username} with {self.astrologer.user.username} on {self.scheduled_at}"

class Review(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='review')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Review for {self.booking}"
