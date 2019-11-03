# -*- coding: utf-8 -*-

import graphene
from graphene_django.types import ObjectType

from server.apps.accounts.accounts_interfaces import UserRegistrationError
from server.apps.accounts.logic import AccountsLogic
from server.apps.jwt_utils import to_jwt


class TimestampsInterface(graphene.Interface):
    inserted_at = graphene.DateTime(required=True)
    updated_at = graphene.DateTime(required=True)


class User(ObjectType):
    class Meta:
        interfaces = (TimestampsInterface,)

    id = graphene.ID(required=True)
    jwt = graphene.String(required=True)
    name = graphene.String(required=True)
    email = graphene.String(required=True)

    def resolve_jwt(self, info):
        return to_jwt({"user": str(self.id)})


class RegistrationError(ObjectType):
    email = graphene.String()


class RegistrationInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    source = graphene.String(required=True)
    password = graphene.String(required=True)
    password_confirmation = graphene.String(required=True)


class UserRegistrationMutation(graphene.Mutation):
    class Arguments:
        input = RegistrationInput(required=True)

    user = graphene.Field(User)
    errors = graphene.Field(RegistrationError)

    def mutate(self, info, **inputs):
        result = AccountsLogic.register_user_with_password(inputs["input"])

        if isinstance(result, UserRegistrationError):
            return UserRegistrationMutation(errors=result)

        return UserRegistrationMutation(user=result[0])
