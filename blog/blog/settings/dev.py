from .base import *

DEBUG = True
ALLOWED_HOSTS = ["*"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': "mydatabase",
        "USER": "user",
        "PASSWORD": "password",
        "HOST": "db",
        "PORT": "5432",
    }
}

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
