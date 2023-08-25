from django.urls import path
from .views import *

urlpatterns = [
    path('gift/add/', GiftAPI.as_view()),
    path('wallet/deposit/', DepositWalletApi.as_view()),
    path('wallet/withdraw/', WithdrawWalletAPI.as_view()),
    path('wallet/show/', GetWalletApi.as_view()),
    path('get/credit/', GetCreditApi.as_view())
]
