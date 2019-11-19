# -*- coding:utf-8 -*-

import base64
from datetime import datetime
from time import time
from typing import Tuple, Union
from uuid import UUID

import graphene
from typing_extensions import Protocol

UUIDType = Union[UUID, str]
data_url_encoded_string_delimiter = ";base64,"


def bytes_and_file_name_from_data_url_encoded_string(
    data_url_encoded_string: str,
) -> Tuple[bytes, str]:  # noqa
    mime_with_data, base64_encoded_string = data_url_encoded_string.split(
        data_url_encoded_string_delimiter
    )  # noqa

    mime = mime_with_data[4:]
    byte_string = base64_encoded_string.encode()
    file_extension = mime.split("/")[1]
    now = str(time()).split(".")[0]
    file_name = f"{now}.{file_extension}"
    return base64.urlsafe_b64decode(byte_string), file_name


class TimestampsInterface(graphene.Interface):
    inserted_at = graphene.DateTime(required=True)
    updated_at = graphene.DateTime(required=True)


class TimestampLike(Protocol):
    inserted_at: datetime
    updated_at: datetime


class UUID_IdLike(Protocol):
    id: UUID
