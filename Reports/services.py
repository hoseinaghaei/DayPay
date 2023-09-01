from django.db.models import Count
from rest_framework.response import Response
from rest_framework import status


from Accounts.Enums import EmployeeEnums
from Accounts.models import Employee


class CompanyReportService:

    @staticmethod
    def get_employees_count(company_id: int) -> Response:
        employee_counts = (
            Employee.objects.filter(company_id=company_id).values('status').annotate(status_count=Count('status')))

        status_counts = dict()
        for item in employee_counts:
            status_counts[EmployeeEnums.Status(item['status']).label] = item['status_count']

        return Response(data=status_counts, status=status.HTTP_200_OK)
