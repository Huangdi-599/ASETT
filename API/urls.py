from django.urls import path, include
##importing path from django
from . import views

#from rest_framework_simplejwt.views import (
#    TokenObtainPairView,
#    TokenRefreshView,
#    TokenVerifyView
#)


urlpatterns = [
    path('signup', views.UserSignup.as_view()),
    path('data', views.Cryptocurrencies, name='cryptocurrencies'),
    
    
    path('portfolios/create', views.CreatePortfolioView.as_view(), name='create-portfolio'),
    path('portfolios/<int:pk>/add-crypto/', views.AddCryptoView.as_view(), name='add-crypto'),
    path('portfolios/<int:pk>/remove-crypto/<int:crypto_id>/', views.RemoveCryptoView.as_view(), name='remove-crypto'),
    
    
    path('cryptos/', views.CryptoView.as_view(), name='list-cryptos'),
    #path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    #path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]