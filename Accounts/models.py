from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import PermissionsMixin

from .Enums import EmployeeEnums
from .managers import UserManager
from .validators import PhoneNumberValidator


class Users(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()
    phone_number_validator = PhoneNumberValidator()

    username = models.CharField(
        max_length=150,
        unique=True,
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        validators=[username_validator],
        error_messages={
            "unique": "A user with that username already exists.",
        },
    )
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=12, unique=True, validators=[phone_number_validator])
    is_staff = models.BooleanField(
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )
    is_active = models.BooleanField(default=True)

    object = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    @classmethod
    def normalize_phone_number(cls, phone_number):
        """
            remove 0 and add country code at the beginning off phone number
        """
        return phone_number


class Company(models.Model):
    name = models.CharField(
        max_length=150, unique=True, error_messages={
            "unique": "A user with that username already exists.",
        })
    logo = models.ImageField(upload_to='company/', height_field=100, width_field=100, null=True, blank=True)
    max_credit_limit = models.PositiveIntegerField()

    user = models.OneToOneField(Users, on_delete=models.CASCADE)


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

    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='employees')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='employees')

