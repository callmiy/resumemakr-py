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
    CreateResumeComponentRequiredAttrs,
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
    CreateRatableRequiredAttrs,
    CreateRatableErrorsType,
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
    def _get_resume_from_user_and_resume_ids(
        params: CreateResumeComponentRequiredAttrs
    ) -> Tuple[MaybeResume, CreateResumeComponentRequiredAttrs]:
        resume_id = params.pop("resume_id")  # type: ignore
        user_id = params.pop("user_id")  # type: ignore

        return (
            ResumesDjangoLogic.get_resume(
                GetResumeAttrs(user_id=user_id, id=resume_id)
            ),
            params,
        )

    @staticmethod
    def _get_resume_from_user_and_owner_ids(
        params: CreateRatableRequiredAttrs
    ) -> Tuple[MaybeResume, CreateRatableRequiredAttrs]:
        resume_id = params.pop("owner_id")  # type: ignore
        user_id = params.pop("user_id")  # type: ignore

        return (
            ResumesDjangoLogic.get_resume(
                GetResumeAttrs(user_id=user_id, id=resume_id)
            ),
            params,
        )

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
            resume, rest_params = ResumesDjangoLogic._get_resume_from_user_and_resume_ids(  # noqa
                params
            )  # noqa

            if resume is None:
                return CreateResumeComponentErrors(resume="not found")

            photo = params.get("photo")

            if photo is not None:
                url, _ = ResumesDjangoLogic.save_data_url_encoded_file(photo)
                params["photo"] = url

            personal_info = PersonalInfo(
                **rest_params, resume=cast(Resume, resume)
            )  # noqa
            return cast(PersonalInfoLike, personal_info)
        except KeyError:
            return CreateResumeComponentErrors(error="something went wrong")

    @staticmethod
    def create_experience(
        params: CreateExperienceAttrs
    ) -> CreateExperienceReturnType:  # noqa
        try:
            resume, rest_params = ResumesDjangoLogic._get_resume_from_user_and_resume_ids(  # noqa
                params
            )  # noqa

            if resume is None:
                return CreateResumeComponentErrors(resume="not found")

            experience = Experience(**rest_params, resume=cast(Resume, resume))  # noqa
            return cast(ExperienceLike, experience)
        except KeyError:
            return CreateResumeComponentErrors(error="something went wrong")

    @staticmethod
    def create_education(
        params: CreateEducationAttrs
    ) -> CreateEducationReturnType:  # noqa
        try:
            resume, rest_params = ResumesDjangoLogic._get_resume_from_user_and_resume_ids(  # noqa
                params
            )  # noqa

            if resume is None:
                return CreateResumeComponentErrors(resume="not found")

            education = Education(**rest_params, resume=cast(Resume, resume))  # noqa
            return cast(EducationLike, education)
        except KeyError:
            return CreateResumeComponentErrors(error="something went wrong")

    @staticmethod
    def create_skill(params: CreateSkillAttrs) -> CreateSkillReturnType:
        try:
            resume, rest_params = ResumesDjangoLogic._get_resume_from_user_and_resume_ids(  # noqa
                params
            )  # noqa

            if resume is None:
                return CreateResumeComponentErrors(resume="not found")

            skill = Skill(**rest_params, resume=cast(Resume, resume))  # noqa
            return cast(SkillLike, skill)
        except KeyError:
            return CreateResumeComponentErrors(error="something went wrong")

    @staticmethod
    def create_ratable(params: CreateRatableAttrs) -> CreateRatableReturnType:
        tag = RatableEnumType(params.pop("tag"))  # type: ignore

        try:
            resume, rest_params = ResumesDjangoLogic._get_resume_from_user_and_owner_ids(  # noqa
                params
            )  # noqa

            if resume is None:
                return CreateRatableErrorsType(owner="not found", tag=tag)

            result = SpokenLanguage(**rest_params, owner=cast(Resume, resume))
            ratable = cast(Ratable, result)
            ratable.tag = RatableEnumType.spoken_language
            return ratable
        except KeyError:
            return CreateRatableErrorsType(
                error="something went wrong", tag=tag
            )  # noqa
