# -*- coding: utf-8 -*-

import graphene
from graphene.types import ObjectType

from server.apps.resumes.resumes_interfaces import (
    PHOTO_ALREADY_UPLOADED,
    CreateResumeAttrs,
)  # noqa
from server.apps.resumes.logic import ResumesLogic


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
        params = CreateResumeAttrs(**inputs["input"], user_id=user.id)
        resume = ResumesLogic.create_resume(params)
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

    def resolve_photo(self, info, **inputs):
        params = inputs["input"]
        photo_params = params.get("photo")

        if photo_params is not None:
            if photo_params == PHOTO_ALREADY_UPLOADED:
                return photo_params


class ResumesCombinedMutation(ObjectType):
    create_resume = CreateResumeMutation.Field()
