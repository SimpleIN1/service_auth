"""
Django settings for AccountsProject project.

Generated by 'django-admin startproject' using Django 4.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')
ACCESS_SECRET_KEY = os.getenv('ACCESS_SECRET_KEY')
REFRESH_SECRET_KEY = os.getenv('REFRESH_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = (bool(int(os.environ.get('DEBUG', 1))))

ALLOWED_HOSTS = ['*']

AUTH_USER_MODEL = 'AccountsApp.User'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'corsheaders',
    'cacheops',

    'AccountsApp.apps.AccountsAppConfig',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'AccountsApp.middleware.DisableCSRFMiddleware.DisableCSRFMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',
]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'http')

CSRF_TRUSTED_ORIGINS = ['http://0.0.0.0:8080', 'http://10.4.47.53:8080', 'https://fam.rcpod.space:443']

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

ROOT_URLCONF = 'AccountsProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'AccountsApp/templates')],
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

WSGI_APPLICATION = 'AccountsProject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('NAME_DB'),
        'USER': os.getenv('USER_DB'),
        'PASSWORD': os.getenv('PASSWORD_DB'),
        'HOST': os.getenv('HOST_DB'),
        'PORT': os.getenv('PORT_DB'),
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS')
EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')

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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'AccountsApp.services.authentication.RemoteUserAuthentication',
        'AccountsApp.services.auth.authentication.JWTAuthentication',
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',
        # 'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        # 'rest_framework.permissions.IsAuthenticated',
    ),
}

if not DEBUG:
    REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = (
            # "rest_framework.renderers.JSONRenderer",
            "drf_orjson_renderer.renderers.ORJSONRenderer",
        )


AUTHENTICATION_BACKENDS = [
    'AccountsApp.services.authentication.CustomModelBackend',
     # 'django.contrib.auth.backends.RemoteUserBackend',
     #'django.contrib.auth.backends.ModelBackend',
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


ACCOUNT_AUTHENTICATION_METHOD = 'email'
USERNAME_FIELD = 'email'
ACCOUNT_EMAIL_REQUIRED = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static-admin/'
MEDIA_URL = '/media/'
#MEDIA_ROOT = os.path.join(BASE_DIR, 'files')
STATIC_ROOT = os.path.join(BASE_DIR, 'static-admin')
# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# CORS
CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
)
CORS_ALLOW_METHODS = ['DELETE', 'GET', 'OPTIONS', 'PATCH', 'POST', 'PUT']
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = [
    'https://fam.rcpod.space:443',
]

#Cashing
CACHEOPS = {
    'AccountsApp.*': {
        'ops': 'all',
        'timeout': 60*15,
    },
    '*.*': {
        'timeout': 60*15,
    }
}
CACHEOPS_REDIS = os.getenv('CELERY_BROKER_URL', 'redis://127.0.0.1:6379/3')


#Logging for sql
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console'],
        }
    },
}

ERRORS = {
    # user_error
    'user_error': {
        '1': 'Некорректный электронный адрес или пароль.',#'Пользователь не найден.',
        '2': 'Старый пароль некорректный.',
        '3': 'Почта не подтверждена. Вам отправлено письмо с подтверждением на почту',
        '4': 'Пользователь не найден или удален.',
    },

    # user info
    'user_info': {
        '5': 'Пароль уже измен.',
        '6': 'Почта уже подтверждена.',
        '7': 'Пароль успешно изменен', #'Восстановление пароля прошло успешно.',
        '8': 'Почта подтверждена.',
        '9': 'Для подтверждения почты вам отправлено письмо на электронный адрес, который был указан при регистрации.',
        '10': 'Для сброса пароля вам отправлено письмо на электронный адрес, который был указан.',
        '11': 'Данные обновлены.',
        '12': 'Аккаунт восстановлен',
        '13': 'Для восстановления учетной записи вам отправлено письмо на электронный адрес, который был указан.',
    },

    # token error
    'token_error': {
        '14': 'Токен не правильный.',
        '15': 'Действие токена закончилось.',
        '16': 'Токен не валидный с ошибкой раскодировки.',
    },

    'available_tmp_error': {
        '17': 'Невозможно выполнить операцию',
    },

    # fields error
    'fields_error': {
        '18': 'Обязательные поля не преданы или не прошли валидацию',
        '19': 'Пользователь с этим адресом электронной почты уже существует.',
    },
    'auth_error': {
        '20': 'Учетные данные не были предоставлены.'
    },
    'file_info': {
        '1': 'Данных нет.',
    },
    'user_access': {
        '2': 'Пользователю предоставлен доступ.',
    }
}

PROTOCOL = 'https'
HOST = 'fam.rcpod.space'#
PORT = '443'
URL_PAGE = {
    'email_verify': 'url1',
    'reset_password': 'restore_password',
    'recovery_account': 'url1',
    'url_for_access_client': 'api/auth/access_client/',
}

PASSWORD_RESET_TIMEOUT = 60 * 60 * 24 * 10

CONTENT_TYPE = {
    'application/vnd.oasis.opendocument.text': 'odt',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'docx',
    'application/pdf': 'pdf',
    'application/msword': 'doc',
}
