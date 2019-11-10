# -*- coding: utf-8 -*-


from graphene import ObjectType, Schema, Field
from graphene_django.debug import DjangoDebug

from server.apps.accounts.accounts_graphql_schema import (
    AccountsCombinedMutation,
)  # noqa
from server.apps.resumes.resumes_graphql_schema import ResumesCombinedMutation
from server.apps.accounts.logic import user_from_jwt


class AppQuery(ObjectType):
    debug = Field(DjangoDebug, name="_debug")

    def resolve_hello(self, info):
        return "hello"


class AppMutation(
    ResumesCombinedMutation, AccountsCombinedMutation, ObjectType
):  # noqa
    pass


graphql_schema = Schema(query=AppQuery, mutation=AppMutation)

AUTH_USER_KEY = "current_user"


def put_user_context(next, root, info, **args):
    if getattr(info.context, AUTH_USER_KEY, None):
        return next(root, info, **args)

    authorization = info.context.headers.get("Authorization")

    if authorization is None:
        return next(root, info, **args)

    prefix_jwt = authorization.split()

    if len(prefix_jwt) != 2:
        return next(root, info, **args)

    if prefix_jwt[0] != "Bearer":
        return next(root, info, **args)

    setattr(info.context, AUTH_USER_KEY, user_from_jwt(prefix_jwt[1]))

    return next(root, info, **args)
