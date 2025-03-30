"""
Django settings for Ecommerce project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR= os.path.join(BASE_DIR,'templates')



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-f0-#4599@c&!&4(d46j=6st08$*+r$@dy7fqu2a8izhpg#(ly@'

RAZORPAY_API_KEY = 'rzp_test_MAimzLa32DUYt6 '
RAZORPAY_API_SECRET = 'qbDDZBXaEQPNG72T9ZPVPytC'



PAYPAL_CLIENT_ID = 'AUIZsWRO2Snvs5c55uP7Zpx8ROSc-TSAwfAGtXrAwXu8gz3dl_lVjzAKDfLgPL0r0f4bb7URRTbTUlHA'
PAYPAL_SECRET = 'EOyoBk9CPLjDvinZfn1531ZsDDTCugVYI-MywCCQKdeS_ArvEYvyqumZMZF3DEcabqlX8Bsjiqd3XUBD'


# To Enable Popus in Django or else it will block the payment popup
SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin-allow-popups"



# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['woodora.live', 'www.woodora.live', '3.108.63.103']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google', 
    "corsheaders",  
    'products',
    'home',
    'custom_admin',
    'payment',
    
]






EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'jayasrees317@gmail.com'  
EMAIL_HOST_PASSWORD = 'lonf kdqd biao hrhs'  
DEFAULT_FROM_EMAIL = 'jayasrees317@gmail.com'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'allauth.account.middleware.AccountMiddleware',
    'products.middleware.CouponMiddleware',
]


SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_by_email',  # Auto-match by email
    'social_core.pipeline.user.create_user',  # Auto-create user
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)


CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:8000",  # Allow Django local server
    "http://localhost:8000",
]

CORS_ALLOW_CREDENTIALS = True   


CSRF_TRUSTED_ORIGINS = ['https://woodora.live', 'https://www.woodora.live']
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = True  # Redirect HTTP to HTTPS
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True



ROOT_URLCONF = 'Ecommerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/"templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'home.context_processors.breadcrumbs',
            ],
        },
    },
]

WSGI_APPLICATION = 'Ecommerce.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
  "default": {
     "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
        "USER": 'admin',
        "PASSWORD": "idhal@19#2022",
        "HOST": 'woodora-ecommerce.c5iaosgak9m1.ap-south-1.rds.amazonaws.com'
     }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS=[
    os.path.join(BASE_DIR,'static')

]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]


SOCIALACCOUNT_AUTO_SIGNUP = True

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': '318951295751-dvhj4hrmos37mmbn3c9las9mjphtr042.apps.googleusercontent.com',
            'secret': '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',

            'key': ''
        },
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'OAUTH_PKCE_ENABLED': True,
    }
}
SITE_ID = 1
LOGIN_REDIRECT_URL = '/index/'
LOGIN_REDIRECT_URL = 'index'
# ACCOUNT_SIGNUP_REDIRECT_URL = '/index/' 
SOCIALACCOUNT_LOGIN_ON_GET = True

#487195215093-9ppt8n6uif5iemtpe3cblkjpvlhvvqij.apps.googleusercontent.com
