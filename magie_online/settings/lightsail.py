import json
import os

import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def get_secret(secret_name):
  region_name = "us-west-2"

  # Create a Secrets Manager client using the assumed role's temporary credentials
  client = boto3.client(
    service_name='secretsmanager',
    region_name=region_name
  )

  try:
    get_secret_value_response = client.get_secret_value(
      SecretId=secret_name
    )
  except (NoCredentialsError, PartialCredentialsError) as e:
    raise Exception('AWS credentials not found') from e
  except client.exceptions.ResourceNotFoundException:
    raise Exception(f'The requested secret {secret_name} was not found')
  except client.exceptions.InvalidRequestException as e:
    raise Exception(f'The request was invalid due to: {e}')
  except client.exceptions.InvalidParameterException as e:
    raise Exception(f'The request had invalid params: {e}')

  # Decrypts secret using the associated KMS key.
  secret = get_secret_value_response['SecretString']
  return secret


# Retrieve secrets
SECRET_KEY = get_secret('prod/magiepuzzles/django_secret_key')

database_credentials = json.loads(get_secret('prod/magiepuzzles/postgresql'))
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': database_credentials['dbname'],
    'USER': database_credentials['username'],
    'PASSWORD': database_credentials['password'],
    'HOST': database_credentials['host'],
    'PORT': database_credentials['port'],
  },
}

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
  'puzzles.magiegame.com',
  'd1ocrz2zrz8geq.cloudfront.net',
  '100.20.81.239',
  'localhost'
]

CSRF_TRUSTED_ORIGINS = [
  'https://magiegame.com',
  'http://magiegame.local:5173',
  'https://puzzles.magiegame.com',
  'https://www.google-analytics.com',
  'https://d1ocrz2zrz8geq.cloudfront.net/'
]

CORS_ALLOWED_ORIGINS = [
  'https://magiegame.com',
  'http://magiegame.local:5173',
  'https://puzzles.magiegame.com',
  'https://100.20.81.239',
  'http://100.20.81.239'
]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

GOOGLE_ANALYTICS_MEASUREMENT_ID = 'G-423DSKKYX5'

# Application definition

INSTALLED_APPS = [
  'django.contrib.admin',
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.messages',
  'corsheaders',
  'puzzles.apps.PuzzlesConfig',
  'rest_framework',
  'char_counter',
  'django.contrib.staticfiles',
  'analytical',
]

MIDDLEWARE = [
  'django.middleware.security.SecurityMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.common.CommonMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'django.middleware.clickjacking.XFrameOptionsMiddleware',
  'corsheaders.middleware.CorsMiddleware'
]

ROOT_URLCONF = 'magie_online.urls'

TEMPLATES = [
  {
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [os.path.join(BASE_DIR, 'templates')]
    ,
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

WSGI_APPLICATION = 'magie_online.wsgi.application'

# Database
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGGING = {
  'version': 1,
  'disable_existing_loggers': False,
  'handlers': {
    'console': {
      'class': 'logging.StreamHandler'
    },
    # 'file': {
    #     'level': 'INFO',
    #     'class': 'logging.FileHandler',
    #     'filename': '/opt/python/log/django.log',
    # },
  },
  'loggers': {
    'root': {
      'handlers': ['console'],
      'level': 'INFO',
      'propagate': True,
    },
  },
}

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
