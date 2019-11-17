# -*- coding: utf-8 -*-

from __future__ import annotations

import re
from abc import ABCMeta, abstractstaticmethod
from enum import Enum
from time import time
from typing import List, NamedTuple, Optional, Tuple, Union

from mypy_extensions import TypedDict
from typing_extensions import Protocol

from server.interfaces import TimestampLike, UUID_IdLike
from server.apps.apps_commons import UUIDType

PHOTO_ALREADY_UPLOADED = "___ALREADY_UPLOADED___"
RESUME_TITLE_WITH_TIME = re.compile(r"^(.+?)_(\d{10})$")


class RatableEnumType(Enum):
    spoken_language = "spoken_language"
    supplementary_skill = "supplementary_skill"


class TextOnlyEnumType(Enum):
    resume_hobby = "resume_hobby"
    education_achievement = "education_achievement"


class ResumesLogicInterface(metaclass=ABCMeta):
    __slots__ = ()

    @staticmethod
    @abstractstaticmethod
    def save_data_url_encoded_file(
        base64_encoded_file: str,
    ) -> Tuple[str, str]:  # noqa E501
        pass

    @staticmethod
    @abstractstaticmethod
    def create_resume(params: CreateResumeAttrs) -> ResumeLike:
        pass

    @staticmethod
    @abstractstaticmethod
    def create_personal_info(
        params: CreatePersonalInfoAttrs,
    ) -> CreatePersonalInfoReturnType:  # noqa E501
        pass

    @staticmethod
    @abstractstaticmethod
    def get_resume(params: GetResumeAttrs) -> MaybeResume:
        pass

    @staticmethod
    @abstractstaticmethod
    def create_experience(
        params: CreateExperienceAttrs,
    ) -> CreateExperienceReturnType:  # noqa E501
        pass

    @staticmethod
    @abstractstaticmethod
    def create_education(
        params: CreateEducationAttrs,
    ) -> CreateEducationReturnType:  # noqa E50
        pass

    @staticmethod
    @abstractstaticmethod
    def create_skill(params: CreateSkillAttrs) -> CreateSkillReturnType:
        pass

    @staticmethod
    @abstractstaticmethod
    def create_ratable(params: CreateRatableAttrs) -> CreateRatableReturnType:
        pass

    @staticmethod
    @abstractstaticmethod
    def get_personal_infos(
        resume_ids: List[str],
    ) -> List[PersonalInfoLike]:  # noqa E501
        pass

    @staticmethod
    @abstractstaticmethod
    def get_educations(resume_ids: List[str]) -> List[EducationLike]:
        pass

    @staticmethod
    @abstractstaticmethod
    def get_skills(resume_ids: List[str]) -> List[SkillLike]:
        pass

    @staticmethod
    @abstractstaticmethod
    def create_text_only(attrs: CreateTextOnlyAttr) -> CreateTextOnlyReturnType:
        pass

    @staticmethod
    @abstractstaticmethod
    def get_many_text_only(
        owner_ids: List[str], tag: TextOnlyEnumType,
    ) -> List[TextOnlyLike]:
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
    user_id: UUIDType


class CreateResumeRequiredAttrs(TypedDict):
    user_id: UUIDType
    title: str


class CreateResumeAttrs(CreateResumeRequiredAttrs, total=False):
    description: str


class GetResumeAttrs(TypedDict):
    user_id: UUIDType
    id: str


MaybeResume = Optional[ResumeLike]


class CreateResumeComponentErrors:
    __slots__ = "resume", "error"

    def __init__(
        self, resume: Optional[str] = None, error: Optional[str] = None
    ) -> None:
        self.resume = resume
        self.error = error


############################ END RESUME ############################## noqa


class CreateIndexableAttr(TypedDict):
    index: int


class CreateResumeComponentRequiredAttrs(TypedDict):
    resume_id: UUIDType


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
    resume_id: UUIDType


class CreatePersonalInfoAttrs(CreateResumeComponentRequiredAttrs, total=False):
    first_name: str
    last_name: str
    profession: str
    address: str
    email: str
    phone: str
    date_of_birth: str
    photo: str


CreatePersonalInfoReturnType = Union[
    PersonalInfoLike, CreateResumeComponentErrors
]  # noqa

MaybePersonalInfo = Optional[PersonalInfoLike]

############################ END PERSONAL INFO ########################## noqa

############################ EDUCATION ############################## noqa


class EducationLike(UUID_IdLike, TimestampLike, Indexable, Protocol):
    school: str
    course: str
    from_date: str
    to_date: str
    resume_id: UUIDType


class CreateEducationAttrs(
    CreateResumeComponentRequiredAttrs, CreateIndexableAttr, total=False
):
    school: str
    course: str
    from_date: str
    to_date: str


CreateEducationReturnType = Union[EducationLike, CreateResumeComponentErrors]

############################ END EDUCATION ############################ noqa

############################ EXPERIENCE ############################## noqa


class ExperienceLike(UUID_IdLike, TimestampLike, Indexable, Protocol):
    position: str
    company_name: str
    from_date: str
    to_date: str
    resume_id: UUIDType


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
    resume_id: UUIDType


class CreateSkillAttrs(
    CreateResumeComponentRequiredAttrs, CreateIndexableAttr, total=False
):
    description: str


CreateSkillReturnType = Union[SkillLike, CreateResumeComponentErrors]

############################ end skills ############################## noqa

############################ ratable ################################# noqa


class Ratable(UUID_IdLike, TimestampLike, Protocol):
    description: str
    level: str
    owner_id: UUIDType
    tag: RatableEnumType


class CreateRatableRequiredAttrs(TypedDict):
    description: str
    owner_id: UUIDType
    user_id: UUIDType
    tag: RatableEnumType


class CreateRatableAttrs(CreateRatableRequiredAttrs, total=False):
    level: str


class CreateRatableErrorsType(NamedTuple):
    tag: RatableEnumType
    owner: Optional[str] = None
    error: Optional[str] = None


CreateRatableReturnType = Union[Ratable, CreateRatableErrorsType]
############################ end ratable ############################## noqa


############################ TEXT ONLY LIKE ############################## noqa


class TextOnlyLike(UUID_IdLike, Protocol):
    text: str
    owner_id: UUIDType
    tag: TextOnlyEnumType


class CreateTextOnlyAttr(TypedDict):
    text: str
    owner_id: UUIDType
    tag: TextOnlyEnumType


class CreateTextOnlyErrorsType:
    __slots__ = "tag", "owner", "error"

    def __init__(
        self,
        tag: TextOnlyEnumType,
        owner: Optional[str] = None,
        error: Optional[str] = None,
    ) -> None:
        self.tag = tag
        self.owner = owner
        self.error = error


CreateTextOnlyReturnType = Union[TextOnlyLike, CreateTextOnlyErrorsType]


############################ END TEST ONLY LIKE ####################### noqa
