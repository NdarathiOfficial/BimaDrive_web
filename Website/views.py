from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.http import JsonResponse
from django_daraja.mpesa.core import MpesaClient
import firebase_admin
from firebase_admin import credentials, db
import logging
import os

from google.rpc.http_pb2 import HttpResponse

mpesa_api = MpesaClient()   # <-- FIX

from webauthn.helpers.structs import (
    AuthenticatorSelectionCriteria,
    AuthenticatorAttachment,
    ResidentKeyRequirement,
    UserVerificationRequirement,
)

from .models import UserPasskey

from webauthn.helpers.structs import (
    AuthenticatorSelectionCriteria,
    AuthenticatorAttachment,
    ResidentKeyRequirement,
    UserVerificationRequirement,
)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django_daraja.mpesa.core import MpesaClient
logger = logging.getLogger(__name__)
if not firebase_admin._apps:
    try:
        # Construct the path to the service account JSON file securely.
        # This assumes the JSON file is in the same folder as this views.py file.
        current_dir = os.path.dirname(os.path.abspath(__file__))
        key_path = os.path.join(current_dir, 'firebase-service-account.json')

        cred = credentials.Certificate(key_path)
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://bimadrive-46fd0-default-rtdb.firebaseio.com/'
        })
        logger.info("Firebase Admin initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize Firebase Admin: {e}")
        # Fallback to default behavior if file is missing (will fail if credentials aren't in env variables)
        try:
            firebase_admin.initialize_app(options={
                'databaseURL': 'https://bimadrive-46fd0-default-rtdb.firebaseio.com/'
            })
        except Exception as fallback_e:
            logger.error(f"Fallback initialization also failed: {fallback_e}")

import json
import requests
import base64
from datetime import datetime
import os
import firebase_admin
from firebase_admin import credentials, db

from .forms import ClientRegisterForm, InsurerRegisterForm

logger = logging.getLogger(__name__)

# ----------------- STRICT FIREBASE INITIALIZATION ----------------- #
if not firebase_admin._apps:
    try:
        # Option A: Check Render Environment Variable first
        firebase_config_string = os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON")

        if firebase_config_string:
            cred_dict = json.loads(firebase_config_string)
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://bimadrive-46fd0-default-rtdb.firebaseio.com/'
            })
            logger.info("Firebase Admin initialized successfully using Environment Variable.")
        else:
            # Option B: Fallback to local JSON file path for development
            current_dir = os.path.dirname(os.path.abspath(__file__))
            key_path = os.path.join(current_dir, 'firebase-service-account.json')

            if os.path.exists(key_path):
                cred = credentials.Certificate(key_path)
                firebase_admin.initialize_app(cred, {
                    'databaseURL': 'https://bimadrive-46fd0-default-rtdb.firebaseio.com/'
                })
                logger.info("Firebase Admin initialized successfully with local JSON Key.")
            else:
                raise FileNotFoundError(
                    f"\n\n🚨 FIREBASE ERROR 🚨\n"
                    f"No FIREBASE_SERVICE_ACCOUNT_JSON environment variable found, "
                    f"and local file does not exist at:\n>>> {key_path} <<<\n\n"
                )
    except Exception as e:
        logger.error(f"Failed to initialize Firebase Admin: {e}")
        raise e



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



def payment_processing(request):
    return render(request, "payment/payment_processing.html")

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

            # Safely handle the amount
            amount = int(float(data.get('amount')))
            user_id = data.get('userId')
            plan_name = data.get('plan')

            # Instantiate Client
            client = MpesaClient()
            account_reference = 'BimaDrive'
            transaction_desc = f'Payment for {plan_name}'

            # --- LOCALHOST VS PRODUCTION CALLBACK LOGIC ---
            host = request.get_host()

            # If you are using Ngrok to test webhooks locally, you can set this env variable
            custom_callback = os.getenv('MPESA_CALLBACK_URL')

            if custom_callback:
                callback_url = f"{custom_callback.rstrip('/')}/mpesa/callback"
            elif host.startswith(('localhost', '127.0.0.1')):
                # Safaricom rejects localhost URLs. We use a dummy valid URL so the prompt still appears on your phone.
                # Note: You will not receive the automated success ping to your local database using a dummy URL.
                callback_url = "https://sandbox.safaricom.co.ke/mpesa/callback"
                logger.warning(
                    "Running on localhost. Using a dummy callback URL. Payment will trigger, but the callback won't reach your local database.")
            else:
                # Production: Dynamically generates your live Render domain (e.g., https://your-app.onrender.com/mpesa/callback)
                callback_url = request.build_absolute_uri('/mpesa/callback')

            # Make the STK Push Call
            response = client.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)

            # Access attributes directly using dot notation
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
    """Safaricom hits this endpoint automatically when the user puts in their PIN"""
    if request.method == 'POST':
        try:
            callback_data = json.loads(request.body.decode('utf-8'))
            stk_callback = callback_data.get('Body', {}).get('stkCallback', {})

            checkout_id = stk_callback.get('CheckoutRequestID')
            result_code = stk_callback.get('ResultCode')
            result_desc = stk_callback.get('ResultDesc')

            if checkout_id:
                status = 'Completed' if result_code == 0 else 'Failed'

                # Update Firebase so the frontend realtime listener triggers
                db.reference(f'PendingTransactions/{checkout_id}').update({
                    'status': status,
                    'resultDesc': result_desc,
                    'updatedAt': datetime.now().isoformat()
                })

            return JsonResponse({'ResultCode': 0, 'ResultDesc': 'Accepted'})
        except Exception as e:
            logger.error(f"Callback Error: {str(e)}")
            return JsonResponse({'error': 'Internal Server Error'}, status=500)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def query_payment_status(request):
    """Actively asks Safaricom for the status of a transaction using direct API calls"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            checkout_id = data.get('checkout_id')

            if not checkout_id:
                return JsonResponse({'error': 'CheckoutRequestID required'}, status=400)

            # Get Access Token
            access_token = get_mpesa_access_token()
            if not access_token:
                return JsonResponse({'status': 'Pending', 'message': 'Generating Token...'})

            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            passkey = settings.MPESA_PASSKEY
            business_short_code = settings.MPESA_EXPRESS_SHORTCODE
            password = base64.b64encode((business_short_code + passkey + timestamp).encode()).decode()

            payload = {
                "BusinessShortCode": business_short_code,
                "Password": password,
                "Timestamp": timestamp,
                "CheckoutRequestID": checkout_id
            }

            api_url = 'https://api.safaricom.co.ke/mpesa/stkpushquery/v1/query' if settings.MPESA_ENVIRONMENT == 'production' else 'https://sandbox.safaricom.co.ke/mpesa/stkpushquery/v1/query'
            headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}

            response = requests.post(api_url, json=payload, headers=headers, timeout=10)
            res_data = response.json()

            logger.info(f"M-Pesa Direct Query Response: {res_data}")

            result_code = str(res_data.get('ResultCode', ''))
            result_desc = str(res_data.get('ResultDesc', 'Processing'))

            status = 'Pending'
            if result_code == '0':
                status = 'Completed'
            elif result_code in ['1032', '1', '2001', '1037']:
                status = 'Failed'

            # Sync to Firebase
            if status != 'Pending':
                db.reference(f'PendingTransactions/{checkout_id}').update({
                    'status': status,
                    'resultDesc': result_desc,
                    'updatedAt': datetime.now().isoformat()
                })

            return JsonResponse({
                'status': status,
                'result_code': result_code,
                'result_desc': result_desc
            })

        except Exception as e:
            logger.error(f"STK Query Exception: {str(e)}")
            return JsonResponse({'status': 'Pending', 'message': 'Still processing...'}, status=200)

    return JsonResponse({'error': 'Only POST method allowed'}, status=405)

@csrf_exempt
def query_payment_status(request):
    """Actively asks Safaricom for the status of a transaction using direct API calls"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            checkout_id = data.get('checkout_id')

            if not checkout_id:
                return JsonResponse({'error': 'CheckoutRequestID required'}, status=400)

            # Get Access Token
            access_token = get_mpesa_access_token()
            if not access_token:
                return JsonResponse({'status': 'Pending', 'message': 'Generating Token...'})

            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            passkey = settings.MPESA_PASSKEY
            business_short_code = settings.MPESA_EXPRESS_SHORTCODE
            password = base64.b64encode((business_short_code + passkey + timestamp).encode()).decode()

            payload = {
                "BusinessShortCode": business_short_code,
                "Password": password,
                "Timestamp": timestamp,
                "CheckoutRequestID": checkout_id
            }

            api_url = 'https://api.safaricom.co.ke/mpesa/stkpushquery/v1/query' if settings.MPESA_ENVIRONMENT == 'production' else 'https://sandbox.safaricom.co.ke/mpesa/stkpushquery/v1/query'
            headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}

            response = requests.post(api_url, json=payload, headers=headers, timeout=10)
            res_data = response.json()

            logger.info(f"M-Pesa Direct Query Response: {res_data}")

            result_code = str(res_data.get('ResultCode', ''))
            result_desc = str(res_data.get('ResultDesc', 'Processing'))

            status = 'Pending'
            # ResultCode '0' means success in Safaricom Query
            if result_code == '0':
                status = 'Completed'
            # 1032 = Cancelled, 1 = Insufficient funds, 2001 = Wrong PIN, 1037 = Timeout
            elif result_code in ['1032', '1', '2001', '1037']:
                status = 'Failed'

            return JsonResponse({
                'status': status,
                'result_code': result_code,
                'result_desc': result_desc
            })

        except Exception as e:
            logger.error(f"STK Query Exception: {str(e)}")
            return JsonResponse({'status': 'Pending', 'message': 'Still processing...'}, status=200)

    return JsonResponse({'error': 'Only POST method allowed'}, status=405)
import requests
from requests.auth import HTTPBasicAuth
from django.core.cache import cache

def get_mpesa_access_token():
    """Fetches and caches the Safaricom M-Pesa Access Token securely."""
    cached_token = cache.get('mpesa_access_token')
    if cached_token:
        return cached_token

    consumer_key = settings.MPESA_CONSUMER_KEY
    consumer_secret = settings.MPESA_CONSUMER_SECRET

    api_url = ('https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
               if getattr(settings, 'MPESA_ENVIRONMENT', 'sandbox') == 'production'
               else 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials')

    try:
        r = requests.get(api_url, auth=HTTPBasicAuth(consumer_key, consumer_secret), timeout=10)
        r.raise_for_status()
        token = r.json()['access_token']

        # Cache token for 58 minutes (3500 seconds)
        cache.set('mpesa_access_token', token, 3500)
        return token
    except Exception as e:
        logger.error(f"M-PESA TOKEN ERROR: {e}")
        return None




import json
import base64
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from webauthn import (
    generate_authentication_options,
    verify_authentication_response,
    options_to_json
)
from webauthn.helpers.structs import PublicKeyCredentialRequestOptions
from .models import UserPasskey

# Configure your Relying Party settings (update domain for production)
RP_ID = "localhost"
RP_ORIGIN = "http://localhost:8000"


@csrf_exempt
def passkey_challenge_view(request):
    """Step C: Generate login challenge options for the login page."""
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=405)
    try:
        host_header = request.get_host().split(':')[0]
        rp_id = "localhost" if host_header in ["127.0.0.1", "localhost", ""] else host_header

        all_passkeys = UserPasskey.objects.all()
        if not all_passkeys.exists():
            return JsonResponse({
                "error": "No passkeys registered yet. Please log in with email and create one in your dashboard first."
            }, 400)

        allow_credentials = [
            {"id": base64.urlsafe_b64decode(pk.credential_id + "=="), "type": "public-key"}
            for pk in all_passkeys
        ]

        options = generate_authentication_options(
            rp_id=rp_id,
            allow_credentials=allow_credentials,
            user_verification=UserVerificationRequirement.PREFERRED,
        )

        request.session['passkey_challenge'] = options.challenge.hex()
        return HttpResponse(options_to_json(options), content_type="application/json")
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)




@csrf_exempt
def passkey_verify_view(request):
    """Step 2: Verify the signed assertion returned by the user's hardware."""
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    try:
        data = json.loads(request.body)
        expected_challenge = request.session.get('passkey_challenge')

        if not expected_challenge:
            return JsonResponse({"error": "Challenge expired or missing."}, status=400)

        credential_id_b64 = data.get("id")
        passkey_record = UserPasskey.objects.filter(credential_id=credential_id_b64).first()

        if not passkey_record:
            return JsonResponse({"error": "Passkey not recognized in database."}, status=404)

        # Verify the cryptographic assertion signature
        verification = verify_authentication_response(
            query=data,
            expected_challenge=bytes.fromhex(expected_challenge),
            expected_rp_id=RP_ID,
            expected_origin=RP_ORIGIN,
            credential_public_key=base64.b64decode(passkey_record.public_key),
            credential_current_sign_count=passkey_record.sign_count,
            require_user_verification=True,
        )

        # Update signature counter to prevent replay attacks
        passkey_record.sign_count = verification.new_sign_count
        passkey_record.save()

        # Clear challenge
        del request.session['passkey_challenge']

        return JsonResponse({
            "success": True,
            "message": "Passkey verified successfully",
            "redirect_url": "/client/dashboard/"  # Adjust to your client dashboard url name/path
        })

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)


import json
import base64
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from webauthn import (
    generate_registration_options,
    verify_registration_response,
    generate_authentication_options,
    verify_authentication_response,
    options_to_json,
)
from webauthn.helpers.structs import UserVerificationRequirement
from .models import UserPasskey

@csrf_exempt
def passkey_register_options_view(request):
    """Step A: Generate options for creating a new passkey from the dashboard."""
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=405)
    try:
        data = json.loads(request.body)
        firebase_uid = data.get("uid")
        email = data.get("email", "user@bimadrive.com")

        # Normalize host: if testing locally on 127.0.0.1, treat it as localhost for WebAuthn compliance
        host_header = request.get_host().split(':')[0]
        rp_id = "localhost" if host_header in ["127.0.0.1", "localhost", ""] else host_header

        authenticator_selection = AuthenticatorSelectionCriteria(
            authenticator_attachment=AuthenticatorAttachment.PLATFORM,
            resident_key=ResidentKeyRequirement.REQUIRED,
            user_verification=UserVerificationRequirement.PREFERRED,
        )

        options = generate_registration_options(
            rp_id=rp_id,
            rp_name="BimaDrive Insurance",
            user_id=firebase_uid.encode('utf-8')[:64],
            user_name=email,
            user_display_name=email.split('@')[0],
            authenticator_selection=authenticator_selection,
        )

        request.session['reg_challenge'] = options.challenge.hex()
        request.session['reg_uid'] = firebase_uid

        return HttpResponse(options_to_json(options), content_type="application/json")
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
def passkey_register_verify_view(request):
    """Step B: Verify and save the newly created passkey to Django."""
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=405)
    try:
        data = json.loads(request.body)
        expected_challenge = request.session.get('reg_challenge')
        firebase_uid = request.session.get('reg_uid')

        if not expected_challenge or not firebase_uid:
            return JsonResponse({"error": "Registration session expired."}, status=400)

        raw_host = request.get_host().split(':')[0]
        rp_id = raw_host if raw_host else "localhost"
        origin = f"https://{request.get_host()}" if "onrender.com" in rp_id else f"http://{request.get_host()}"

        verification = verify_registration_response(
            credential=data,
            expected_challenge=bytes.fromhex(expected_challenge),
            expected_rp_id=rp_id,
            expected_origin=origin,
            require_user_verification=False,
        )

        UserPasskey.objects.update_or_create(
            firebase_uid=firebase_uid,
            defaults={
                'credential_id': base64.urlsafe_b64encode(verification.credential_id).decode('utf-8').rstrip("="),
                'public_key': base64.urlsafe_b64encode(verification.credential_public_key).decode('utf-8').rstrip("="),
                'sign_count': verification.sign_count,
            }
        )

        del request.session['reg_challenge']
        del request.session['reg_uid']

        return JsonResponse({"success": True, "message": "Passkey registered successfully!"})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)

@csrf_exempt
def passkey_challenge_view(request):
    """Step C: Generate login challenge options for the login page."""
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=405)
    try:
        raw_host = request.get_host().split(':')[0]
        rp_id = raw_host if raw_host else "localhost"

        all_passkeys = UserPasskey.objects.all()
        if not all_passkeys.exists():
            return JsonResponse({
                "error": "No passkeys registered yet. Please log in with email and create one in your dashboard first."
            }, 400)

        allow_credentials = [
            {"id": base64.urlsafe_b64decode(pk.credential_id + "=="), "type": "public-key"}
            for pk in all_passkeys
        ]

        options = generate_authentication_options(
            rp_id=rp_id,
            allow_credentials=allow_credentials,
            user_verification=UserVerificationRequirement.PREFERRED,
        )

        request.session['passkey_challenge'] = options.challenge.hex()
        return HttpResponse(options_to_json(options), content_type="application/json")
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
def passkey_verify_view(request):
    """Step D: Verify login assertion and log the user in."""
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=405)
    try:
        data = json.loads(request.body)
        expected_challenge = request.session.get('passkey_challenge')

        if not expected_challenge:
            return JsonResponse({"error": "Challenge expired or missing."}, status=400)

        raw_id_b64 = data.get("id")
        passkey_record = UserPasskey.objects.filter(credential_id=raw_id_b64).first()

        if not passkey_record:
            return JsonResponse({"error": "Passkey not recognized."}, status=404)

        raw_host = request.get_host().split(':')[0]
        rp_id = raw_host if raw_host else "localhost"
        origin = f"https://{request.get_host()}" if "onrender.com" in rp_id else f"http://{request.get_host()}"

        verification = verify_authentication_response(
            query=data,
            expected_challenge=bytes.fromhex(expected_challenge),
            expected_rp_id=rp_id,
            expected_origin=origin,
            credential_public_key=base64.urlsafe_b64decode(passkey_record.public_key + "=="),
            credential_current_sign_count=passkey_record.sign_count,
            require_user_verification=False,
        )

        passkey_record.sign_count = verification.new_sign_count
        passkey_record.save()
        del request.session['passkey_challenge']

        return JsonResponse({
            "success": True,
            "message": "Authenticated!",
            "firebase_uid": passkey_record.firebase_uid,
            "redirect_url": "/client/dashboard/"
        })
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)