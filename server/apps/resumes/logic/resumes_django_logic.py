# -*- coding: utf-8 -*-

from typing import Tuple, cast

from django.conf import settings

from server.apps.resumes.resumes_interfaces import (  # noqa
    ResumeLike,
    ResumesLogicInterface,
    CreateResumeAttrs,
)
from server.file_upload_utils import (  # noqa
    bytes_and_file_name_from_data_url_encoded_string,
)
from server.apps.resumes.models import Resume


class ResumesDjangoLogic(ResumesLogicInterface):
    def save_data_url_encoded_file(string: str) -> Tuple[str, str]:  # noqa
        bytes_string, file_name = bytes_and_file_name_from_data_url_encoded_string(  # noqa
            string
        )
        file_path = f"{settings.MEDIA_ROOT}/{file_name}"

        with open(file_path, "wb") as storage_location:  # noqa
            storage_location.write(bytes_string)
            return f"{settings.MEDIA_URL}/{file_name}", file_path

    def create_resume(params: CreateResumeAttrs) -> ResumeLike:
        resume = Resume(**params)
        resume.save()
        return cast(ResumeLike, resume)
