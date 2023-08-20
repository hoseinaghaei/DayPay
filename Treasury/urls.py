from django.urls import path
from .views import GiftAPI

urlpatterns = [
    path('gift/add', GiftAPI.as_view()),
    path('wallet/deposit', ),
    path('wallet/withdraw', ),
    path('wallet/show', ),
]
