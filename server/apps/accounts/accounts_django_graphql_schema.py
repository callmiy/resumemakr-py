# -*- coding: utf-8 -*-

import graphene

from graphene_django.types import DjangoObjectType
from server.apps.accounts.models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User


class Query(object):
    all_users = graphene.List(UserType)
