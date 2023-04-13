from django.contrib import admin
from .models import Crypto, Portfolio
# Register your models here.
admin.site.register(Portfolio)
admin.site.register(Crypto)