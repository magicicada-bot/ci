# Copyright 2008-2015 Canonical
# Copyright 2015-2018 Chicharreros (https://launchpad.net/~chicharreros)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# For further info, check  http://launchpad.net/magicicada-server

"""Django settings for magicicada project.

Generated by 'django-admin startproject' using Django 1.8.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

import logging
import os
import sys

from psycopg2.extensions import ISOLATION_LEVEL_REPEATABLE_READ


def get_file_content(folder, filename):
    filepath = os.path.join(folder, filename)
    if not os.path.exists(filepath):
        filepath = os.path.join(folder, 'dev-' + filename)

    with open(filepath) as f:
        content = f.read()

    return content


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'keep the secret key used in production secret!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'magicicada.filesync',
    'magicicada.txlog',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'magicicada.urls'

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

WSGI_APPLICATION = 'magicicada.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

PG_HOST = os.environ.get('PG_HOST', '/dev/shm/pg_magicicada')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'filesync',
        'HOST': PG_HOST,
        'USER': 'postgres',
        'OPTIONS': {
            'isolation_level': ISOLATION_LEVEL_REPEATABLE_READ,
        },
    },
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

PASSWORD_VALIDATORS = [
    'UserAttributeSimilarityValidator',
    'MinimumLengthValidator',
    'CommonPasswordValidator',
    'NumericPasswordValidator',
]
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': f'django.contrib.auth.password_validation.{validator}'}
    for validator in PASSWORD_VALIDATORS
]


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

AUTH_USER_MODEL = 'filesync.StorageUser'

# define the TRACE level
TRACE = 5
logging.addLevelName(TRACE, 'TRACE')


class MagicicadaLogger(logging.Logger):
    """Logger that support our custom levels."""

    def trace(self, msg, *args, **kwargs):
        """log at TRACE level"""
        if self.isEnabledFor(TRACE):
            self._log(TRACE, msg, args, **kwargs)


logging.setLoggerClass(MagicicadaLogger)


# Custom settings

APP_NAME = 'filesync'
ENVIRONMENT_NAME = 'development'
INSTANCE_ID = 1

LOG_FOLDER = os.path.join(BASE_DIR, 'tmp')
LOG_FORMAT = '%(asctime)s %(levelname)-8s %(name)s[%(process)d]: %(message)s'
_LOG_HANDLERS = os.getenv('MAGICICADA_LOG_HANDLERS', 'file').split()
_LOG_LEVEL = os.getenv('MAGICICADA_LOG_LEVEL', 'INFO')
if 'trace' in _LOG_HANDLERS:
    _LOG_LEVEL = 'TRACE'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': LOG_FORMAT,
        },
    },
    'handlers': {
        'console': {
            'level': 'TRACE',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'level': 'TRACE',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'encoding': 'utf-8',
            'filename': os.path.join(LOG_FOLDER, 'magicicada.log'),
            'formatter': 'simple',
        },
        'trace': {
            'level': 'TRACE',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'encoding': 'utf-8',
            'filename': os.path.join(LOG_FOLDER, 'magicicada-trace.log'),
            'formatter': 'simple',
        },
        'metrics': {
            'level': 'TRACE',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'encoding': 'utf-8',
            'filename': os.path.join(LOG_FOLDER, 'metrics.log'),
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
        'pyinotify': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
        'magicicada': {
            'handlers': _LOG_HANDLERS,
            'level': _LOG_LEVEL,
            'propagate': False,
        },
        'magicicada.metrics': {
            'handlers': ['metrics'],
            'level': 'INFO',
            'propagate': False,
        },
        'magicicadaclient': {
            'handlers': _LOG_HANDLERS,
            'level': _LOG_LEVEL,
            'propagate': False,
        },
        'magicicadaprotocol': {
            'handlers': _LOG_HANDLERS,
            'level': _LOG_LEVEL,
            'propagate': False,
        },
        # This requires hooking up the PythonLoggingObserver, which we do in
        # the testlib helper to get Twisted's logs when running the suite
        'twisted': {
            'handlers': _LOG_HANDLERS,
            'level': 'INFO',
            'propagate': False,
        },
    },
}

PUBLIC_URL_PREFIX = 'http://some_url'
ROOT_USERVOLUME_NAME = 'Magicicada'
ROOT_USERVOLUME_PATH = '~/' + ROOT_USERVOLUME_NAME
SERVICE_GROUP = 'filesync'
SERVICE_NAME = 'server'
STORAGE_PROXY_PORT = None
SYSLOG_FORMAT = (
    '%(processName)-13s %(levelname)-8s %(name)s[%(process)d]: %(message)s')


# Server settings

API_SERVER_NAME = 'filesync-server'
API_STATUS_PORT = 21102
CERTS_FOLDER = os.path.join(BASE_DIR, 'certs')
# the `crt` key with the content of `cacert.pem` file
CRT = get_file_content(CERTS_FOLDER, 'cacert.pem')
CRT_CHAIN = None
# the `key` key with the content of `privkey.pem` file
CRT_KEY = get_file_content(CERTS_FOLDER, 'privkey.pem')
DELTA_MAX_SIZE = 1000
DISABLE_SSL_COMPRESSION = True
GC_DEBUG = False
GET_FROM_SCRATCH_LIMIT = 2000
GRACEFUL_SHUTDOWN = True
HEARTBEAT_INTERVAL = 5
IDLE_TIMEOUT = 7200
MAGIC_UPLOAD_ACTIVE = True
MAX_DELTA_INFO = 20
PROTOCOL_WEAKREF = False
SSL_LOG_FILENAME = 'ssl-proxy.log'
SSL_PORT = 21101
SSL_SERVER_NAME = 'ssl-proxy'
SSL_STATUS_PORT = 21103
STATS_LOG_INTERVAL = 0
STORAGE_CHUNK_SIZE = 5242880
TCP_PORT = 21100
TRACE_USERS = ['test', 'etc']
UPLOAD_BUFFER_MAX_SIZE = 10485761
STORAGE_BASEDIR = os.path.join(BASE_DIR, 'tmp', 'filestorage')


try:
    from magicicada.settings.local import *  # noqa
except ImportError as err:
    print("WARNING: importing local settings:", err, file=sys.stderr)
