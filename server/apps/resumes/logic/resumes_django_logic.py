# -*- coding: utf-8 -*-


from typing import Tuple, cast

from django.conf import settings
from django.db import IntegrityError, transaction

from server.apps.resumes.models import Resume, PersonalInfo
from server.apps.resumes.resumes_commons import (
    CreateResumeAttrs,  # noqa
    ResumeLike,
    ResumesLogicInterface,
    uniquify_resume_title,
    CreatePersonalInfoAttrs,
    PersonalInfoLike,
    GetResumeAttrs,
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
            return f"{settings.MEDIA_URL}/{file_name}", file_path

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
    def get_resume(params: GetResumeAttrs) -> ResumeLike:
        return cast(ResumeLike, Resume.objects.get(**params))

    @staticmethod
    def create_personal_info(
        params: CreatePersonalInfoAttrs
    ) -> PersonalInfoLike:  # noqa
        resume_id = params.pop("resume_id")  # type: ignore
        user_id = params.pop("user_id")  # type: ignore

        resume = ResumesDjangoLogic.get_resume(
            GetResumeAttrs(user_id=user_id, id=resume_id)
        )

        personal_info = PersonalInfo(**params, resume=cast(Resume, resume))
        return cast(PersonalInfoLike, personal_info)
