# -*- coding: utf-8 -*-

from typing import cast

import graphene
from graphene.types import ObjectType

from server.apps.resumes.logic import ResumesLogic
from server.apps.resumes.resumes_commons import (  # noqa
    PHOTO_ALREADY_UPLOADED,
    CreatePersonalInfoAttrs,
    CreateResumeAttrs,
)


class Resume(ObjectType):
    id = graphene.ID(required=True)
    title = graphene.String(required=True)
    description = graphene.String(required=False)
    user_id = graphene.ID(required=True)


class CreateResumeInput(graphene.InputObjectType):
    title = graphene.String(required=True)
    description = graphene.String()


class ResumeSuccess(ObjectType):
    resume = graphene.Field(Resume)


class CreateResumeErrors(ObjectType):
    errors = graphene.String()


class CreateResumePayload(graphene.Union):
    class Meta:
        types = (ResumeSuccess, CreateResumeErrors)


class CreateResumeMutation(graphene.Mutation):
    class Arguments:
        input = CreateResumeInput(required=True)

    Output = CreateResumePayload

    def mutate(self, info, **inputs):
        user = info.context["current_user"]
        params = dict(**inputs["input"], user_id=user.id)
        resume = ResumesLogic.create_resume(cast(CreateResumeAttrs, params))
        return ResumeSuccess(resume=resume)


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

    def resolve_photo(self, info):
        return self.photo


class CreatePersonalInfoInput(graphene.InputObjectType):
    first_name = graphene.String()
    last_name = graphene.String()
    profession = graphene.String()
    address = graphene.String()
    email = graphene.String()
    phone = graphene.String()
    date_of_birth = graphene.String()
    photo = graphene.String()
    resume_id = graphene.ID(required=True)


class PersonalInfoSuccess(ObjectType):
    personal_info = graphene.Field(PersonalInfo)


class CreatePersonalInfoErrors(ObjectType):
    errors = graphene.String()


class CreatePersonalInfoPayload(graphene.Union):
    class Meta:
        types = (PersonalInfoSuccess, CreatePersonalInfoErrors)


class CreatePersonalInfoMutation(graphene.Mutation):
    class Arguments:
        input = CreatePersonalInfoInput(required=True)

    Output = CreatePersonalInfoPayload

    def mutate(self, info, **inputs):
        user = info.context["current_user"]
        params = dict(**inputs["input"], user_id=user.id)

        personal_info = ResumesLogic.create_personal_info(
            cast(CreatePersonalInfoAttrs, params)
        )

        return PersonalInfoSuccess(personal_info=personal_info)


class ResumesCombinedMutation(ObjectType):
    create_resume = CreateResumeMutation.Field()
    create_personal_info = CreatePersonalInfoMutation.Field()
