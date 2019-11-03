# -*- coding: utf-8 -*-

from graphene import ObjectType, Schema, String

from server.apps.accounts.accounts_graphql_schema import AccountsMutation


class AppQuery(ObjectType):
    hello = String()

    def resolve_hello(self, info):
        return "hello"


class AppMutation(AccountsMutation, ObjectType):
    pass


graphql_schema = Schema(query=AppQuery, mutation=AppMutation)
