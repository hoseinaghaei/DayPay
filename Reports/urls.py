from django.urls import path

from .views import *


urlpatterns = [
    path('company/transactions/', CompanyTransactions.as_view()),
    path('employee/transactions/', EmployeeTransactions.as_view()),
    path('company/details/', CompanyDetails.as_view()),
    path('employee/details/', EmployeeDetails.as_view()),
]
