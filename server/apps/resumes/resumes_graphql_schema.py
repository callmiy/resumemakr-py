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
    CreateResumeComponentErrors,
    CreateExperienceAttrs,
    CreateEducationAttrs,
    CreateSkillAttrs,
    RatableEnumType,
    CreateRatableAttrs,
    CreateRatableErrorsType,
    GetResumeAttrs,
    CreateResumeComponentErrors,
)


class Resume(ObjectType):
    class Meta:
        interfaces = (TimestampsInterface,)

    id = graphene.ID(required=True)
    title = graphene.String(required=True)
    description = graphene.String(required=False)
    user_id = graphene.ID(required=True)
    personal_info = graphene.List(lambda: PersonalInfo)


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


class ResumeChildErrors(ObjectType):
    resume = graphene.String()
    error = graphene.String()


class CreatePersonalInfoErrors(ObjectType):
    errors = graphene.Field(ResumeChildErrors)


class CreatePersonalInfoPayload(graphene.Union):
    class Meta:
        types = (PersonalInfoSuccess, CreatePersonalInfoErrors)


class CreatePersonalInfoMutation(graphene.Mutation):
    class Arguments:
        input = CreatePersonalInfoInput(required=True)

    Output = CreatePersonalInfoPayload

    def mutate(self, info, **inputs):
        user = info.context.current_user
        params = inputs["input"]

        resume = ResumesLogic.get_resume(
            GetResumeAttrs(user_id=user.id, id=params["resume_id"])
        )

        if resume is None:
            errors = CreateResumeComponentErrors(resume="not found")
            return CreatePersonalInfoErrors(errors=errors)

        result = ResumesLogic.create_personal_info(
            cast(CreatePersonalInfoAttrs, params)
        )

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


class CreateExperienceInput(CreateIndexable, graphene.InputObjectType):
    resume_id = graphene.ID(required=True)
    position = graphene.String()
    company_name = graphene.String()
    from_date = graphene.String()
    to_date = graphene.String()


class ExperienceSuccess(ObjectType):
    experience = graphene.Field(Experience)


class CreateExperienceErrors(ObjectType):
    errors = graphene.Field(ResumeChildErrors)


class CreateExperiencePayload(graphene.Union):
    class Meta:
        types = (ExperienceSuccess, CreateExperienceErrors)


class CreateExperienceMutation(graphene.Mutation):
    class Arguments:
        input = CreateExperienceInput(required=True)

    Output = CreateExperiencePayload

    def mutate(self, info, **inputs):
        user = info.context.current_user
        params = inputs["input"]

        resume = ResumesLogic.get_resume(
            GetResumeAttrs(user_id=user.id, id=params["resume_id"])
        )

        if resume is None:
            errors = CreateResumeComponentErrors(resume="not found")
            return CreateExperienceErrors(errors=errors)

        result = ResumesLogic.create_experience(
            cast(CreateExperienceAttrs, dict(**params))
        )  # noqa

        if isinstance(result, CreateResumeComponentErrors):
            return CreateExperienceErrors(errors=result)

        return ExperienceSuccess(experience=result)


class Education(ObjectType):
    class Meta:
        interfaces = (HasResumeIdInterface, Indexable)

    school = graphene.String()
    course = graphene.String()
    from_date = graphene.String()
    to_date = graphene.String()


class CreateEducationInput(CreateIndexable, graphene.InputObjectType):
    resume_id = graphene.ID(required=True)
    school = graphene.String()
    course = graphene.String()
    from_date = graphene.String()
    to_date = graphene.String()


class EducationSuccess(ObjectType):
    education = graphene.Field(Education)


class CreateEducationErrors(ObjectType):
    errors = graphene.Field(ResumeChildErrors)


class CreateEducationPayload(graphene.Union):
    class Meta:
        types = (EducationSuccess, CreateEducationErrors)


class CreateEducationMutation(graphene.Mutation):
    class Arguments:
        input = CreateEducationInput(required=True)

    Output = CreateEducationPayload

    def mutate(self, info, **inputs):
        user = info.context.current_user
        params = inputs["input"]

        resume = ResumesLogic.get_resume(
            GetResumeAttrs(user_id=user.id, id=params["resume_id"])
        )

        if resume is None:
            errors = CreateResumeComponentErrors(resume="not found")
            return CreateEducationErrors(errors=errors)

        result = ResumesLogic.create_education(
            cast(CreateEducationAttrs, params)
        )  # noqa

        return EducationSuccess(education=result)


class Skill(ObjectType):
    class Meta:
        interfaces = (HasResumeIdInterface, Indexable)

    description = graphene.String()


class CreateSkillInput(CreateIndexable, graphene.InputObjectType):
    resume_id = graphene.ID(required=True)
    description = graphene.String()


class SkillSuccess(ObjectType):
    skill = graphene.Field(Skill)


class CreateSkillErrors(ObjectType):
    errors = graphene.Field(ResumeChildErrors)


class CreateSkillPayload(graphene.Union):
    class Meta:
        types = (SkillSuccess, CreateSkillErrors)


class CreateSkillMutation(graphene.Mutation):
    class Arguments:
        input = CreateSkillInput(required=True)

    Output = CreateSkillPayload

    def mutate(self, info, **inputs):
        user = info.context.current_user
        params = inputs["input"]

        resume = ResumesLogic.get_resume(
            GetResumeAttrs(user_id=user.id, id=params["resume_id"])
        )

        if resume is None:
            errors = CreateResumeComponentErrors(resume="not found")
            return CreateSkillErrors(errors=errors)

        result = ResumesLogic.create_skill(cast(CreateSkillAttrs, params))

        return SkillSuccess(skill=result)


RatableEnum = graphene.Enum.from_enum(RatableEnumType)


class Ratable(ObjectType):
    id = graphene.ID(required=True)
    owner_id = graphene.ID(required=True)
    description = graphene.String(required=True)
    tag = graphene.Field(RatableEnum, required=True)
    level = graphene.String()


class RatableSuccess(ObjectType):
    ratable = graphene.Field(Ratable)


class CreateRatableInput(graphene.InputObjectType):
    owner_id = graphene.ID(required=True)
    description = graphene.String(required=True)
    tag = graphene.Field(RatableEnum, required=True)
    level = graphene.String()


class CreateRatableError(ObjectType):
    tag = graphene.Field(RatableEnum, required=True)
    owner = graphene.String()
    error = graphene.String()


class CreateRatableErrors(ObjectType):
    errors = graphene.Field(CreateRatableError)


class CreateRatablePayload(graphene.Union):
    class Meta:
        types = (RatableSuccess, CreateRatableErrors)


class CreateRatableMutation(graphene.Mutation):
    class Arguments:
        input = CreateRatableInput(required=True)

    Output = CreateRatablePayload

    def mutate(self, info, **inputs):
        user = info.context.current_user
        params = inputs["input"]
        tag = params["tag"]

        resume = ResumesLogic.get_resume(
            GetResumeAttrs(user_id=user.id, id=params["owner_id"])
        )

        if resume is None:
            errors = CreateRatableErrorsType(owner="not found", tag=tag)
            return CreateRatableErrors(errors=errors)

        result = ResumesLogic.create_ratable(cast(CreateRatableAttrs, params))

        return RatableSuccess(ratable=result)


class ResumesCombinedMutation(ObjectType):
    create_resume = CreateResumeMutation.Field()
    create_personal_info = CreatePersonalInfoMutation.Field()
    create_experience = CreateExperienceMutation.Field()
    create_education = CreateEducationMutation.Field()
    create_skill = CreateSkillMutation.Field()
    create_ratable = CreateRatableMutation.Field()
