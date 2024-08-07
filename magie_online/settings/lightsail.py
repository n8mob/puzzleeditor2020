import os
import boto3
import json
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def assume_role(role_arn, session_name):
    sts_client = boto3.client('sts')
    response = sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName=session_name
    )
    credentials = response['Credentials']
    return credentials


def get_secret(secret_name):
    region_name = "us-west-2"
    secret_role_arn = 'arn:aws:iam::118653355254:role/MAGiE-Puzzles-Role'
    session_name = 'magie_puzzles_session'

    # Assume the role
    credentials = assume_role(secret_role_arn, session_name)

    # Create a Secrets Manager client using the assumed role's temporary credentials
    client = boto3.client(
        service_name='secretsmanager',
        region_name=region_name,
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken']
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
    'puzzleeditor2020-dev.us-west-2.elasticbeanstalk.com',
    'magie-editor.us-west-2.elasticbeanstalk.com',
]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'puzzles.apps.PuzzlesConfig',
    'rest_framework',
    'char_counter',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'magie_online.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, '../../templates')]
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

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

STATIC_URL = '/static/'