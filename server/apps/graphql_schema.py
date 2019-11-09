# -*- coding: utf-8 -*-

from graphene import ObjectType, Schema, String

from server.apps.accounts.accounts_graphql_schema import (
    AccountsCombinedMutation,
)  # noqa
from server.apps.resumes.resumes_graphql_schema import ResumesCombinedMutation


class AppQuery(ObjectType):
    hello = String()

    def resolve_hello(self, info):
        return "hello"


class AppMutation(
    ResumesCombinedMutation, AccountsCombinedMutation, ObjectType
):  # noqa
    pass


graphql_schema = Schema(query=AppQuery, mutation=AppMutation)
