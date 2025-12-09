from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.http import JsonResponse
from django_daraja.mpesa.core import MpesaClient

mpesa_api = MpesaClient()   # <-- FIX

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django_daraja.mpesa.core import MpesaClient

import json
import requests
import base64
from datetime import datetime
import os
import firebase_admin
from firebase_admin import credentials, db

from .forms import ClientRegisterForm, InsurerRegisterForm

# ---------------- FIREBASE INITIALIZATION ---------------- #
if not firebase_admin._apps:
    cred_path = 'serviceAccountKey.json'
    if os.path.exists(cred_path):
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://bimadrive-46fd0-default-rtdb.firebaseio.com'
        })
    else:
        print(f"Firebase key not found: {cred_path}")





# ----------------- AUTHENTICATION & REGISTRATION ----------------- #



def login_view(request):
    next_url = request.GET.get("next") or request.POST.get("next")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # If Django sent a ?next= redirect, honor it.
            if next_url:
                return redirect(next_url)

            # Otherwise use role-based redirect
            if user.role == "insurer":
                return redirect("insurer_dashboard")
            elif user.role == "system_admin":
                return redirect("system_admin")
            else:
                return redirect("client_dashboard")

    else:
        form = AuthenticationForm()

    return render(request, "accounts/login.html", {
        "form": form,
        "next": next_url,
    })



def register_client(request):
    form = ClientRegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("login")
    return render(request, "accounts/register_client.html", {"form": form})


def register_insurer(request):
    form = InsurerRegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("login")
    return render(request, "accounts/register_insurer.html", {"form": form})


# ----------------- DASHBOARDS ----------------- #

def client_dashboard(request):
    return render(request, "dashboards/client_dashboard.html")


def insurer_dashboard(request):
    return render(request, "dashboards/insurer_dashboard.html")


def system_admin(request):
    return render(request, "system_admin/system_admin.html")


# ----------------- PAGES ----------------- #
def index(request):
    return render(request, "index/index.html")


def base(request):
    return render(request, "base/base.html")


def contact(request):
    return render(request, "contact/contact.html")


def about(request):
    return render(request, "about/about.html")


def add_vehicle(request):
    return render(request, "add_vehicle/add_vehicle.html")

def vehicle_details(request):
    return render(request, "view_vehicle/vehicle_details.html")


def cover(request):
    return render(request, "cover/insurance_cover.html")


def report_accident(request):
    return render(request, "report_accident/report_accident.html")


def client_claims(request):
    return render(request, "claims/client_claims.html")


def insurer_claims(request):
    return render(request, "claims/insurer_claims.html")

def client_valuation(request):
    return render(request, "valuation/client_valuation.html")


def insurer_valuation(request):
    return render(request, "valuation/insurer_valuation.html")


def towing(request):
    return render(request, "towing/towing.html")


def update_vehicle_details(request):
    return render(request, "view_vehicle/update_vehicle_details.html")

def admin_login(request):
    return render(request, "system_admin/admin_login.html")

def admin_register(request):
    return render(request, "system_admin/admin_register.html")

def profile(request):
    return render(request, "profile/profile.html")

def payment(request):
    return render(request, "payment/payment.html")


import json
import logging
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django_daraja.mpesa.core import MpesaClient  # Ensure django-daraja is installed
import firebase_admin
from firebase_admin import credentials, db

logger = logging.getLogger(__name__)

# --- INITIALIZE FIREBASE (Run once) ---
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://bimadrive-46fd0-default-rtdb.firebaseio.com'
        })
    except Exception as e:
        print(f"Firebase Init Error: {e}")


@csrf_exempt
def initiate_stk_push(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            phone_number = data.get('phone')
            amount = int(data.get('amount'))
            user_id = data.get('userId')
            plan_name = data.get('plan')

            # Instantiate Client
            client = MpesaClient()
            account_reference = 'BimaDrive'
            transaction_desc = f'Payment for {plan_name}'
            callback_url = 'https://your-domain.com/mpesa/callback' # Must be a live URL

            # Make the STK Push Call
            # This returns an MpesaResponse object, NOT a dictionary
            response = client.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)

            # --- FIX IS HERE ---
            # Access attributes directly using dot notation, not .get()
            response_code = getattr(response, 'response_code', None)
            checkout_id = getattr(response, 'checkout_request_id', None)
            error_message = getattr(response, 'response_description', 'Unknown Error')

            if response_code == '0':
                # Save to Firebase PendingTransactions
                db.reference(f'PendingTransactions/{checkout_id}').set({
                    'userId': user_id,
                    'status': 'Pending',
                    'amount': amount,
                    'plan': plan_name,
                    'phone': phone_number,
                    'timestamp': datetime.now().isoformat()
                })

                # Return dictionary manually since MpesaResponse isn't JSON serializable by default
                return JsonResponse({
                    'ResponseCode': response_code,
                    'CheckoutRequestID': checkout_id,
                    'CustomerMessage': getattr(response, 'customer_message', 'Success')
                })
            else:
                return JsonResponse({'error': error_message}, status=400)

        except Exception as e:
            logger.error(f"STK Push Error: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Only POST method allowed'}, status=405)

@csrf_exempt
def mpesa_callback(request):
    """
    Receives M-Pesa result from Safaricom and updates Firebase.
    """
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            stk_callback = body.get('Body', {}).get('stkCallback', {})

            result_code = stk_callback.get('ResultCode')
            checkout_id = stk_callback.get('CheckoutRequestID')
            result_desc = stk_callback.get('ResultDesc')

            # Reference the transaction in Firebase
            pending_ref = db.reference(f'PendingTransactions/{checkout_id}')
            transaction_data = pending_ref.get()

            if result_code == 0:
                # --- SUCCESSFUL PAYMENT ---
                metadata = stk_callback.get('CallbackMetadata', {}).get('Item', [])

                # Extract Receipt
                mpesa_receipt = next((item['Value'] for item in metadata if item['Name'] == 'MpesaReceiptNumber'), None)

                if transaction_data and mpesa_receipt:
                    payment_record = {
                        'userId': transaction_data.get('userId'),
                        'amount': transaction_data.get('amount'),
                        'mpesaCode': mpesa_receipt,
                        'phoneNumber': transaction_data.get('phone'),
                        'status': 'Completed',
                        'plan': transaction_data.get('plan'),
                        'timestamp': datetime.now().isoformat()
                    }

                    # 1. Save Permanent Records
                    db.reference('Payments').push(payment_record)
                    db.reference('Receipts').push(payment_record)

                    # 2. Update Pending Node (Frontend listener triggers here)
                    pending_ref.update({
                        'status': 'Completed',
                        'mpesaCode': mpesa_receipt
                    })
            else:
                # --- FAILED PAYMENT ---
                if transaction_data:
                    pending_ref.update({
                        'status': 'Failed',
                        'reason': result_desc
                    })

        except Exception as e:
            print(f"Callback Error: {e}")

        return JsonResponse({'result': 'ok'})

    return JsonResponse({'error': 'Invalid method'}, status=405)