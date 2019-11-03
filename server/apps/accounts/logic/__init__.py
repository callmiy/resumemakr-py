from typing import Mapping

from .accounts_logic_django import AccountsLogicDjango

AccountsLogic = AccountsLogicDjango


def to_camel_case(key: str) -> str:
    first, *rest = key.split("_")
    return f"{first}{''.join(x.capitalize() for x in rest)}"


def user_params_to_graphql_variable(
    params: Mapping[str, str]
) -> Mapping[str, str]:  # noqa
    return {to_camel_case(x): params[x] for x in params}
