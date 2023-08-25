from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import PermissionsMixin

from .Enums import EmployeeEnums
from .managers import UserManager
from .validators import PhoneNumberValidator
from .utils import generate_user_secret_key

from Bases.base_models import BaseModel


class Users(AbstractBaseUser, BaseModel, PermissionsMixin):
    phone_number_validator = PhoneNumberValidator()

    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=12, unique=True, validators=[phone_number_validator])
    is_staff = models.BooleanField(
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )
    is_active = models.BooleanField(default=True)
    secret_key = models.CharField(max_length=32, blank=True, null=True, unique=True)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Users'
        verbose_name_plural = 'Users'

    @classmethod
    def normalize_phone_number(cls, phone_number):
        """
            remove 0 and add country code at the beginning off phone number
        """
        return phone_number

    def set_unique_secret_key(self):
        secret_key = generate_user_secret_key()
        while Users.objects.filter(secret_key=secret_key).exists():
            secret_key = generate_user_secret_key()

        self.secret_key = secret_key


class Company(BaseModel):
    name = models.CharField(
        max_length=150, unique=True, error_messages={
            "unique": "A user with that username already exists.",
        })
    logo = models.ImageField(upload_to='company/', height_field=100, width_field=100, null=True, blank=True)
    max_credit_limit = models.PositiveIntegerField()
    given_credit = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    user = models.OneToOneField(Users, on_delete=models.CASCADE)


class Employee(BaseModel):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    role = models.IntegerField(choices=EmployeeEnums.Roles.choices, default=EmployeeEnums.Roles.TEAM_MEMBER)
    national_id = models.CharField(max_length=10)
    birth_date = models.DateField(null=True, blank=True)
    salary = models.PositiveBigIntegerField()
    credit_rate_limit = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(100)])
    gender = models.IntegerField(choices=EmployeeEnums.Genders.choices)
    marital_status = models.IntegerField(choices=EmployeeEnums.MaritalStatus.choices)
    credit_cart_number = models.CharField(max_length=16, null=True, blank=True)
    account_number = models.CharField(max_length=50, null=True, blank=True)
    sheba_number = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to='employee/', height_field=100, width_field=100, null=True, blank=True)
    status = models.IntegerField(choices=EmployeeEnums.Status.choices)
    is_active = models.BooleanField(default=True)

    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='employees')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='employees')

