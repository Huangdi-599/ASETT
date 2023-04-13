from rest_framework import serializers
from .models import Crypto,Portfolio,PortfolioCrypto
from .auth_serializers import UserDataSerializer
from .crypto import Crypto_data


class CryptoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crypto
        fields = '__all__'
        


class PortfolioCryptoSerializer(serializers.ModelSerializer):
    crypto = CryptoSerializer(read_only=True)
    value = serializers.DecimalField(max_digits=20, decimal_places=10, read_only=True)
    class Meta:
        model = PortfolioCrypto
        fields = ('crypto', 'quantity','value')

class PortfolioSerializer(serializers.ModelSerializer):
    user = UserDataSerializer(read_only = True)
    portfolio_crypto = PortfolioCryptoSerializer(many=True, read_only=True)
    total_value = serializers.SerializerMethodField()
    class Meta:
        model = Portfolio
        fields = ('id','name', 'description', 'user', 'portfolio_crypto','total_value')

    
    def get_total_value(self, obj):
        return sum([pc.value for pc in obj.portfolio_crypto.all()])    
    
    def validate_name(self, value):
        request =  self.context.get('request')
        q = Portfolio.objects.filter(user=request.user)
        query = q.filter(name__iexact = value)
        if query.exists():
            raise serializers.ValidationError("This name already exist")
        return value


#class ReferralBonusSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = ReferralBonus
#        fields = ('id', 'referrer', 'referral_link', 'bonus_amount')
#