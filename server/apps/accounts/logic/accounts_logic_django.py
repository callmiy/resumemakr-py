# -*- coding: utf-8 -*-

from django.contrib.auth.hashers import make_password, check_password
from django.db import transaction
from typing import Mapping, cast

from django.db.utils import IntegrityError

from server.apps.accounts.models import Credential, User
from server.apps.accounts.accounts_interfaces import (
    AccountsLogicInterface,
    UserCredentialTupleType,
    UserRegistrationReturnType,
    UserRegistrationError,
    UserLoginType,
)


class AccountsLogicDjango(AccountsLogicInterface):
    @classmethod
    def register_user_with_password(
        cls, attrs: Mapping[str, str]
    ) -> UserRegistrationReturnType:
        with transaction.atomic():
            try:
                user = User(name=attrs["name"], email=attrs["email"])
                user.save()

                credential = Credential(
                    source="password",
                    token=make_password(attrs["password"]),
                    user=user,  # noqa
                )
                credential.save()

                user_credential_tuple = cast(
                    UserCredentialTupleType, (user, credential)
                )  # noqa

                return user_credential_tuple
            except IntegrityError:
                return UserRegistrationError(email="has already been taken")

    @classmethod
    def login_with_password(cls, attrs: Mapping[str, str]) -> UserLoginType:
        try:
            credential = Credential.objects.get(user__email=attrs["email"])

            if check_password(attrs["password"], credential.token):
                return cast(
                    UserCredentialTupleType, (credential.user, credential)
                )  # noqa
            return None
        except Credential.DoesNotExist:
            return None
