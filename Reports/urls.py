from django.urls import path

from .views import *


urlpatterns = [
    path('company/transactions/', CompanyTransactions.as_view()),
    path('employee/transactions/', EmployeeTransactions.as_view()),
    path('employee/count/', EmployeeCount.as_view())
]
