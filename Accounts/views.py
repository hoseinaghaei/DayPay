from django.shortcuts import render

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import permissions, generics, status

from Bases.base_views import BaseAPIView
from .serializers import LoginSerializer
from .services import AuthenticationService


class LoginApi(BaseAPIView):
    authentication_classes = []
    serializer_class = LoginSerializer

    def post(self, request: Request):
        try:
            validated_data = self._prepare_validated_data(request)
            response = AuthenticationService().login_password(validated_data, request.query_params.get('type', 'Employee'))
            return response
        except Exception as e:
            return Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SendOTPApi(BaseAPIView):
    authentication_classes = []
    serializer_class = LoginSerializer

    def post(self, request):
        try:
            validated_data = self._prepare_validated_data(request)
            response = AuthenticationService().generate_opt(validated_data)
            return response
        except Exception as e:
            return Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPApi(BaseAPIView):
    authentication_classes = []
    serializer_class = LoginSerializer

    def post(self, request):
        try:
            validated_data = self._prepare_validated_data(request)
            response = AuthenticationService().login_otp(validated_data, request.query_params.get('type', 'Employee'))
            return response
        except Exception as e:
            return Response(data={"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(BaseAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        pass


class CompanyProfileApi(BaseAPIView):
    def get(self, request):
        pass


class EmployeeProfileApi(BaseAPIView):
    def get(self, request):
        pass
