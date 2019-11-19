# -*- coding: utf-8 -*-

from typing import Mapping

import jwt

from server.settings.components import config

secret = config("SECRET_KEY")


class JwtManager:
    @staticmethod
    def to_jwt(payload: Mapping[str, str]) -> str:
        return jwt.encode(payload, secret, algorithm="HS256").decode()

    @staticmethod
    def from_jwt(encoded_jwt: str) -> Mapping[str, str]:
        return jwt.decode(encoded_jwt, secret, algorithms="HS256")
