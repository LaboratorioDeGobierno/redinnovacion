"""
Django settings for the project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# standard library
import os
import sys

# django-loginas
from django.core.urlresolvers import reverse_lazy

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))
BASE_DIR = os.path.dirname(PROJECT_DIR)

DATABASES = {
    'default': {
        # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'django.db.backends.postgresql_psycopg2',

        # Or path to database file if using sqlite3.
        'NAME': os.path.basename(os.getcwd()),

        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.

        # Set to empty string for localhost. Not used with sqlite3.
        'HOST': '',
        # Set to empty string for default. Not used with sqlite3.
        'PORT': '',
    }
}

# TEST should be true if we are running python tests
TEST = 'test' in sys.argv

try:
    from local_settings import LOCAL_DEBUG, LOCAL_DATABASES
except:
    DEBUG = True
else:
    DATABASES.update(LOCAL_DATABASES)
    DEBUG = LOCAL_DEBUG

# The email backend to use. For possible shortcuts see django.core.mail.
# The default is to use the SMTP backend.
# Third-party backends can be specified by providing a Python path
# to a module that defines an EmailBackend class.
if TEST:
    EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
elif DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

email_settings = {
    'EMAIL_SENDER_NAME': "Laboratorio ",
    'SENDER_EMAIL': 'correo@XXXX.cl',

    'EMAIL_HOST': '',
    'EMAIL_HOST_USER': '',
    'EMAIL_HOST_PASSWORD': '',
    'EMAIL_PORT': '',
    'ENABLE_EMAILS': False,

    # 'EMAIL_HOST': '',
    # 'EMAIL_HOST_USER': '',
    # 'EMAIL_HOST_PASSWORD': '',
    # 'EMAIL_PORT': '',
    # 'ENABLE_EMAILS': False,
}

try:
    from local_settings import LOCAL_EMAIL_SETTINGS
except:
    # heroku conf
    email_settings.update(os.environ)
else:
    email_settings.update(LOCAL_EMAIL_SETTINGS)

EMAIL_SENDER_NAME = email_settings['EMAIL_SENDER_NAME']
SENDER_EMAIL = email_settings['SENDER_EMAIL']
DEFAULT_FROM_EMAIL = SENDER_EMAIL
SERVER_EMAIL = SENDER_EMAIL

EMAIL_HOST = email_settings['EMAIL_HOST']
EMAIL_HOST_USER = email_settings['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = email_settings['EMAIL_HOST_PASSWORD']
EMAIL_PORT = email_settings['EMAIL_PORT']

ENABLE_EMAILS = email_settings['ENABLE_EMAILS']


# Since we are using our custom user model, we need to set the authentication
# backend to the CustomBackend, so it returns the User model
AUTHENTICATION_BACKENDS = (
    'users.backends.CustomBackend',
)

ADMINS = (
    ('German Mondragon', 'gmondragon@lab.gob.cl.cl'),
    ('Hugo Munoz', 'hmunoz@lab.gob.cl'),
)

MANAGERS = ADMINS


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Santiago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'es'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
    os.path.join(BASE_DIR, 'project/locale_extra'),
)

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/uploads/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static/')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'compressor.finders.CompressorFinder',
)

# SECURITY WARNING: keep the secret key used in production secret!
# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.core.context_processors.debug',
                'django.core.context_processors.i18n',
                'django.core.context_processors.media',
                'django.core.context_processors.static',
                'django.core.context_processors.tz',
                'django.core.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                'users.context_processors.active_users',
                'notifications.context_processors.current_notifications'
            ],
            'loaders': [
                # PyJade part:   ##############################
                ('pyjade.ext.django.Loader', (
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ))
            ]
        },
    },
]

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'users.middleware.UpdateLastActivityMiddleware',
    'users.middleware.PendingUserMiddleware',
)

if DEBUG:
    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

ROOT_URLCONF = 'project.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'project.wsgi.application'

INSTALLED_APPS = (
    'base',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'django.contrib.humanize',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'compressor',
    'users',
    'institutions',
    'activities',
    'events',
    'documents',
    'cases',
    'configs',
    'interests',
    'regions',
    'comments',
    'evaluations',
    'messaging',
    'notifications',
    'newsletters',
    'documentation',
    'dynamic_contents',

    'bootstrap_admin',
    'django.contrib.admin',
    'captcha',
    'easy_thumbnails',
    'bootstrapform',
    'formtools',
    'rest_framework',
    'rest_framework.authtoken',
    'django.contrib.admindocs',
    'phonenumber_field',
    'import_export',
    'platforms',
    'mailing',
    'ckeditor',
    'ckeditor_uploader',
    'django_cron',
    'loginas',
    'robots',
)
# Set the apps that are installed locally
try:
    from local_settings import LOCALLY_INSTALLED_APPS
except:
    pass
else:
    INSTALLED_APPS = INSTALLED_APPS + LOCALLY_INSTALLED_APPS

if DEBUG:
    env = 'development'
else:
    env = 'production'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '{}/logs/{}/error.log'.format(BASE_DIR, env),
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'file'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# set the precompilers for less and jade client templates
COMPRESS_PRECOMPILERS = (
    ('text/less', 'node_modules/less/bin/lessc {infile} > {outfile}'),
    ('text/jade', 'base.filters.jade.JadeCompilerFilter'),
)

COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter',
]

# user loggin
LOGIN_REDIRECT_URL = "/"

# Tuple of IP addresses, as strings, that:
#   * See debug comments, when DEBUG is true
#   * Receive x-headers
INTERNAL_IPS = ('127.0.0.1', '10.0.2.2',)

# Hosts/domain names that are valid for this site.
# "*" matches anything, ".example.com" matches example.com and all subdomains
ALLOWED_HOSTS = [
    'localhost',
    '138.197.130.97',
]

if DEBUG:
    try:
        from local_settings import LOCAL_ALLOWED_HOST
        ALLOWED_HOSTS.append(LOCAL_ALLOWED_HOST)
    except:
        pass

AUTH_USER_MODEL = 'users.User'

# default keys, replace with somethign your own
RECAPTCHA_PUBLIC_KEY = 'place recaptcha public key here'
RECAPTCHA_PRIVATE_KEY = 'place recaptcha private key here'
NOCAPTCHA = True
# un comment when we start using only SSL
# RECAPTCHA_USE_SSL = True

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.DjangoFilterBackend',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

EMAIL_HOST = ''#'smtp.gmail.com'
EMAIL_HOST_USER = ''#'la cuenta@xx.cl'
EMAIL_HOST_PASSWORD = ''#'lacontrasenna'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# ckeditor path & backend
CKEDITOR_UPLOAD_PATH = ''
CKEDITOR_IMAGE_BACKEND = "pillow"


# mailchimp
#Configuraciones para Mailchimp
try:
    from local_settings import LOCAL_MAILCHIMP_API_KEY
    MAILCHIMP_API_KEY = LOCAL_MAILCHIMP_API_KEY
except:
    MAILCHIMP_API_KEY = ''##'token-mailchimp'

MAILCHIMP_API_SERVER = MAILCHIMP_API_KEY.split('-')[-1]
MAILCHIMP_API_BASE_URL = (
    'https://{}.api.mailchimp.com/3.0/'.format(
        MAILCHIMP_API_SERVER
    )
)

MAILCHIMP_CONTACT_DICT = {
    'company': 'Nombre Compania',
    'address1': 'Direccion 1',
    'address2': 'Direccion 2',
    'city': 'Ciudad',
    'state': 'Estado',
    'zip': '0000001',
    'country': 'Pais',
    'phone': 'phone',
}

MAILCHIMP_CAMPAIGN_DEFAULTS = {
    'from_name': 'Laboratorio ',
    'from_email': 'contacto@XXXXXX.cl',
    'language': 'spanish',
}

MAILCHIMP_PERMISSION_REMINDER = (
    'Hemos obtenido su email porque pertenece a labgob'
)

MAILCHIMP_EMAIL_OPTION = True

MAILCHIMP_CAMPAIGN_TYPE = 'regular'

MAILCHIMP_CAMPAIGN_SETTINGS = {
    'title': 'Default - ',
    'from_name': 'Laboratorio',
    'reply_to': 'contacto@XXXX.cl',
}

# django_cron
CRON_CLASSES = [
    "mailing.cron.ScheduleMailingCronJob",
    "notifications.cron.NotifyIncomingEventCronJob",
    "newsletters.cron.NewsletterMailingCronJob",
]


LOGOUT_URL = reverse_lazy('loginas-logout')
LOGINAS_REDIRECT_URL = LOGIN_REDIRECT_URL
LOGINAS_LOGOUT_REDIRECT_URL = reverse_lazy('admin:index')


def CAN_LOGIN_AS(request, target_user):
    return request.user.is_superuser and not target_user.is_superuser


# thumbnails
THUMBNAIL_ALIASES = {
    '': {
        'small': {'size': (400, 400), 'crop': True},
        'small_no_crop': {'size': (400, 400), 'crop': False},
        'smaller': {'size': (200, 200), 'crop': False},
        'tiny': {'size': (100, 100), 'crop': False},
    },
}
