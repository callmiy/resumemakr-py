# -*- coding: utf-8 -*-


from typing import Tuple, cast

from django.conf import settings
from django.db import IntegrityError, transaction

from server.apps.resumes.models import (
    Education,
    Experience,
    PersonalInfo,
    Resume,
    Skill,
    SpokenLanguage,
    SupplementarySkill,
)  # noqa
from server.apps.resumes.resumes_commons import (
    CreateEducationAttrs,
    CreateEducationReturnType,
    CreateExperienceAttrs,
    CreateExperienceReturnType,
    CreatePersonalInfoAttrs,
    CreatePersonalInfoReturnType,
    CreateResumeAttrs,
    CreateResumeComponentErrors,
    EducationLike,
    ExperienceLike,
    GetResumeAttrs,
    MaybeResume,
    PersonalInfoLike,
    ResumeLike,
    ResumesLogicInterface,
    uniquify_resume_title,
    SkillLike,
    CreateSkillAttrs,
    CreateSkillReturnType,
    CreateRatableAttrs,
    CreateRatableReturnType,
    Ratable,
    RatableEnumType,
    MaybePersonalInfo,
)
from server.file_upload_utils import (
    bytes_and_file_name_from_data_url_encoded_string,
)  # noqa


class ResumesDjangoLogic(ResumesLogicInterface):
    @staticmethod
    def save_data_url_encoded_file(string: str) -> Tuple[str, str]:  # noqa
        bytes_string, file_name = bytes_and_file_name_from_data_url_encoded_string(  # noqa
            string
        )
        file_path = f"{settings.MEDIA_ROOT}/{file_name}"

        with open(file_path, "wb") as storage_location:  # noqa
            storage_location.write(bytes_string)
            return f"{settings.MEDIA_URL}{file_name}", file_path

    @staticmethod
    def create_resume(params: CreateResumeAttrs) -> ResumeLike:
        try:
            with transaction.atomic():
                resume = Resume(**params)
                resume.save()
                return cast(ResumeLike, resume)
        except IntegrityError:
            params["title"] = uniquify_resume_title(params["title"])
            resume = Resume(**params)
            resume.save()
            return cast(ResumeLike, resume)

    @staticmethod
    def get_resume(params: GetResumeAttrs) -> MaybeResume:
        try:
            return cast(ResumeLike, Resume.objects.get(**params))
        except Resume.DoesNotExist:
            return None

    @staticmethod
    def create_personal_info(
        params: CreatePersonalInfoAttrs
    ) -> CreatePersonalInfoReturnType:  # noqa
        try:
            photo = params.get("photo")

            if photo is not None:
                url, _ = ResumesDjangoLogic.save_data_url_encoded_file(photo)
                params["photo"] = url

            personal_info = PersonalInfo(**params)
            personal_info.save()
            return cast(PersonalInfoLike, personal_info)
        except KeyError:
            return CreateResumeComponentErrors(error="something went wrong")

    @staticmethod
    def create_experience(
        params: CreateExperienceAttrs
    ) -> CreateExperienceReturnType:  # noqa
        return cast(ExperienceLike, Experience(**params))

    @staticmethod
    def create_education(
        params: CreateEducationAttrs
    ) -> CreateEducationReturnType:  # noqa
        education = Education(**params)
        education.save()
        return cast(EducationLike, education)

    @staticmethod
    def create_skill(params: CreateSkillAttrs) -> CreateSkillReturnType:
        skill = Skill(**params)
        skill.save()
        return cast(SkillLike, skill)

    @staticmethod
    def create_ratable(params: CreateRatableAttrs) -> CreateRatableReturnType:
        tag = RatableEnumType(params.pop("tag"))  # type: ignore

        if tag == RatableEnumType.spoken_language:
            cls = SpokenLanguage

        elif tag == RatableEnumType.supplementary_skill:
            cls = SupplementarySkill  # type: ignore

        _ratable = cls(**params)
        _ratable.save()
        ratable = cast(Ratable, _ratable)
        ratable.tag = tag
        return ratable

    @staticmethod
    def get_personal_info_from_resume(resume: ResumeLike) -> MaybePersonalInfo:
        personal_info_set = resume.personal_info.all()  # type: ignore
        return None if len(personal_info_set) == 0 else personal_info_set[0]
