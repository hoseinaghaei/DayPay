from django.urls import path

from .views import *


urlpatterns = [
    path('company/transactions/', CompanyTransactions.as_view()),
    path('employee/tranasctions/', EmployeeTransactions.as_view())
]
