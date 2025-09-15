from .base import *

DEBUG = True
ALLOWED_HOSTS = ["*"]
CSRF_TRUSTED_ORIGINS = ["https://www.harribenhub.com"]

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

STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / "static",   # if you have a global static/ folder
]

STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": "dnyin4f6e",
    "API_KEY": "245323211134724",
    "API_SECRET": "2kENSedE97Vvf8zb4upBV2ekoAY",
}
