from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from .Enums import EmployeeEnums


class Company(models.Model):
    name = models.CharField(
        max_length=150, unique=True, error_messages={
            "unique": "A user with that username already exists.",
        })
    logo = models.ImageField()
    max_credit_limit = models.PositiveIntegerField()


class Employee(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    role = models.IntegerField(choices=EmployeeEnums.Roles, default=EmployeeEnums.Roles.TEAM_MEMBER)
    national_id = models.CharField(max_length=10)
    birth_date = models.DateField()
    salary = models.PositiveBigIntegerField()
    credit_rate_limit = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(100)])
    gender = models.IntegerField(choices=EmployeeEnums.Genders)
    marital_status = models.IntegerField(choices=EmployeeEnums.MaritalStatus)
    credit_cart_number = models.CharField(max_length=16)
    account_number = models.CharField(max_length=50)
    sheba_number = models.CharField(max_length=50)
    image = models.ImageField()
    status = models.IntegerField(choices=EmployeeEnums.Status)

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='employees')

