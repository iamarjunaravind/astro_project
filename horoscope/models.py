from django.db import models

class ZodiacSign(models.Model):
    name = models.CharField(max_length=20)
    image = models.ImageField(upload_to='zodiac_images/', null=True, blank=True)

    def __str__(self):
        return self.name

class DailyHoroscope(models.Model):
    sign = models.ForeignKey(ZodiacSign, on_delete=models.CASCADE, related_name='daily_horoscopes')
    date = models.DateField()
    description = models.TextField()
    
    class Meta:
        unique_together = ('sign', 'date')

    def __str__(self):
        return f"{self.sign.name} - {self.date}"
