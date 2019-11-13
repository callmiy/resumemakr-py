# -*- coding: utf-8 -*-


from graphene import ObjectType, Schema, Field
from graphene_django.debug import DjangoDebug

from server.apps.accounts.accounts_graphql_schema import (
    AccountsCombinedMutation,
)  # noqa
from server.apps.resumes.resumes_graphql_schema import (
    ResumesCombinedMutation,
    ResumesCombinedQuery,
)


class AppQuery(ResumesCombinedQuery, ObjectType):
    debug = Field(DjangoDebug, name="_debug")


class AppMutation(
    ResumesCombinedMutation, AccountsCombinedMutation, ObjectType
):  # noqa
    pass


graphql_schema = Schema(query=AppQuery, mutation=AppMutation)
