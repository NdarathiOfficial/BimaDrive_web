"""
URL configuration for Website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('base/', views.base, name='base'),

    path("login/", views.login_view, name="login"),

    path("register/client/", views.register_client, name="register_client"),
    path("register/insurer/", views.register_insurer, name="register_insurer"),

    path("dashboard/client/", views.client_dashboard, name="client_dashboard"),
    path("dashboard/insurer/", views.insurer_dashboard, name="insurer_dashboard"),
    path("about/", views.about, name='about'),
    path("contact/", views.contact, name='contact'),
    path("add_vehicle/", views.add_vehicle, name='add_vehicle'),
    path("vehicle_details/", views.vehicle_details, name='view_vehicle'),
    path("cover/", views.cover, name='cover'),
    path("report_accident/", views.report_accident, name='report_accident'),
    path("client_claims/", views.client_claims, name='client_claims'),
    path("insurer_claims/", views.insurer_claims, name='insurer_claims'),
    path("client_valuation/", views.client_valuation, name='client_valuation'),
    path("insurer_valuation/", views.insurer_valuation, name='insurer_valuation'),
    path("towing/", views.towing, name='towing'),
    path("update_vehicle_details/", views.update_vehicle_details, name='update_vehicle_details'),
    path("system_admin/", views.system_admin, name='system_admin'),
    path("admin_login/", views.admin_login, name='admin_login'),
    path("admin_register/", views.admin_register, name='admin_register'),
    path("profile/", views.profile, name='profile'),
    path("payment/", views.payment, name='payment'),
    path('stk_push/', views.initiate_stk_push, name='stk_push'),
    path('mpesa/callback', views.mpesa_callback, name='mpesa_callback'),

]
