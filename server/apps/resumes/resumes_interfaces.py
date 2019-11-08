# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
from typing import Tuple

PHOTO_ALREADY_UPLOADED = "___ALREADY_UPLOADED___"


class ResumesLogicInterface(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def save_data_url_encoded_file(base64_encoded_file: str) -> Tuple[str, str]:  # noqa
        pass
