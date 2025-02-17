"""
Django settings for office_management project.

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


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-kl+0f%9i$80m11ge9*sg4f$81b$(#or%^k&v*o5jo@_0nvm^e&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework.authtoken',
    'django_filters',
    'my_app',
    'my_asset',
    'project_management',
    'rest_framework',
    'accountsAPI',
    'assetsAPI',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'accountsAPI.middlewares.TokenMiddleware',
]

ROOT_URLCONF = 'office_management.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'office_management.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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
# Default setting
AUTHENTICATION_BACKENDS = [
    'my_app.authentication_backends.CustomUserBackend',
    'django.contrib.auth.backends.ModelBackend',  # Default backend
]


AUTH_USER_MODEL = 'my_app.CustomUser'


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
MEDIA_URL='/media/'
MEDIA_ROOT=os.path.join(BASE_DIR,'media')
  
# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# enderers are used to determine how API responses are formatted. If you're working with Django REST Framework (DRF), you can configure different renderers in the settings.py file to support various response formats like JSON, XML, HTML, etc.
# pip install drf-xml
# pip install drf-csv
REST_FRAMEWORK = {
    # 'DEFAULT_RENDERER_CLASSES': [
    #     'rest_framework.renderers.JSONRenderer',  # Default JSON renderer
    #     'rest_framework.renderers.BrowsableAPIRenderer',  # Browsable API renderer
    #     # 'rest_framework.renderers.AdminRenderer',  # Admin-style renderer
    #     # 'rest_framework_xml.renderers.XMLRenderer',  # XML renderer (requires drf-xml)
    #     # 'rest_framework_csv.renderers.CSVRenderer',  # CSV renderer (requires drf-csv)
    #     # 'rest_framework_yaml.renderers.YAMLRenderer', 
    # ],
     'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'rest_framework.authentication.TokenAuthentication',
        'accountsAPI.authentication.CustomTokenAuthentication',  # ✅ Use custom authentication
        'rest_framework.authentication.SessionAuthentication',
    ],
    #  'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.IsAuthenticated',
    # ],
    # for class based throttling implementation
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',  # For unauthenticated users
        'rest_framework.throttling.UserRateThrottle',  # For authenticated users
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '2/minute',  # Unauthenticated users: 5 requests per minute
        'user': '5/minute',  # Authenticated users: 10 requests per minute
    },
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',  # Enables filtering
        'rest_framework.filters.SearchFilter',  # Enables search
        'rest_framework.filters.OrderingFilter',  # Enables ordering
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 'PAGE_SIZE': 3,  # Number of records per page
}
# DJOSER = {
    # 'USER_ID_FIELD':'username', # in user model username is active as primary key
    # 'LOGIN_FIELD': 'email',  # Use email instead of username
    # 'USER_CREATE_PASSWORD_RETYPE': True,  # Require password confirmation
    # 'SEND_ACTIVATION_EMAIL': False,  # Disable email activation
# }
# how use renders in in view 
# from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
# class MyModelViewSet(viewsets.ModelViewSet):
    # queryset = MyModel.objects.all()
    # serializer_class = MyModelSerializer
    # renderer_classes = [JSONRenderer, BrowsableAPIRenderer]  # Override global renderers

# In-Memory Cache (For Development)
#  Pros: Fastest option, as it stores data in memory.
#  Cons: Data is lost when the server restarts.
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
#         'LOCATION': 'user_list_cache',
#     }
# }
# Database Cache (For Production)  ----->  stores cache data in the database.
# Pros: Persistent, survives server restarts.
# Cons: Slightly slower than in-memory cache.
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'user_cache_table',  # Table name in the database
    }
}


