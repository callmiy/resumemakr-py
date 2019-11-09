# -*- coding: utf-8 -*-

from __future__ import annotations
from abc import ABCMeta, abstractmethod
from typing import Tuple

from mypy_extensions import TypedDict
from typing_extensions import Protocol

from server.interfaces import TimestampLike, UUID_IdLike

PHOTO_ALREADY_UPLOADED = "___ALREADY_UPLOADED___"


class CreateResumeRequiredAttrs(TypedDict):
    user_id: str
    title: str


class CreateResumeAttrs(CreateResumeRequiredAttrs, total=False):
    description: str


class ResumesLogicInterface(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def save_data_url_encoded_file(
        cls, base64_encoded_file: str
    ) -> Tuple[str, str]:  # noqa
        pass

    @classmethod
    @abstractmethod
    def create_resume(cls, params: CreateResumeAttrs) -> ResumeLike:
        pass


class ResumeLike(UUID_IdLike, TimestampLike, Protocol):
    first_name: str
    last_name: str
    profession: str
    address: str
    email: str
    phone: str
    date_of_birth: str
    photo: str
    resume_id: str
