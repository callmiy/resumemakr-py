# -*- coding: utf-8 -*-

import graphene


class TimestampsInterface(graphene.Interface):
    inserted_at = graphene.DateTime(required=True)
    updated_at = graphene.DateTime(required=True)
