# -*- coding: utf-8 -*-

import uuid
from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import Mapping, Tuple

from typing_extensions import Protocol


class TimestampLike(Protocol):
    inserted_at: datetime
    updated_at: datetime


class UUID_IdLike(Protocol):
    id: uuid.UUID


class UserLike(UUID_IdLike, TimestampLike, Protocol):
    name: str
    email: str


class CredentialLike(UUID_IdLike, TimestampLike, Protocol):
    source: str
    token: str


UserCredentialTupleType = Tuple[UserLike, CredentialLike]


class AccountsLogicInterface(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def register_with_password(
        cls, attrs: Mapping[str, str]
    ) -> UserCredentialTupleType:
        pass

    @classmethod
    @abstractmethod
    def login_with_password(
        cls, attrs: Mapping[str, str]
    ) -> UserCredentialTupleType:  # noqa
        pass
