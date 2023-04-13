from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Portfolio, Crypto, PortfolioCrypto
# Create your tests here.
"""
Test For USER resgistration and Authentication
"""


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