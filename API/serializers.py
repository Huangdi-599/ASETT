from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.contrib.auth import password_validation,get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.utils.translation import gettext_lazy as _


from rest_framework import serializers
from .models import Crypto,Portfolio,PortfolioCrypto,PasswordResetToken
from .auth_serializers import UserDataSerializer

User = get_user_model()

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


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    token = serializers.CharField(read_only=True)
        
    def validate_email(self, value):
        # Check if the email belongs to a registered user
        try:
            User.objects.get(email=value) 
        except User.DoesNotExist:
            raise serializers.ValidationError('No account is associated with this email address.')
        return value

    def save(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        token = default_token_generator.make_token(user)
        PasswordResetToken.objects.create(user=user, token=token)
        # You can replace the following lines with your own email sending code
        #subject = 'Password Reset'
        #message = f'Use this token to reset your password: {token}'
        #user.email_user(subject, message)
        return {'email': email, 'token': token}

class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    def validate(self, data):
        token = data['token']
        try:
            password_reset_token = PasswordResetToken.objects.get(token=token)
        except PasswordResetToken.DoesNotExist:
            raise serializers.ValidationError('Invalid token.')

        user = password_reset_token.user
        password = data['password']
        password_confirm = data['password_confirm']

        # Validate that the two password fields match
        if password != password_confirm:
            raise serializers.ValidationError('Passwords do not match.')

        # Validate the new password using Django's built-in password validators
        try:
            password_validation.validate_password(password, user)
        except forms.ValidationError as e:
            raise serializers.ValidationError(e.messages)

        return data

    def save(self):
        token = self.validated_data['token']
        password = self.validated_data['password']
        password_reset_token = PasswordResetToken.objects.get(token=token)
        user = password_reset_token.user

        form = SetPasswordForm(user, {'new_password1': password, 'new_password2': password})
        if form.is_valid():
            form.save()

        # Delete the password reset token after the password is reset
        password_reset_token.delete()

        return user



#class ReferralBonusSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = ReferralBonus
#        fields = ('id', 'referrer', 'referral_link', 'bonus_amount')
#