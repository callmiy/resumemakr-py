# -*- coding: utf-8 -*-

from typing import Mapping, cast

from django.contrib.auth.hashers import check_password, make_password
from django.db import transaction
from django.db.utils import IntegrityError

from server.apps.accounts.accounts_commons import (
    AccountsLogicInterface,
    UserCredentialTupleType,
    UserLoginType,
    UserRegistrationError,
    UserRegistrationReturnType,
    UserLike,
    MaybeUser,
)
from server.apps.accounts.models import Credential, User


class AccountsLogicDjango(AccountsLogicInterface):
    @staticmethod
    def register_user_with_password(
        attrs: Mapping[str, str]
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

    @staticmethod
    def login_with_password(attrs: Mapping[str, str]) -> UserLoginType:
        try:
            credential = Credential.objects.get(user__email=attrs["email"])

            if check_password(attrs["password"], credential.token):
                return cast(
                    UserCredentialTupleType, (credential.user, credential)
                )  # noqa
            return None
        except Credential.DoesNotExist:
            return None

    @staticmethod
    def get_user_by_id(id: str) -> MaybeUser:
        try:
            return cast(UserLike, User.objects.get(pk=id))
        except User.DoesNotExist:
            return None
