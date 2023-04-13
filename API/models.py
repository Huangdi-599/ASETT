from django.db import models

# Create your models here.
import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    referral_link = models.CharField(max_length=100, blank=True, null=True)

    USERNAME_FIELD = 'email'

    def __str__(self):
        return str(self.id)

    def get_short_name(self):
        return self.email

class Crypto(models.Model):
    name = models.CharField(max_length=100, unique=True)
    symbol = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=20, decimal_places=10)
    quantity = models.DecimalField(max_digits=20, decimal_places=10)

    def __str__(self):
        return self.name


class Portfolio(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='portfolio')
    crypto = models.ManyToManyField(Crypto, related_name='portfolio')
    quantity = models.DecimalField(max_digits=20, decimal_places=10)

    def __str__(self):
        return f"{self.user.email}'s portfolio"


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
