from django.shortcuts import render

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import permissions, generics, status

from Bases.base_views import BaseAPIView
from .serializers import LoginSerializer, EmployeeSerializer
from .services import AuthenticationService
from . models import Employee


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


class EmployeeAPIs(BaseAPIView):
    serializer_class = EmployeeSerializer

    def get(self, request):
        company_id = request.query_params.get("company_id")
        employees = Employee.objects.filter(company_id=company_id)
        if employees.exists():
            serializer = self.serializer_class(employees, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({"error": str(Employee.DoesNotExist)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        try:
            employee_id = request.data.pop("employee_id")
            employee = Employee.objects.get(id=employee_id)
        except Employee.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(employee, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

