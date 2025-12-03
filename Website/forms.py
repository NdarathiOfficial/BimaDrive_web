from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class ClientRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'client'
        if commit:
            user.save()
        return user

class InsurerRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'insurer'
        if commit:
            user.save()
        return user


# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from .models import User
#
#
# class ClientRegisterForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ["username", "email", "password1", "password2"]
#
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.role = "client"
#         if commit:
#             user.save()
#         return user
#
#
# class InsurerRegisterForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ["username", "email", "password1", "password2"]
#
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.role = "insurer"
#         if commit:
#             user.save()
#         return user
