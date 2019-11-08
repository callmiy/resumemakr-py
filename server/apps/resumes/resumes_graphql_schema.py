# -*- coding: utf-8 -*-

import graphene
from graphene.types import ObjectType

from server.apps.resumes.resumes_interfaces import PHOTO_ALREADY_UPLOADED


class Resume(ObjectType):
    id = graphene.ID(required=True)
    title = graphene.String(required=True)
    description = graphene.String(required=False)
    user_id = graphene.ID(required=True)


class PersonalInfo(ObjectType):
    id = graphene.ID(required=True)
    first_name = graphene.String()
    last_name = graphene.String()
    profession = graphene.String()
    address = graphene.String()
    email = graphene.String()
    phone = graphene.String()
    date_of_birth = graphene.String()
    photo = graphene.String()
    resume_id = graphene.ID()

    def resolve_photo(self, info, **inputs):
        params = inputs["input"]
        photo_params = params.get("photo")

        if photo_params is not None:
            if photo_params == PHOTO_ALREADY_UPLOADED:
                return photo_params
