from django.db import models
from django.conf import settings

from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string

# Create your models here.
import uuid
from django.db import models
User = settings.AUTH_USER_MODEL


##class User(AbstractUser):
##    referral_code = models.CharField(max_length=20, blank=True)
##
##    def save(self, *args, **kwargs):
##        if not self.referral_code:
##            self.referral_code = get_random_string(length=6).upper()
##        super().save(*args, **kwargs)
##
##    def get_referral_link(self):
##        return f"{settings.BASE_URL}/signup?ref={self.referral_code}"
##
##
##class Referral(models.Model):
##    referrer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referral_referrer')
##    referred_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='referral_referred_user')
##    created_at = models.DateTimeField(auto_now_add=True)
#
 #   def __str__(self):
 #       return f"{self.referrer.username} referred {self.referred_user.username if self.referred_user else 'unknown user'}"

class Crypto(models.Model):
    name = models.CharField(max_length=100, unique=True)
    symbol = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=20, decimal_places=10)
    market_cap = models.IntegerField()
    percentage_change = models.DecimalField(max_digits=20, decimal_places=10)
    
    def __str__(self):
        return self.name
    
class Portfolio(models.Model):
    description = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='portfolio')
    crypto = models.ManyToManyField(Crypto, through='PortfolioCrypto', related_name='portfolio')

    def __str__(self):
        return f"{self.user.email}'s portfolio"

class PortfolioCrypto(models.Model):
    portfolio = models.ForeignKey('Portfolio', on_delete=models.CASCADE, related_name='portfolio_crypto')
    crypto = models.ForeignKey(Crypto, on_delete=models.CASCADE, related_name='portfolio_crypto')
    quantity = models.DecimalField(max_digits=20, decimal_places=10,default=0)
    
    @property
    def value(self):
        return self.quantity * self.crypto.price
    class Meta:
        unique_together = ('portfolio', 'crypto')



class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

