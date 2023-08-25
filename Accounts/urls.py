from django.urls import path

from .views import *


urlpatterns = [
    path('login/password/', LoginApi.as_view()),
    path('send/otp/', SendOTPApi.as_view()),
    path('login/otp/', VerifyOTPApi.as_view())
]
