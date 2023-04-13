from django.db import models
from django.conf import settings

# Create your models here.
import uuid
from django.db import models
User = settings.AUTH_USER_MODEL


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
    quantity = models.DecimalField(max_digits=20, decimal_places=10)

    def __str__(self):
        return f"{self.user.email}'s portfolio"

class PortfolioCrypto(models.Model):
    portfolio = models.ForeignKey('Portfolio', on_delete=models.CASCADE, related_name='portfolio_crypto')
    crypto = models.ForeignKey(Crypto, on_delete=models.CASCADE, related_name='portfolio_crypto')
    quantity = models.DecimalField(max_digits=20, decimal_places=10,default=0)
    class Meta:
        unique_together = ('portfolio', 'crypto')


##class ReferralBonus(models.Model):
##    referrer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referral_bonus')
##    referral_link = models.CharField(max_length=100)
##    bonus_amount = models.DecimalField(max_digits=20, decimal_places=10)
##


##class PasswordResetToken(models.Model):
##    user = models.ForeignKey(User, on_delete=models.CASCADE)
##    token = models.CharField(max_length=100)
##    created_at = models.DateTimeField(auto_now_add=True)


class SessionToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
