# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
from typing import Mapping, NamedTuple, Optional, Tuple, Union

from typing_extensions import Protocol

from server.interfaces import TimestampLike, UUID_IdLike


class UserLike(UUID_IdLike, TimestampLike, Protocol):
    name: str
    email: str


class CredentialLike(UUID_IdLike, TimestampLike, Protocol):
    source: str
    token: str


class UserRegistrationError(NamedTuple):
    email: str


UserCredentialTupleType = Tuple[UserLike, CredentialLike]

UserRegistrationReturnType = Union[
    UserCredentialTupleType, UserRegistrationError
]  # noqa

UserLoginType = Optional[UserCredentialTupleType]


class AccountsLogicInterface(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def register_with_password(
        cls, attrs: Mapping[str, str]
    ) -> UserRegistrationReturnType:
        pass

    @classmethod
    @abstractmethod
    def login_with_password(cls, attrs: Mapping[str, str]) -> UserLoginType:
        pass


ATTRIBUTE_NOT_UNIQUE_ERROR_MESSAGE = "has already been taken"
USER_LOGIN_ERROR_MESSAGE = "Invalid email/password"
