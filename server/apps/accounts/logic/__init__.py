from typing import Mapping

from server.apps.accounts.accounts_commons import UserLike, MaybeUser
from server.apps.jwt_utils.jwt_utils import JwtManager

from .accounts_logic_django import AccountsLogicDjango

AccountsLogic = AccountsLogicDjango


def to_camel_case(key: str) -> str:
    first, *rest = key.split("_")
    return f"{first}{''.join(x.capitalize() for x in rest)}"


def user_params_to_graphql_variable(
    params: Mapping[str, str]
) -> Mapping[str, str]:  # noqa
    return {to_camel_case(x): params[x] for x in params}


def user_to_jwt(user: UserLike) -> str:
    return JwtManager.to_jwt({"user": str(user.id)})


def user_from_jwt(jwt: str) -> MaybeUser:
    user_id = JwtManager.from_jwt(jwt)["user"]
    return AccountsLogic.get_user_by_id(user_id)
