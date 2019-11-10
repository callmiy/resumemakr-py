# -*- coding:utf-8 -*-

from server.settings.components import BASE_DIR

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "resumemakr_test_d",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "localhost",
        "PORT": 5432,
        "OPTIONS": {"connect_timeout": 10},
    }
}


PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

AUTHENTICATION_BACKENDS = ("django.contrib.auth.backends.ModelBackend",)

MEDIA_ROOT = BASE_DIR.joinpath("tests/media")
