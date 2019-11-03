# -*- coding: utf-8 -*-

from graphene import ObjectType, Schema, String

from server.apps.accounts.accounts_graphql_schema import (
    UserRegistrationMutation,
)  # noqa


class AppQuery(ObjectType):
    hello = String()

    def resolve_hello(self, info):
        return "hello"


class AppMutation(ObjectType):
    registration = UserRegistrationMutation.Field()


graphql_schema = Schema(query=AppQuery, mutation=AppMutation)
