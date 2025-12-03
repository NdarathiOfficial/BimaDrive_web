"""
Django settings for Bimadrive project.
"""

from pathlib import Path

# ===============================
# BASE DIRECTORY
# ===============================
BASE_DIR = Path(__file__).resolve().parent.parent


# ===============================
# SECURITY SETTINGS
# ===============================
SECRET_KEY = 'django-insecure-2!tsk1f4##n&w0av38)qumhb*)&2@ls_*(z*x_wu1*we&8_)in'
DEBUG = True
ALLOWED_HOSTS = []  # Add production hostnames here


# ===============================
# APPLICATIONS
# ===============================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_daraja',

    # Your app
    'Website',
]


# ===============================
# MIDDLEWARE
# ===============================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ===============================
# URL CONFIGURATION
# ===============================
ROOT_URLCONF = 'Bimadrive.urls'


# ===============================
# TEMPLATES
# ===============================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],  # Global templates folder
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# ===============================
# WSGI
# ===============================
WSGI_APPLICATION = 'Bimadrive.wsgi.application'


# ===============================
# DATABASE
# ===============================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ===============================
# PASSWORD VALIDATION
# ===============================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ===============================
# INTERNATIONALIZATION
# ===============================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# ===============================
# STATIC FILES
# ===============================
STATIC_URL = '/static/'

# Serve static files during development
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Where static files will be collected in production
STATIC_ROOT = BASE_DIR / "staticfiles"


# ===============================
# MEDIA FILES (optional)
# ===============================
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ===============================
# DEFAULT PRIMARY KEY FIELD TYPE
# ===============================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ===============================
# CUSTOM USER MODEL
# ===============================
AUTH_USER_MODEL = 'Website.User'  # Your custom user model


# ===============================
# LOGIN SETTINGS
# ===============================
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/client/'
LOGOUT_REDIRECT_URL = '/login/'


MPESA_ENVIRONMENT='sandbox'
MPESA_CONSUMER_KEY = 'dyTusM791Kz6ATVyQaFlBlk6c2aQpBapNPPVV7unePSMeoAH'
MPESA_CONSUMER_SECRET = 'cd0FXES2ZugdDk5zVqlUtqSDdccUzVBsR05ES5v4KurC7P5BQMX2vYanuylWaW13'
MPESA_SHORTCODE='174379'
MPESA_EXPRESS_SHORTCODE='174379'
MPESA_SHORTCODE_TYPE='paybill'
MPESA_PASSKEY='bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
MPESA_INITIATOR_USERNAME='testapi'
MPESA_INITIATOR_SECURITY_CREDENTIALS='Safaricom123!!'