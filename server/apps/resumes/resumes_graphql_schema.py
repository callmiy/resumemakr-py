# -*- coding: utf-8 -*-

from typing import cast

import graphene
from graphene.types import Interface, ObjectType

from server.apps.graphql_schema_commons import TimestampsInterface
from server.apps.resumes.logic import ResumesLogic
from server.apps.resumes.resumes_commons import (  # noqa
    PHOTO_ALREADY_UPLOADED,
    CreatePersonalInfoAttrs,
    CreateResumeAttrs,
    CreatePersonalInfoErrors as CreatePersonalInfoErrorsType,
)


class Resume(ObjectType):
    class Meta:
        interfaces = (TimestampsInterface,)

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
        user = info.context.current_user
        params = dict(**inputs["input"], user_id=user.id)
        resume = ResumesLogic.create_resume(cast(CreateResumeAttrs, params))
        return ResumeSuccess(resume=resume)


class HasResumeIdInterface(Interface):
    id = graphene.ID(required=True)
    resume_id = graphene.ID(required=True)


class PersonalInfo(ObjectType):
    class Meta:
        interfaces = (HasResumeIdInterface,)

    first_name = graphene.String()
    last_name = graphene.String()
    profession = graphene.String()
    address = graphene.String()
    email = graphene.String()
    phone = graphene.String()
    date_of_birth = graphene.String()
    photo = graphene.String()


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


class CreatePersonalInfoError(ObjectType):
    resume = graphene.String()
    error = graphene.String()


class CreatePersonalInfoErrors(ObjectType):
    errors = graphene.Field(CreatePersonalInfoError)


class CreatePersonalInfoPayload(graphene.Union):
    class Meta:
        types = (PersonalInfoSuccess, CreatePersonalInfoErrors)


class CreatePersonalInfoMutation(graphene.Mutation):
    class Arguments:
        input = CreatePersonalInfoInput(required=True)

    Output = CreatePersonalInfoPayload

    def mutate(self, info, **inputs):
        user = info.context.current_user
        params = dict(**inputs["input"], user_id=user.id)

        result = ResumesLogic.create_personal_info(
            cast(CreatePersonalInfoAttrs, params)
        )

        if isinstance(result, CreatePersonalInfoErrorsType):
            return CreatePersonalInfoErrors(errors=result)

        return PersonalInfoSuccess(personal_info=result)


class TextOnly(ObjectType):
    id: graphene.ID(required=True)  # type: ignore
    text: graphene.String(required=True)  # type: ignore
    owner_id: graphene.ID(required=True)  # type: ignore


class CreateTextOnly(graphene.InputObjectType):
    text: graphene.String(required=True)  # type: ignore
    owner_id: graphene.ID(required=True)  # type: ignore


class Indexable(Interface):
    index = graphene.Int(required=True)


class CreateIndexable(graphene.InputObjectType):
    index = graphene.Int(required=True)


class Experience(ObjectType):
    class Meta:
        interfaces = (HasResumeIdInterface, Indexable)

    position = graphene.String()
    company_name = graphene.String()
    from_date = graphene.String()
    to_date = graphene.String()


class CreateExperience(CreateIndexable, graphene.InputObjectType):
    resume_id = graphene.ID(required=True)


class ExperienceSuccess(ObjectType):
    experience = graphene.Field(Experience)


class Education(ObjectType):
    class Meta:
        interfaces = (HasResumeIdInterface, Indexable)

    school = graphene.String()
    course = graphene.String()
    from_date = graphene.String()
    to_date = graphene.String()


class Skill(ObjectType):
    class Meta:
        interfaces = (HasResumeIdInterface, Indexable)

    description = graphene.String()


class Ratable(ObjectType):
    id = graphene.ID(required=True)
    owner_id = graphene.ID(required=True)
    description = graphene.String(required=True)
    level = graphene.String()


class ResumesCombinedMutation(ObjectType):
    create_resume = CreateResumeMutation.Field()
    create_personal_info = CreatePersonalInfoMutation.Field()
