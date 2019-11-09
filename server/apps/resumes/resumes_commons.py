# -*- coding: utf-8 -*-

from __future__ import annotations

import re
from abc import ABCMeta, abstractmethod
from time import time
from typing import Tuple

from mypy_extensions import TypedDict
from typing_extensions import Protocol

from server.interfaces import TimestampLike, UUID_IdLike

PHOTO_ALREADY_UPLOADED = "___ALREADY_UPLOADED___"
RESUME_TITLE_WITH_TIME = re.compile(r"^(.+?)_(\d{10})$")


class CreateResumeRequiredAttrs(TypedDict):
    user_id: str
    title: str


class CreateResumeAttrs(CreateResumeRequiredAttrs, total=False):
    description: str


class ResumesLogicInterface(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def save_data_url_encoded_file(base64_encoded_file: str) -> Tuple[str, str]:  # noqa
        pass

    @staticmethod
    @abstractmethod
    def create_resume(params: CreateResumeAttrs) -> ResumeLike:
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


def uniquify_resume_title(title: str) -> str:
    matched = RESUME_TITLE_WITH_TIME.match(title)

    if matched is not None:
        title = matched.group(1)

    part1, part2 = str(time()).split(".")
    now = str(int(part1) + int(part2))[:10]
    return f"{title}_{now}"
