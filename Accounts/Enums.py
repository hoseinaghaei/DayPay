from django.db import models


class EmployeeEnums:
    class Genders(models.IntegerChoices):
        MALE = 1, 'male'
        FEMALE = 2, 'female'

    class Roles(models.IntegerChoices):
        TEAM_MEMBER = 1, 'team member'

    class MaritalStatus(models.IntegerChoices):
        SINGLE = 1, 'single'
        MARRIED = 2, 'married'

    class Status(models.IntegerChoices):
        ACTIVE = 1, 'active'
        INACTIVE = 2, 'inactive'
        FIRED = 3, 'fired'
