from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass
    # We can add fields like phone_number, is_astrologer, etc. here later if needed.
    # For now, we will rely on groups or related profile models to distinguish users.
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, blank=True, null=True, unique=True)
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def deduct_wallet(self, amount, description="Wallet Deduction"):
        if self.wallet_balance >= amount:
            self.wallet_balance -= amount
            self.save()
            Transaction.objects.create(
                user=self.user,
                amount=amount,
                transaction_type='debit',
                description=description
            )
            return True
        return False

    def credit_wallet(self, amount, description="Wallet Credit"):
        self.wallet_balance += amount
        self.save()
        Transaction.objects.create(
            user=self.user,
            amount=amount,
            transaction_type='credit',
            description=description
        )

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('credit', 'Credit'),
        ('debit', 'Debit'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    description = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.transaction_type.title()} of {self.amount} for {self.user.username}"

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Default 100 credits for new users
        UserProfile.objects.create(user=instance, wallet_balance=100.00)

