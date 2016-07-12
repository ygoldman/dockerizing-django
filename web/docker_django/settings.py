from configurations import Configuration, values
import logging, logging.handlers
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))


class Internationalization(object):
    LANGUAGE_CODE = 'en-us'
    TIME_ZONE = 'UTC'
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True


class Base(Internationalization, Configuration):
    DEBUG = values.BooleanValue(default=False)
    SECRET_KEY = values.Value(environ_required=True)
    ROOT_URLCONF = values.Value(default='docker_django.urls')

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'simple'
            },
            'file': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': '/var/log/django/django.log',
                'maxBytes': 1024*1024*15, # 15MB
                'backupCount': 10,
                'formatter': 'verbose'
            },
        },
        'loggers': {
            'django': {
                'handlers': ['console','file'],
                'level': values.Value(default='DEBUG', environ_name='LOG_LEVEL'),
                'propagate': True,
            },
        },
    }

    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        # apps
        'docker_django.apps.drdjango',
    )

    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'django.middleware.security.SecurityMiddleware',
    )

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

    WSGI_APPLICATION = 'docker_django.wsgi.application'
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')


class Dev(Base):
    ALLOWED_HOSTS = ['*']
    DEBUG = values.BooleanValue(default=True)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['DB_NAME'],
            'USER': os.environ['DB_USER'],
            'PASSWORD': os.environ['DB_PASS'],
            'HOST': os.environ['DB_SERVICE'],
            'PORT': os.environ['DB_PORT']
        }
    }

    @classmethod
    def post_setup(cls):
        super(Dev, cls).post_setup()
        logging.info("Dev settings configured! \o/")


class Test(Dev):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['DB_NAME'],
            'USER': os.environ['DB_USER'],
            'PASSWORD': os.environ['DB_PASS'],
            'HOST': os.environ['DB_SERVICE'],
            'PORT': os.environ['DB_PORT']
        }
    }


class Prod(Base):
    ALLOWED_HOSTS = ['*']
    DEBUG = False

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': '/var/log/django/django.log',
                'maxBytes': 1024*1024*15, # 15MB
                'backupCount': 10,
                'formatter': 'verbose'
            },
        },
        'loggers': {
            'django': {
                'handlers': ['console','file'],
                'level': values.Value(default='INFO', environ_name='LOG_LEVEL'),
                'propagate': True,
            },
        },
    }

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['DB_NAME'],
            'USER': os.environ['DB_USER'],
            'PASSWORD': os.environ['DB_PASS'],
            'HOST': os.environ['DB_SERVICE'],
            'PORT': os.environ['DB_PORT']
        }
    }

