# Django SaaS Framework

Django Saas Framework simplifies building SaaS apps. It has models, serializers and views that make
it easy to build a B2B SaaS application APIs.

Warning: This is under active development and is not ready for production use. Needs a bunch
of documentation as well.

## Quick start

Add the following to your Django project's settings.py:

```
SECRET_KEY = os.environ['SECRET_KEY']

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    'saas_framework.apps.WorkspacesConfig',
    ... # your apps go here
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'saas_framework.core.middleware.AuthMiddleware',
    ... # any others go here
]

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PERMISSION_CLASSES': [
        'saas_framework.core.permissions.Permission',         
    ]
}

# Optional logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
```

## Add basic paths

Include the polls URLconf in your project urls.py like this::

```
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('saas_framework.urls')),
    ... # other paths go here
]
```

## Run the migrations

```
python manage.py migrate
```

## Start the development server

```
export SECRET_KEY=xxxxxxx
python manage.py runserver
```

