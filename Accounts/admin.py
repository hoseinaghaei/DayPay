from django.contrib import admin

from .models import *
from .forms import *


@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    def get_form(self, request, obj=None, **kwargs):
        defaults = {}
        if obj is None:
            defaults["form"] = self.add_form
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    pass


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    pass
