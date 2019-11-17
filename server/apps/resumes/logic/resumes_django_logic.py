# -*- coding: utf-8 -*-


from typing import List, Mapping, Tuple, Type, cast, Optional

from django.conf import settings
from django.db import IntegrityError, models, transaction

from server.apps.apps_commons import UUIDType
from server.apps.resumes.models import (  # noqa
    Education,
    EducationAchievement,
    Experience,
    PersonalInfo,
    Resume,
    ResumeHobby,
    Skill,
    SpokenLanguage,
    SupplementarySkill,
    ExperienceAchievement,
    SkillAchievement,
)
from server.apps.resumes.resumes_commons import (
    CreateEducationAttrs,
    CreateEducationReturnType,
    CreateExperienceAttrs,
    CreateExperienceReturnType,
    CreatePersonalInfoAttrs,
    CreatePersonalInfoReturnType,
    CreateRatableAttrs,
    CreateRatableReturnType,
    CreateResumeAttrs,
    CreateResumeComponentErrors,
    CreateSkillAttrs,
    CreateSkillReturnType,
    CreateTextOnlyAttr,
    CreateTextOnlyReturnType,
    EducationLike,
    ExperienceLike,
    GetResumeAttrs,
    MaybeResume,
    PersonalInfoLike,
    Ratable,
    RatableEnumType,
    ResumeLike,
    ResumesLogicInterface,
    SkillLike,
    TextOnlyEnumType,
    TextOnlyLike,
    uniquify_resume_title,
    TextOnlyOwnersUnion,
)
from server.file_upload_utils import (  # noqa
    bytes_and_file_name_from_data_url_encoded_string,
)

RATABLE_CLASSES_MAP: Mapping[RatableEnumType, Type[models.Model]] = {
    RatableEnumType.spoken_language: SpokenLanguage,
    RatableEnumType.supplementary_skill: SupplementarySkill,
}


TEXT_ONLY_CLASSES_MAP: Mapping[TextOnlyEnumType, Type[models.Model]] = {
    TextOnlyEnumType.resume_hobby: ResumeHobby,
    TextOnlyEnumType.education_achievement: EducationAchievement,
    TextOnlyEnumType.experience_achievement: ExperienceAchievement,
    TextOnlyEnumType.skill_achievement: SkillAchievement,
}


TEXT_ONLY_OWNER_CLASSES_MAP: Mapping[TextOnlyEnumType, Type[models.Model]] = {
    TextOnlyEnumType.resume_hobby: Resume,
    TextOnlyEnumType.education_achievement: Education,
    TextOnlyEnumType.experience_achievement: Experience,
    TextOnlyEnumType.skill_achievement: Skill,
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
        experience = Experience(**params)
        experience.save()
        return cast(ExperienceLike, experience)

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
    def get_personal_infos(
        resume_ids: List[UUIDType],
    ) -> List[PersonalInfoLike]:  # noqa E501
        personal_infos = PersonalInfo.objects.filter(resume_id__in=resume_ids)
        return cast(List[PersonalInfoLike], personal_infos)

    @staticmethod
    def get_educations(resume_ids: List[UUIDType]) -> List[EducationLike]:
        educations = Education.objects.filter(resume_id__in=resume_ids)
        return cast(List[EducationLike], educations)

    @staticmethod
    def get_skills(resume_ids: List[UUIDType]) -> List[SkillLike]:
        skills = Skill.objects.filter(resume_id__in=resume_ids)
        return cast(List[SkillLike], skills)

    @staticmethod
    def get_experiences(resume_ids: List[UUIDType]) -> List[ExperienceLike]:
        experiences = Experience.objects.filter(resume_id__in=resume_ids)
        return cast(List[ExperienceLike], experiences)

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
        owner_ids: List[UUIDType], tag: TextOnlyEnumType,
    ) -> List[TextOnlyLike]:
        text_only_list = TEXT_ONLY_CLASSES_MAP[tag].objects.filter(
            owner_id__in=owner_ids
        )

        return cast(List[TextOnlyLike], text_only_list)

    @staticmethod
    def get_ratables(
        owner_ids: List[UUIDType], tag: RatableEnumType,
    ) -> List[Ratable]:  # noqa E501
        _ratables = RATABLE_CLASSES_MAP[tag].objects.filter(
            owner_id__in=owner_ids
        )  # noqa E501

        ratables: List[Ratable] = []

        for _ratable in _ratables:
            ratable = cast(Ratable, _ratable)
            ratable.tag = tag
            ratables.append(ratable)

        return ratables

    @staticmethod
    def get_text_only_owner(
        owner_id: UUIDType, tag: TextOnlyEnumType,
    ) -> Optional[TextOnlyOwnersUnion]:
        related_class = TEXT_ONLY_OWNER_CLASSES_MAP[tag]

        try:
            _related = related_class.objects.get(pk=owner_id)
            return _related
        except related_class.DoesNotExist:
            return None
