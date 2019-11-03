# -*- coding: utf-8 -*-

from django.db import models
from ulid2 import generate_ulid_as_uuid


class User(models.Model):  # type: ignore[disallow_any_explicit]
    id = models.UUIDField(default=generate_ulid_as_uuid, primary_key=True)
    name = models.CharField(max_length=255)

    # This should be unique but we don't want django to create the constraint
    email = models.EmailField(unique=False)

    inserted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.name


class Credential(models.Model):  # type: ignore[disallow_any_explicit] # noqa
    id = models.UUIDField(default=generate_ulid_as_uuid, primary_key=True)
    source = models.CharField(max_length=255)
    token = models.CharField(max_length=255)
    inserted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    recovery_token = models.TextField(blank=True, null=True)  # noqa DJ01
    recovery_token_expires = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(
        User, models.DO_NOTHING, db_index=False, db_constraint=False
    )

    class Meta:
        db_table = "credentials"

        indexes = [
            models.Index(fields=["user"], name="credentials_user_id_index")
        ]  # noqa

    def __str__(self):
        return self.source
