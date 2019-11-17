# -*- coding: utf-8 -*-


from typing import Tuple, cast, List, Type, Mapping

from django.conf import settings
from django.db import IntegrityError, transaction, models

from server.apps.resumes.models import (
    Education,
    Experience,
    PersonalInfo,
    Resume,
    Skill,
    SpokenLanguage,
    SupplementarySkill,
    ResumeHobby,
    EducationAchievement,
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
    TextOnlyLike,
    CreateTextOnlyAttr,
    CreateTextOnlyReturnType,
    TextOnlyEnumType,
)
from server.file_upload_utils import (
    bytes_and_file_name_from_data_url_encoded_string,
)  # noqa

RATABLE_CLASSES_MAP: Mapping[RatableEnumType, Type[models.Model]] = {
    RatableEnumType.spoken_language: SpokenLanguage,
    RatableEnumType.supplementary_skill: SupplementarySkill,
}


TEXT_ONLY_CLASSES_MAP: Mapping[TextOnlyEnumType, Type[models.Model]] = {
    TextOnlyEnumType.resume_hobby: ResumeHobby,
    TextOnlyEnumType.education_achievement: EducationAchievement,
}


class ResumesDjangoLogic(ResumesLogicInterface):
    __slots__ = ()

    @staticmethod
    def save_data_url_encoded_file(string: str) -> Tuple[str, str]:  # noqa E501
        (
            bytes_string,
            file_name,
        ) = bytes_and_file_name_from_data_url_encoded_string(  # noqa  E501
            string
        )
        file_path = f"{settings.MEDIA_ROOT}/{file_name}"

        with open(file_path, "wb") as storage_location:
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
        params: CreatePersonalInfoAttrs,
    ) -> CreatePersonalInfoReturnType:  # noqa E501
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
        params: CreateExperienceAttrs,
    ) -> CreateExperienceReturnType:  # noqa E501
        return cast(ExperienceLike, Experience(**params))

    @staticmethod
    def create_education(
        params: CreateEducationAttrs,
    ) -> CreateEducationReturnType:  # noqa E501
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
        tag = RatableEnumType(params.pop("tag"))  # type: ignore[misc] # noqa F821

        _ratable = RATABLE_CLASSES_MAP[tag](**params)
        _ratable.save()
        ratable = cast(Ratable, _ratable)
        ratable.tag = tag
        return ratable

    @staticmethod
    def get_personal_infos(resume_ids: List[str]) -> List[PersonalInfoLike]:
        personal_infos = PersonalInfo.objects.filter(resume_id__in=resume_ids)
        return cast(List[PersonalInfoLike], personal_infos)

    @staticmethod
    def get_educations(resume_ids: List[str]) -> List[EducationLike]:
        educations = Education.objects.filter(resume_id__in=resume_ids)
        return cast(List[EducationLike], educations)

    @staticmethod
    def get_skills(resume_ids: List[str]) -> List[SkillLike]:
        skills = Skill.objects.filter(resume_id__in=resume_ids)
        return cast(List[SkillLike], skills)

    @staticmethod
    def create_text_only(
        params: CreateTextOnlyAttr,
    ) -> CreateTextOnlyReturnType:  # noqa E501
        tag = params.pop("tag")  # type: ignore[misc] # noqa F821
        _text_only = TEXT_ONLY_CLASSES_MAP[tag](**params)
        _text_only.save()
        text_only = cast(TextOnlyLike, _text_only)
        text_only.tag = tag
        return text_only

    @staticmethod
    def get_many_text_only(
        owner_ids: List[str], tag: TextOnlyEnumType,
    ) -> List[TextOnlyLike]:
        text_only_list = TEXT_ONLY_CLASSES_MAP[tag].objects.filter(
            owner_id__in=owner_ids
        )

        return cast(List[TextOnlyLike], text_only_list)
