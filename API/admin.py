from django.contrib import admin
from .models import Crypto, Portfolio,PortfolioCrypto,PasswordResetToken
# Register your models here.
admin.site.register(Portfolio)
admin.site.register(Crypto)
admin.site.register(PortfolioCrypto)
admin.site.register(PasswordResetToken)
