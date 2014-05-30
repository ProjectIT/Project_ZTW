"""
Django settings for tasker project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

# https://docs.djangoproject.com/en/dev/intro/tutorial01/
# http://www.jetbrains.com/pycharm/quickstart/
# python manage.py runserver to start the server



# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@l-w#vjv%&tn84e8ih%w-2rmx!8*)dp@1q!(16gd-npwh8-d=u'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
	'projects'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'tasker.urls'

WSGI_APPLICATION = 'tasker.wsgi.application'


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
}
'''
	'mysql': {
		'ENGINE': 'django.db.backends.mysql',
		'NAME': 'django_test',
		'USER': 'root',
		'PASSWORD': '',
		'HOST': '127.0.0.1',
		'PORT': '3306',
	}
'''

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'

# TEMPLATE_LOADERS = (
#     'django.template.loaders.filesystem.Loader',
#     'django.template.loaders.app_directories.Loader',
# )
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "templates"),
	os.path.join(BASE_DIR, "tasker", "templates"),
	os.path.join(BASE_DIR, "projects","templates"),
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
	os.path.join(BASE_DIR, "tasker", "static"),
	os.path.join(BASE_DIR, "projects","static"),
)

AUTH_PROFILE_MODULE = 'projects.UserProfile'