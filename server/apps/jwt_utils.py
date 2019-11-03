# -*- coding: utf-8 -*-

from typing import Mapping

import jwt

from server.settings.components import config

secret = config("SECRET_KEY")


def to_jwt(payload: Mapping[str, str]) -> bytes:
    return jwt.encode(payload, secret, algorithm="HS256")


def from_jwt(encoded_jwt: str) -> Mapping[str, str]:
    return jwt.decode(encoded_jwt, secret, algorithms="HS256")
