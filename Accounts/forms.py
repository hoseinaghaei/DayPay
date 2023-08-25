from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import Users


class UserCreationForm(forms.ModelForm):

    class Meta:
        model = Users
        fields = "__all__"

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        print(34)
        user.set_unique_secret_key()
        print(1)
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Users
        fields = "__all__"
