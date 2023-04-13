from django.test import TestCase
from rest_framework.test import APITestCase,APIClient
from django.contrib.auth.models import User 
from rest_framework import status
from django.urls import reverse
from datetime import datetime, timedelta
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Portfolio, Crypto, PortfolioCrypto,PasswordResetToken
from .auth_serializers import SignupSerializer
# Create your tests here.
"""
Test For USER resgistration and Authentication
"""

from .auth_serializers import SignupSerializer

class SignupSerializerTestCase(APITestCase):
    def setUp(self):
        self.valid_payload = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword123',
            'password2': 'testpassword123',
            'first_name': 'Test',
            'last_name': 'User'
        }

    def test_valid_signup_data(self):
        serializer = SignupSerializer(data=self.valid_payload)
        self.assertTrue(serializer.is_valid())

    def test_invalid_email(self):
        payload = self.valid_payload.copy()
        payload['email'] = 'invalid_email'
        serializer = SignupSerializer(data=payload)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors['email'][0], 'Enter a valid email address.')

    def test_password_mismatch(self):
        payload = self.valid_payload.copy()
        payload['password2'] = 'mismatched_password'
        serializer = SignupSerializer(data=payload)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors['password'][0], "Password fields didn't match.")

    def test_password_weak(self):
        payload = self.valid_payload.copy()
        payload['password'] = 'weakpassword'
        serializer = SignupSerializer(data=payload)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors['password'][0], "This password is too weak. It must contain at least 8 characters, including at least 1 letter and 1 digit.")

    def test_username_exists(self):
        User.objects.create_user(username='testuser', email='testuser2@example.com', password='testpassword123')
        serializer = SignupSerializer(data=self.valid_payload)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors['username'][0], 'A user with that username already exists.')

    def test_email_exists(self):
        User.objects.create_user(username='testuser2', email='testuser@example.com', password='testpassword123')
        serializer = SignupSerializer(data=self.valid_payload)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors['email'][0], 'A user with that email address already exists.')

class LoginViewTest(APITestCase):

    def setUp(self):
        self.username = 'testuser'
        self.email = 'testuser@example.com'
        self.password = 'testpass123'
        self.user = User.objects.create_user(username=self.username, email=self.email, password=self.password)

    def test_login_with_valid_credentials(self):
        url = reverse('login')
        data = {'email': self.email, 'password': self.password}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

        refresh_token = response.data['refresh']
        refresh = RefreshToken(refresh_token)
        self.assertEqual(str(refresh.access_token.user_id), str(self.user.id))

    def test_login_with_invalid_credentials(self):
        url = reverse('login')
        data = {'email': self.email, 'password': 'wrongpassword'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('access', response.data)
        self.assertNotIn('refresh', response.data)


"""
PASSWORD RESET
"""
class PasswordResetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', email='testuser@test.com', password='testpassword')
        self.client = APIClient()
        self.url_reset = reverse('password_reset')
        self.url_confirm = reverse('password_reset_confirm')
    
    def test_password_reset_request(self):
        """
        Test password reset request with valid email.
        """
        data = {'email': 'testuser@test.com'}
        response = self.client.post(self.url_reset, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data['message'], 'Password reset email sent.')

    def test_password_reset_request_invalid_email(self):
        """
        Test password reset request with invalid email.
        """
        data = {'email': 'invalid_email'}
        response = self.client.post(self.url_reset, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data['email'][0], 'Enter a valid email address.')
    
    def test_password_reset_confirm(self):
        """
        Test password reset confirmation with valid token and new password.
        """
        token = PasswordResetToken.objects.create(user=self.user, token='testtoken',
                                                  created_at=datetime.now() - timedelta(hours=2))
        data = {'token': token.token, 'password': 'newtestpassword'}
        response = self.client.post(self.url_confirm, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data['message'], 'Password reset successfully.')
    
    def test_password_reset_confirm_invalid_token(self):
        """
        Test password reset confirmation with invalid token.
        """
        data = {'token': 'invalid_token', 'password': 'newtestpassword'}
        response = self.client.post(self.url_confirm, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data['non_field_errors'][0], 'Invalid token.')
    
    def test_password_reset_confirm_expired_token(self):
        """
        Test password reset confirmation with expired token.
        """
        token = PasswordResetToken.objects.create(user=self.user, token='testtoken',
                                                  created_at=datetime.now() - timedelta(days=2))
        data = {'token': token.token, 'password': 'newtestpassword'}
        response = self.client.post(self.url_confirm, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data['non_field_errors'][0], 'Token has expired.')



"""
Test For Portfoilios
"""
class PortfolioTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser', email='testuser@test.com', password='testpass')
        
    def test_create_portfolio(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/portfolios/', {'name': 'My Portfolio', 'description': 'My Portfolio Description'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'My Portfolio')
        self.assertEqual(response.data['description'], 'My Portfolio Description')
        self.assertEqual(response.data['user'], self.user.id)

class AddCryptoViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='test_user', email='test@example.com', password='test_password'
        )
        self.client.force_authenticate(user=self.user)

        # Create a crypto to add to the portfolio
        self.crypto = Crypto.objects.create(
            name='Bitcoin',
            symbol='BTC',
            price=45000,
            quantity=100
        )

        # Create a portfolio for the user
        self.portfolio = Portfolio.objects.create(
            name='Test Portfolio',
            description='Test Portfolio Description',
            user=self.user,
            quantity=0
        )

    def test_add_crypto_to_portfolio(self):
        url = f'/api/portfolios/{self.portfolio.pk}/add-crypto/'
        data = {
            'crypto_id': self.crypto.pk,
            'quantity': 10
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify that the portfolio crypto was added
        portfolio_crypto = PortfolioCrypto.objects.filter(
            portfolio=self.portfolio,
            crypto=self.crypto
        ).first()
        self.assertIsNotNone(portfolio_crypto)
        self.assertEqual(portfolio_crypto.quantity, 10)

    def test_add_crypto_to_portfolio_with_invalid_crypto_id(self):
        url = f'/api/portfolios/{self.portfolio.pk}/add-crypto/'
        data = {
            'crypto_id': 9999,  # Invalid crypto id
            'quantity': 10
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Crypto with id 9999 does not exist')

    def test_add_crypto_to_nonexistent_portfolio(self):
        url = '/api/portfolios/9999/add-crypto/'  # Nonexistent portfolio id
        data = {
            'crypto_id': self.crypto.pk,
            'quantity': 10
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)