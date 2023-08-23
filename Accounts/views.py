from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, generics, status


class LoginApi(APIView):
    def post(self, request):
        pass


class SendOTPApi(APIView):
    def post(self, request):
        pass


class VerifyOTPApi(APIView):
    def post(self, request):
        pass


class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        pass


class CompanyProfileApi(APIView):
    def get(self, request):
        pass


class EmployeeProfileApi(APIView):
    def get(self, request):
        pass
