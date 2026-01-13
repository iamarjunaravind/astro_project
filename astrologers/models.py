from django.db import models
from django.conf import settings

class Skill(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class AstrologerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='astrologer_profile')
    bio = models.TextField()
    experience_years = models.IntegerField(default=0)
    skills = models.ManyToManyField(Skill)
    languages = models.ManyToManyField(Language)
    chat_price_per_minute = models.DecimalField(max_digits=6, decimal_places=2, default=10.00)
    call_price_per_minute = models.DecimalField(max_digits=6, decimal_places=2, default=15.00)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Astrologer {self.user.username}"
