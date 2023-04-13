from django.shortcuts import render,redirect,get_object_or_404
import requests
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User


from rest_framework import generics,permissions
from django.core.paginator import Paginator


from .models import Crypto, Portfolio,PortfolioCrypto
#from .serializers import 
from .auth_serializers import SignupSerializer,MyTokenObtainPairSerializer
from .serializers import CryptoSerializer, PortfolioSerializer,PortfolioCryptoSerializer

def Cryptocurrencies(request):
    data = requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false&locale=en').json()
    query = request.GET.get('q')
    if query:
        coins = [coin for coin in coins if query.lower() in coin['name'].lower()]
    paginator = Paginator(data, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'index.html', {'page_obj': page_obj, 'query': query})

#def Cryptocurrencies(request):
#    data = requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false&locale=en').json()
#    data = data[:10] 
#    return render(request,'index.html',{'data':data})


from rest_framework_simplejwt.views import TokenObtainPairView

class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class UserSignup(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    template_name = 'signup.html'
    permission_classes = [permissions.AllowAny]
    
    #def get(self, request):
    #    return render(request, self.template_name)
   
class CreatePortfolioView(generics.ListCreateAPIView):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer
    template_name = 'portfolio.html'
    def get_queryset(self, *args , **kwargs):
       qs = super().get_queryset(*args , **kwargs)
       request  = self.request
       user = request.user
       if user.is_authenticated:
           return qs.filter(user = request.user) 
    def perform_create(self, serializer):
        request  = self.request
        serializer.save(user = request.user)
    #def get(self, request):
    #    return render(request, self.template_name)

class AddCryptoView(generics.CreateAPIView):
    serializer_class = PortfolioCryptoSerializer
    
    def create(self, request, *args, **kwargs):
        portfolio_pk = kwargs.get('pk')
        user = request.user

        try:
            portfolio = Portfolio.objects.get(pk=portfolio_pk, user=user)
        except Portfolio.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Get the crypto to add to the portfolio
        crypto_id = request.data.get('crypto_id')
        quantity = request.data.get('quantity')
        try:
            crypto = Crypto.objects.get(id=crypto_id)
        except Crypto.DoesNotExist:
            return Response({'error': f'Crypto with id {crypto_id} does not exist'}, status=400)

        portfolio_crypto = PortfolioCrypto.objects.create(
            portfolio=portfolio,
            crypto=crypto,
            quantity=quantity
        )
        serializer = self.get_serializer(portfolio_crypto)
        return Response(serializer.data)

    
class PortfolioCryptoListView(generics.ListAPIView):
    serializer_class = CryptoSerializer
    def get_queryset(self):
        user = self.request.user
        portfolio_pk = self.kwargs.get('pk')
        try:
            portfolio = Portfolio.objects.get(pk=portfolio_pk, user=user)
        except Portfolio.DoesNotExist:
            return Crypto.objects.none()
        return portfolio.crypto.all()


class RemoveCryptoView(generics.DestroyAPIView):
    serializer_class = PortfolioSerializer
    lookup_field = 'pk'

    def destroy(self, request, *args, **kwargs):
        portfolio_pk = kwargs.get('pk')
        crypto_id = kwargs.get('crypto_id')
        user = request.user

        try:
            portfolio = Portfolio.objects.get(pk=portfolio_pk, user=user)
        except Portfolio.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            portfolio_crypto = PortfolioCrypto.objects.get(portfolio=portfolio, crypto__id=crypto_id)
        except PortfolioCrypto.DoesNotExist:
            return Response({'error': f'Crypto with id {crypto_id} does not exist in portfolio with id {portfolio_pk}'}, status=400)

        portfolio_crypto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        


class CryptoView(generics.ListAPIView):
    queryset = Crypto.objects.all()
    serializer_class = CryptoSerializer
    permission_classes = [permissions.AllowAny]