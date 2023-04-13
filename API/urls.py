from django.urls import path, include
##importing path from django
from . import views

#from rest_framework_simplejwt.views import (
#    TokenObtainPairView,
#    TokenRefreshView,
#    TokenVerifyView
#)


urlpatterns = [
    path('login/', views.LoginView.as_view(), name='token_obtain_pair'),
    path('signup', views.UserSignup.as_view()),
    path('password-reset/', views.PasswordResetRequestView.as_view(), name='password_reset'),
    path('password-reset/confirm/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    
    
    path('data', views.Cryptocurrencies, name='cryptocurrencies'),

    
    path('portfolios/', views.CreatePortfolioView.as_view(), name='create-portfolio'),
    path('portfolios/<int:pk>/add-crypto/', views.AddCryptoView.as_view(), name='add-crypto'),
    path('portfolios/<int:pk>/remove-crypto/<int:crypto_id>/', views.RemoveCryptoView.as_view(), name='remove-crypto'),
    path('portfolios/<int:pk>', views.PortfolioCryptoListView.as_view(), name='list-crypto'),

    
    path('', views.CryptoView.as_view(), name='list-cryptos'),
    #path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    #path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]