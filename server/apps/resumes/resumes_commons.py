# -*- coding: utf-8 -*-

from __future__ import annotations

import re
from abc import ABCMeta, abstractmethod
from time import time
from typing import NamedTuple, Optional, Tuple, Union

from mypy_extensions import TypedDict
from typing_extensions import Protocol

from server.interfaces import TimestampLike, UUID_IdLike

PHOTO_ALREADY_UPLOADED = "___ALREADY_UPLOADED___"
RESUME_TITLE_WITH_TIME = re.compile(r"^(.+?)_(\d{10})$")


class ResumesLogicInterface(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def save_data_url_encoded_file(base64_encoded_file: str) -> Tuple[str, str]:  # noqa
        pass

    @staticmethod
    @abstractmethod
    def create_resume(params: CreateResumeAttrs) -> ResumeLike:
        pass

    @staticmethod
    @abstractmethod
    def create_personal_info(
        params: CreatePersonalInfoAttrs
    ) -> CreatePersonalInfoReturnType:  # noqa
        pass

    @staticmethod
    @abstractmethod
    def get_resume(params: GetResumeAttrs) -> MaybeResume:
        pass

    @staticmethod
    @abstractmethod
    def create_experience(
        params: CreateExperienceAttrs
    ) -> CreateExperienceReturnType:  # noqa
        pass


def uniquify_resume_title(title: str) -> str:
    matched = RESUME_TITLE_WITH_TIME.match(title)

    if matched is not None:
        title = matched.group(1)

    part1, part2 = str(time()).split(".")
    now = str(int(part1) + int(part2))[:10]
    return f"{title}_{now}"


############################ RESUME ############################## noqa
class ResumeLike(UUID_IdLike, TimestampLike, Protocol):
    title: str
    description: str
    user_id: str


class CreateResumeRequiredAttrs(TypedDict):
    user_id: str
    title: str


class CreateResumeAttrs(CreateResumeRequiredAttrs, total=False):
    description: str


class GetResumeAttrs(TypedDict):
    user_id: str
    id: str


MaybeResume = Optional[ResumeLike]
############################ END RESUME ############################## noqa


class CreateIndexableAttr(TypedDict):
    index: int


class CreateResumeComponentRequiredAttrs(TypedDict):
    resume_id: str
    user_id: str


class Indexable(Protocol):
    index: int


############################ PERSONAL INFO ############################## noqa
class PersonalInfoLike(UUID_IdLike, TimestampLike, Protocol):
    first_name: str
    last_name: str
    profession: str
    address: str
    email: str
    phone: str
    date_of_birth: str
    photo: str
    resume_id: str


class CreatePersonalInfoAttrs(CreateResumeComponentRequiredAttrs, total=False):
    first_name: str
    last_name: str
    profession: str
    address: str
    email: str
    phone: str
    date_of_birth: str
    photo: str


class CreateResumeComponentErrors(NamedTuple):
    resume: Optional[str] = None
    error: Optional[str] = None


CreatePersonalInfoReturnType = Union[
    PersonalInfoLike, CreateResumeComponentErrors
]  # noqa


############################ END PERSONAL INFO ########################## noqa

############################ EDUCATION ############################## noqa
class EducationLike(UUID_IdLike, TimestampLike, Indexable, Protocol):
    school: str
    course: str
    from_date: str
    to_date: str
    resume_id: str


class CreateEducationAttrs(
    CreateResumeComponentRequiredAttrs, CreateIndexableAttr, total=False
):
    school: str
    course: str
    from_date: str
    to_date: str


############################ END EDUCATION ############################ noqa

############################ EXPERIENCE ############################## noqa


class ExperienceLike(UUID_IdLike, TimestampLike, Indexable, Protocol):
    position: str
    company_name: str
    from_date: str
    to_date: str
    resume_id: str


class CreateExperienceAttrs(
    CreateResumeComponentRequiredAttrs, CreateIndexableAttr, total=False
):
    position: str
    company_name: str
    from_date: str
    to_date: str


CreateExperienceReturnType = Union[ExperienceLike, CreateResumeComponentErrors]

############################ END experience ############################## noqa

############################ skills ############################## noqa


class SkillLike(UUID_IdLike, TimestampLike, Indexable, Protocol):
    description: str
    resume_id: str


class CreateSkillAttrs(
    CreateResumeComponentRequiredAttrs, CreateIndexableAttr, total=False
):
    description: str


############################ end skills ############################## noqa

############################ ratable ################################# noqa


class Ratable(UUID_IdLike, TimestampLike, Protocol):
    description: str
    level: str
    owner_id: str


class CreateRatableRequiredAttrs(TypedDict):
    description: str
    owner_id: str
    user_id: str


class CreateSpokenLanguageAttrs(
    CreateResumeComponentRequiredAttrs, total=False
):  # noqa
    level: str


############################ end ratable ############################## noqa

############################ TEXT ONLY LIKE ############################## noqa


class TextOnlyLike(UUID_IdLike, Protocol):
    text: str
    owner_id: str


class CreateTextOnlyAttr(TypedDict):
    text: str
    owner_id: str


############################ END TEST ONLY LIKE ####################### noqa
