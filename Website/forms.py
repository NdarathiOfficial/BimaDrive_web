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


from django import forms
from django.contrib.auth.forms import SetPasswordForm
import re

class BimaDrivePasswordResetForm(forms.Form):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter your account email',
            'class': 'styled-input'
        })
    )

class BimaDriveSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter new password',
            'class': 'styled-input'
        })
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm new password',
            'class': 'styled-input'
        })
    )

    def clean_new_password1(self):
        password = self.cleaned_data.get('new_password1')
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[0-9]', password):
            raise forms.ValidationError("Password must contain at least one number.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise forms.ValidationError("Password must contain at least one special character.")
        return password