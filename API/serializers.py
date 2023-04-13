from rest_framework import serializers
from .models import Crypto,Portfolio
from .auth_serializers import UserDataSerializer
from .crypto import Crypto_data


class CryptoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crypto
        fields = ['id', 'name', 'symbol', 'price', 'quantity']


class PortfolioSerializer(serializers.ModelSerializer):
    user = UserDataSerializer(read_only = True)
    crypto = CryptoSerializer(many=True,required=False)
    class Meta:
        model = Portfolio
        fields = ['id','name','description','user','quantity', 'crypto']
        extra_kwargs = {'quantity': {'required': False, 'default': 0}}


#class ReferralBonusSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = ReferralBonus
#        fields = ('id', 'referrer', 'referral_link', 'bonus_amount')
#