# -*- coding: utf-8 -*-

import base64
from time import time
from typing import Tuple

data_url_encoded_string_delimiter = ";base64,"


def bytes_and_file_name_from_data_url_encoded_string(
    data_url_encoded_string: str
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
