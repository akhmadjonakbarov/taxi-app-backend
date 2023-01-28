from datetime import timedelta
from pathlib import Path
from os.path import join as joinpath
from rest_framework.settings import api_settings


BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'django-insecure-_d#)wd6eda)vwdc9m@s)qxw46+j2ngfwxh6dcnpu#umawv3763'

DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # my apps
    'userapp.apps.UserappConfig',
    'serviceapp.apps.ServiceappConfig',
    'carapp.apps.CarappConfig',
    # other apps
    'rest_framework',
    'knox',
    'corsheaders.apps.CorsHeadersAppConfig',
]

AUTH_USER_MODEL = 'userapp.CustomUser'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'knox.auth.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

REST_KNOX = {
    'SECURE_HASH_ALGORITHM': 'cryptography.hazmat.primitives.hashes.SHA512',
    # By default, it is set to 64 characters (this shouldn't need changing).
    'AUTH_TOKEN_CHARACTER_LENGTH': 64,
    # The default is 10 hours i.e., timedelta(hours=10)).
    'TOKEN_TTL': timedelta(minutes=45),
    'USER_SERIALIZER': 'api.serializers.CustomUserSerializer',
    # By default, this option is disabled and set to None -- thus no limit.
    'TOKEN_LIMIT_PER_USER': None,
    # This defines if the token expiry time is extended by TOKEN_TTL each time the token is used.
    'AUTO_REFRESH': False,
    'EXPIRY_DATETIME_FORMAT': api_settings.DATETIME_FORMAT,
}


# CSRF_COOKIE_DOMAIN = '*'
#
# CSRF_TRUSTED_ORIGINS = ['*']
#
# CORS_ALLOWED_ORIGINS = ['*']
#
# CORS_ALLOW_METHODS = [
#     "DELETE",
#     "GET",
#     "OPTIONS",
#     "PATCH",
#     "POST",
#     "PUT",
# ]
#
# CORS_ORIGIN_WHITELIST = (
#
#     '*'
# )

ROOT_URLCONF = 'taxistartup.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'taxistartup.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
# MEDIA_URL = '/images/'
MEDIA_URL = ''

STATICFILES_DIRS = [
    BASE_DIR / 'statics'
]

MEDIA_ROOT = joinpath(BASE_DIR, 'statics/images')

STATIC_ROOT = joinpath(BASE_DIR, 'staticfiles')



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
