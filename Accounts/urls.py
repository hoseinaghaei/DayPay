from django.urls import path

from .views import *


urlpatterns = [
    path('login/password/', LoginApi.as_view()),
]
