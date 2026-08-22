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

import base64
import json
import logging

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

import firebase_admin
from firebase_admin import auth as firebase_auth

from webauthn import (
    generate_registration_options,
    verify_registration_response,
    generate_authentication_options,
    verify_authentication_response,
    options_to_json,
)

from webauthn.helpers.structs import (
    AuthenticatorSelectionCriteria,
    AuthenticatorAttachment,
    ResidentKeyRequirement,
    UserVerificationRequirement,
    PublicKeyCredentialDescriptor,
    RegistrationCredential,
)

from .models import UserPasskey




from webauthn import (
    generate_authentication_options,
    verify_authentication_response,
    options_to_json,
)

from webauthn.helpers.structs import (
    PublicKeyCredentialDescriptor,
    UserVerificationRequirement,)

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


from django.http import JsonResponse, HttpResponse
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


# ============================================================
# WEB AUTHN CONFIGURATION
# ============================================================

def get_webauthn_config(request):
    """
    Returns:

        rp_id
        origin

    for the current host.
    """

    host = request.get_host().split(":")[0].lower()

    # LOCAL DEVELOPMENT
    if host in ("localhost", "127.0.0.1"):

        return (
            "localhost",
            f"http://{request.get_host()}"
        )

    # PRODUCTION
    return (
        host,
        f"https://{request.get_host()}"
    )


# ============================================================
# BASE64URL HELPERS
# ============================================================

def base64url_encode(data):
    """
    Convert bytes -> Base64URL without padding.
    """

    return base64.urlsafe_b64encode(
        data
    ).decode("utf-8").rstrip("=")


def base64url_decode(data):
    """
    Convert Base64URL -> bytes.
    """

    if not data:
        return b""

    padding = "=" * (-len(data) % 4)

    return base64.urlsafe_b64decode(
        data + padding
    )


# ============================================================
# PASSKEY REGISTRATION - STEP A
# ============================================================

@csrf_exempt
def passkey_register_options_view(request):

    if request.method != "POST":

        return JsonResponse(
            {
                "error": "Invalid request method."
            },
            status=405
        )

    try:

        data = json.loads(
            request.body.decode("utf-8")
        )

        firebase_uid = data.get("uid")
        email = data.get(
            "email",
            "user@bimadrive.com"
        )

        if not firebase_uid:

            return JsonResponse(
                {
                    "error": (
                        "Firebase UID is required."
                    )
                },
                status=400
            )

        # ----------------------------------------------------
        # WebAuthn configuration
        # ----------------------------------------------------

        rp_id, origin = get_webauthn_config(
            request
        )

        # ----------------------------------------------------
        # User ID
        # ----------------------------------------------------

        user_id = firebase_uid.encode(
            "utf-8"
        )[:64]

        # ----------------------------------------------------
        # Authenticator requirements
        # ----------------------------------------------------

        authenticator_selection = (
            AuthenticatorSelectionCriteria(
                authenticator_attachment=(
                    AuthenticatorAttachment.PLATFORM
                ),

                resident_key=(
                    ResidentKeyRequirement.REQUIRED
                ),

                user_verification=(
                    UserVerificationRequirement.PREFERRED
                ),
            )
        )

        # ----------------------------------------------------
        # Prevent same credential from being registered twice
        # ----------------------------------------------------

        existing_passkeys = (
            UserPasskey.objects.filter(
                firebase_uid=firebase_uid
            )
        )

        exclude_credentials = []

        for passkey in existing_passkeys:

            credential_bytes = base64url_decode(
                passkey.credential_id
            )

            exclude_credentials.append(
                PublicKeyCredentialDescriptor(
                    id=credential_bytes
                )
            )

        # ----------------------------------------------------
        # Generate registration options
        # ----------------------------------------------------

        options = generate_registration_options(

            rp_id=rp_id,

            rp_name="BimaDrive Insurance",

            user_id=user_id,

            user_name=email,

            user_display_name=(
                email.split("@")[0]
            ),

            authenticator_selection=(
                authenticator_selection
            ),

            exclude_credentials=(
                exclude_credentials
            ),
        )

        # ----------------------------------------------------
        # Save challenge in session
        # ----------------------------------------------------

        request.session[
            "passkey_registration_challenge"
        ] = options.challenge.hex()

        request.session[
            "passkey_registration_uid"
        ] = firebase_uid

        request.session[
            "passkey_registration_rp_id"
        ] = rp_id

        request.session[
            "passkey_registration_origin"
        ] = origin

        request.session.modified = True

        logger.info(
            "Generated passkey registration challenge for %s",
            firebase_uid
        )

        return HttpResponse(
            options_to_json(options),
            content_type="application/json"
        )

    except Exception as e:

        logger.error(
            "Passkey registration options error: %s",
            str(e),
            exc_info=True
        )

        return JsonResponse(
            {
                "error": str(e)
            },
            status=400
        )


# ============================================================
# PASSKEY REGISTRATION - STEP B
# ============================================================

@csrf_exempt
def passkey_register_verify_view(request):
    """Step B: Verify and save the newly created passkey to Django."""
    if request.method != "POST":
        return JsonResponse(
            {
                "error": "Invalid request method."
            },
            status=405
        )

    try:
        data = json.loads(request.body.decode("utf-8"))

        # ----------------------------------------------------
        # Get challenge
        # ----------------------------------------------------

        expected_challenge = request.session.get(
            "passkey_registration_challenge"
        )

        firebase_uid = request.session.get(
            "passkey_registration_uid"
        )

        rp_id = request.session.get(
            "passkey_registration_rp_id"
        )

        origin = request.session.get(
            "passkey_registration_origin"
        )

        if not expected_challenge:
            return JsonResponse(
                {
                    "success": False,
                    "error": "Registration challenge expired or missing."
                },
                status=400
            )

        if not firebase_uid:
            return JsonResponse(
                {
                    "success": False,
                    "error": "Firebase user identity is missing."
                },
                status=400
            )

        if not rp_id or not origin:
            rp_id, origin = get_webauthn_config(request)

        # ----------------------------------------------------
        # Verify registration passing the decoded dictionary directly
        # ----------------------------------------------------

        verification = verify_registration_response(
            credential=data,
            expected_challenge=bytes.fromhex(expected_challenge),
            expected_rp_id=rp_id,
            expected_origin=origin,
            require_user_verification=False,
        )

        # ----------------------------------------------------
        # Encode credential ID
        # ----------------------------------------------------

        credential_id = base64url_encode(
            verification.credential_id
        )

        # ----------------------------------------------------
        # Encode public key
        # ----------------------------------------------------

        public_key = base64url_encode(
            verification.credential_public_key
        )

        # ----------------------------------------------------
        # Save passkey
        # ----------------------------------------------------

        UserPasskey.objects.update_or_create(
            credential_id=credential_id,
            defaults={
                "firebase_uid": firebase_uid,
                "public_key": public_key,
                "sign_count": verification.sign_count,
            }
        )

        # ----------------------------------------------------
        # Clear registration session
        # ----------------------------------------------------

        request.session.pop("passkey_registration_challenge", None)
        request.session.pop("passkey_registration_uid", None)
        request.session.pop("passkey_registration_rp_id", None)
        request.session.pop("passkey_registration_origin", None)
        request.session.modified = True

        logger.info("Passkey registered successfully for %s", firebase_uid)

        return JsonResponse(
            {
                "success": True,
                "message": "Passkey registered successfully.",
                "credential_id": credential_id,
            }
        )

    except Exception as e:
        logger.error(
            "PASSKEY REGISTRATION ERROR: %s",
            str(e),
            exc_info=True
        )

        return JsonResponse(
            {
                "success": False,
                "error": str(e)
            },
            status=400
        )

# ============================================================

@csrf_exempt
def passkey_challenge_view(request):

    if request.method != "POST":

        return JsonResponse(
            {
                "error": "Invalid request method."
            },
            status=405
        )

    try:

        # ----------------------------------------------------
        # WebAuthn configuration
        # ----------------------------------------------------

        rp_id, origin = get_webauthn_config(
            request
        )

        # ----------------------------------------------------
        # Get all registered passkeys
        # ----------------------------------------------------

        passkeys = UserPasskey.objects.all()

        if not passkeys.exists():

            return JsonResponse(
                {
                    "error": (
                        "No passkeys are registered. "
                        "Please sign in normally first "
                        "and register a passkey."
                    )
                },
                status=400
            )

        # ----------------------------------------------------
        # Build allowed credentials
        # ----------------------------------------------------

        allow_credentials = []

        for passkey in passkeys:

            credential_id = base64url_decode(
                passkey.credential_id
            )

            allow_credentials.append(
                PublicKeyCredentialDescriptor(
                    id=credential_id
                )
            )

        # ----------------------------------------------------
        # Generate authentication options
        # ----------------------------------------------------

        options = generate_authentication_options(

            rp_id=rp_id,

            allow_credentials=(
                allow_credentials
            ),

            user_verification=(
                UserVerificationRequirement.PREFERRED
            ),
        )

        # ----------------------------------------------------
        # Store challenge
        # ----------------------------------------------------

        request.session[
            "passkey_authentication_challenge"
        ] = options.challenge.hex()

        request.session[
            "passkey_authentication_rp_id"
        ] = rp_id

        request.session[
            "passkey_authentication_origin"
        ] = origin

        request.session.modified = True

        logger.info(
            "Generated passkey authentication challenge"
        )

        return HttpResponse(
            options_to_json(options),
            content_type="application/json"
        )

    except Exception as e:

        logger.error(
            "Passkey challenge error: %s",
            str(e),
            exc_info=True
        )

        return JsonResponse(
            {
                "error": str(e)
            },
            status=400
        )


# ============================================================
# PASSKEY LOGIN - STEP D
# ============================================================

@csrf_exempt
def passkey_verify_view(request):

    if request.method != "POST":

        return JsonResponse(
            {
                "error": "Invalid request method."
            },
            status=405
        )

    try:

        # ----------------------------------------------------
        # Receive browser assertion
        # ----------------------------------------------------

        raw_body = request.body
        data = json.loads(
            raw_body.decode("utf-8")
        )

        logger.info(
            "Received WebAuthn authentication response."
        )

        # ----------------------------------------------------
        # Validate basic WebAuthn structure
        # ----------------------------------------------------

        required_fields = [
            "id",
            "rawId",
            "type",
            "response",
        ]

        missing_fields = [
            field
            for field in required_fields
            if field not in data
        ]

        if missing_fields:

            return JsonResponse(
                {
                    "success": False,
                    "error": (
                        "Invalid WebAuthn response. "
                        "Missing fields: "
                        + ", ".join(
                            missing_fields
                        )
                    )
                },
                status=400
            )

        # ----------------------------------------------------
        # Get challenge
        # ----------------------------------------------------

        expected_challenge = request.session.get(
            "passkey_authentication_challenge"
        )

        rp_id = request.session.get(
            "passkey_authentication_rp_id"
        )

        origin = request.session.get(
            "passkey_authentication_origin"
        )

        if not expected_challenge:

            return JsonResponse(
                {
                    "success": False,
                    "error": (
                        "Passkey challenge expired "
                        "or missing. Please try again."
                    )
                },
                status=400
            )

        if not rp_id or not origin:

            rp_id, origin = (
                get_webauthn_config(request)
            )

        # ----------------------------------------------------
        # Browser credential ID
        # ----------------------------------------------------

        credential_id = data.get("id")

        if not credential_id:

            return JsonResponse(
                {
                    "success": False,
                    "error": (
                        "Credential ID is missing."
                    )
                },
                status=400
            )

        # ----------------------------------------------------
        # IMPORTANT:
        #
        # Make sure id == base64url(rawId)
        #
        # ----------------------------------------------------

        raw_id = data.get("rawId")

        if not raw_id:

            return JsonResponse(
                {
                    "success": False,
                    "error": (
                        "rawId is missing."
                    )
                },
                status=400
            )

        if credential_id != raw_id:

            return JsonResponse(
                {
                    "success": False,
                    "error": (
                        "Credential ID does not match "
                        "rawId."
                    )
                },
                status=400
            )

        # ----------------------------------------------------
        # Find passkey in database
        # ----------------------------------------------------

        passkey_record = (
            UserPasskey.objects
            .filter(
                credential_id=credential_id
            )
            .first()
        )

        if not passkey_record:

            logger.warning(
                "Unknown passkey attempted: %s",
                credential_id
            )

            return JsonResponse(
                {
                    "success": False,
                    "error": (
                        "This passkey is not registered "
                        "with BimaDrive."
                    )
                },
                status=404
            )

        # ----------------------------------------------------
        # Decode stored public key
        # ----------------------------------------------------

        credential_public_key = (
            base64url_decode(
                passkey_record.public_key
            )
        )

        # ----------------------------------------------------
        # VERIFY WEBAUTHN
        # ----------------------------------------------------

        verification = (
            verify_authentication_response(

                credential=data,

                expected_challenge=(
                    bytes.fromhex(
                        expected_challenge
                    )
                ),

                expected_rp_id=rp_id,

                expected_origin=origin,

                credential_public_key=(
                    credential_public_key
                ),

                credential_current_sign_count=(
                    passkey_record.sign_count
                ),

                require_user_verification=True,
            )
        )

        # ----------------------------------------------------
        # Update authenticator counter
        # ----------------------------------------------------

        passkey_record.sign_count = (
            verification.new_sign_count
        )

        passkey_record.save(
            update_fields=[
                "sign_count"
            ]
        )

        # ----------------------------------------------------
        # Clear challenge
        # ----------------------------------------------------

        request.session.pop(
            "passkey_authentication_challenge",
            None
        )

        request.session.pop(
            "passkey_authentication_rp_id",
            None
        )

        request.session.pop(
            "passkey_authentication_origin",
            None
        )

        request.session.modified = True

        # ----------------------------------------------------
        # Firebase custom authentication token
        # ----------------------------------------------------

        firebase_uid = (
            passkey_record.firebase_uid
        )

        try:

            firebase_token = (
                firebase_auth.create_custom_token(
                    firebase_uid
                )
            )

            if isinstance(
                firebase_token,
                bytes
            ):

                firebase_token = (
                    firebase_token.decode("utf-8")
                )

        except Exception as firebase_error:

            logger.error(
                "Firebase custom token error: %s",
                str(firebase_error),
                exc_info=True
            )

            return JsonResponse(
                {
                    "success": False,
                    "error": (
                        "Passkey verified, but "
                        "Firebase authentication "
                        "could not be completed."
                    )
                },
                status=500
            )

        # ----------------------------------------------------
        # SUCCESS
        # ----------------------------------------------------

        logger.info(
            "Passkey authentication successful "
            "for Firebase UID %s",
            firebase_uid
        )

        return JsonResponse(
            {
                "success": True,

                "message": (
                    "Passkey verified successfully."
                ),

                "firebase_uid": firebase_uid,

                "firebase_token": firebase_token,

                "redirect_url": (
                    "/client/dashboard/"
                ),
            }
        )

    except Exception as e:

        logger.error(
            "PASSKEY AUTHENTICATION ERROR: %s",
            str(e),
            exc_info=True
        )

        return JsonResponse(
            {
                "success": False,
                "error": str(e)
            },
            status=400
        )