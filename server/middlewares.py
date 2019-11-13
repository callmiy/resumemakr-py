# -*- coding: utf-8 -*-

from server.apps.accounts.logic import user_from_jwt
from server.data_loader import AppDataLoader


def set_grapnhql_context_middleware(get_response):
    def middleware(request):
        setattr(request, "app_data_loader", AppDataLoader())
        authorization = request.headers.get("Authorization")

        if authorization is None:
            return get_response(request)

        prefix_jwt = authorization.split()

        if len(prefix_jwt) != 2:
            return get_response(request)

        if prefix_jwt[0] != "Bearer":
            return get_response(request)

        setattr(request, "current_user", user_from_jwt(prefix_jwt[1]))
        return get_response(request)

    return middleware
