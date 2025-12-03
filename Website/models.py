from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('client', 'Client'),
        ('insurer', 'Insurer'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.username} ({self.role})"

# from django.db import models
#
# # Create your models here.
# from django.contrib.auth.models import AbstractUser
# from django.db import models
#
# # class User(AbstractUser):
# #     ROLE_CHOICES = (
# #         ('client', 'Client'),
# #         ('insurer', 'Insurer'),
# #     )
# #     role = models.CharField(max_length=10, choices=ROLE_CHOICES)
#
# class ClientProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client_profile')
#     phone = models.CharField(max_length=15)
#     address = models.TextField(blank=True, null=True)
#     date_of_birth = models.DateField(blank=True, null=True)
#
#     def __str__(self):
#         return self.user.username
#
# class InsurerProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='insurer_profile')
#     company_name = models.CharField(max_length=100)
#     license_number = models.CharField(max_length=50)
#     contact_email = models.EmailField()
#
#     def __str__(self):
#         return self.company_name
#
# class InsurancePolicy(models.Model):
#     POLICY_TYPE_CHOICES = (
#         ('health', 'Health'),
#         ('vehicle', 'Vehicle'),
#         ('life', 'Life'),
#         ('home', 'Home'),
#     )
#
#     insurer = models.ForeignKey(InsurerProfile, on_delete=models.CASCADE, related_name='policies')
#     client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, related_name='policies')
#     policy_type = models.CharField(max_length=20, choices=POLICY_TYPE_CHOICES)
#     policy_number = models.CharField(max_length=50, unique=True)
#     coverage_amount = models.DecimalField(max_digits=12, decimal_places=2)
#     premium_amount = models.DecimalField(max_digits=12, decimal_places=2)
#     start_date = models.DateField()
#     end_date = models.DateField()
#     active = models.BooleanField(default=True)
#
#     def __str__(self):
#         return f"{self.policy_number} - {self.policy_type}"
#
# class Claim(models.Model):
#     STATUS_CHOICES = (
#         ('pending', 'Pending'),
#         ('approved', 'Approved'),
#         ('rejected', 'Rejected'),
#     )
#
#     policy = models.ForeignKey(InsurancePolicy, on_delete=models.CASCADE, related_name='claims')
#     description = models.TextField()
#     amount = models.DecimalField(max_digits=12, decimal_places=2)
#     date_submitted = models.DateTimeField(auto_now_add=True)
#     status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
#
#     def __str__(self):
#         return f"Claim for {self.policy.policy_number} - {self.status}"
#
# class Payment(models.Model):
#     policy = models.ForeignKey(InsurancePolicy, on_delete=models.CASCADE, related_name='payments')
#     amount = models.DecimalField(max_digits=12, decimal_places=2)
#     payment_date = models.DateTimeField(auto_now_add=True)
#     payment_method = models.CharField(max_length=50)
#
#     def __str__(self):
#         return f"{self.policy.policy_number} - {self.amount}"
# from django.db import models
#
# # Create your models here.
