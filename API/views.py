from django.shortcuts import render,redirect,get_object_or_404
import requests
from rest_framework import status
from rest_framework.response import Response

from rest_framework import generics
from django.core.paginator import Paginator

from .models import User,Crypto, Portfolio
#from .serializers import 
from .auth_serializers import SignupSerializer
from .serializers import CryptoSerializer, PortfolioSerializer

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

class UserSignup(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    template_name = 'signup.html'
    
    #def get(self, request):
    #    return render(request, self.template_name)
   


class CreatePortfolioView(generics.CreateAPIView):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer
    template_name = 'portfolio.html'
    #def get_queryset(self, *args , **kwargs):
    #   qs = super().get_queryset(*args , **kwargs)
    #   request  = self.request
    #   user = request.user
    #   if user.is_authenticated:
    #       return qs.filter(user = request.user) 
    def perform_create(self, serializer):
        request  = self.request
        instance = serializer.save()
        return Response(
            {"id": instance.id,"name":instance.name},
            status=status.HTTP_201_CREATED
        )
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        portfolio_id = response.data['id']
        return redirect('add-crypto', pk=portfolio_id)
    #def get(self, request):
    #    return render(request, self.template_name)


class AddCryptoView(generics.UpdateAPIView):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer
    lookup_field = 'pk'
    #def get_queryset(self):
    #    return Portfolio.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        portfolio = serializer.save()
        portfolio.last_updated = timezone.now()
        portfolio.save()
        
    def get_object(self):
       portfolio = get_object_or_404(Portfolio, pk=self.kwargs['pk'], user=self.request.user)
       return portfolio


class RemoveCryptoView(generics.DestroyAPIView):
    serializer_class = PortfolioSerializer

    def get_queryset(self):
        return Portfolio.objects.filter(user=self.request.user)

    def perform_destroy(self, instance):
        crypto_id = self.kwargs.get('crypto_id')
        try:
            crypto = Crypto.objects.get(id=crypto_id)
            instance.cryptos.remove(crypto)
            instance.last_updated = timezone.now()
            instance.save()
        except Crypto.DoesNotExist:
            raise ValidationError({'detail': 'Crypto object does not exist.'})


class CryptoView(generics.ListAPIView):
    queryset = Crypto.objects.all()
    serializer_class = CryptoSerializer