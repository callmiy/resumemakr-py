# -*- coding:utf-8 -*-

import uuid
from datetime import datetime
from typing_extensions import Protocol


class TimestampLike(Protocol):
    inserted_at: datetime
    updated_at: datetime


class UUID_IdLike(Protocol):
    id: uuid.UUID
