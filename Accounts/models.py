from django.db import models

class Company(models.Model):
    name = models.CharField(
        max_length=150, unique=True, error_messages={
            "unique": "A user with that username already exists.",
        })
    logo = models.ImageField()
    max_credit_limit = models.PositiveIntegerField()


