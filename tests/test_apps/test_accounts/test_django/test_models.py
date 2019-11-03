# -*- coding: utf-8 -*-

import pytest
from graphene.test import Client

from server.apps.accounts.logic import (
    AccountsLogic,
    user_params_to_graphql_variable,
)  # noqa

from server.apps.accounts.accounts_interfaces import (
    ATTRIBUTE_NOT_UNIQUE_ERROR_MESSAGE,
    USER_LOGIN_ERROR_MESSAGE,
)  # noqa


user_params = {
    "name": "kanmii",
    "email": "a@b.com",
    "password": "nicePWord",
    "password_confirmation": "nicePWord",
    "source": "password",
}  # noqa


@pytest.mark.django_db
def test_register_with_password_succeeds(
    graphql_client: Client, user_registration_query: str
) -> None:  # noqa
    variables = {"input": user_params_to_graphql_variable(user_params)}

    result = graphql_client.execute(
        user_registration_query, variables=variables
    )  # noqa

    registration = result["data"]["registration"]
    user = registration["user"]

    assert user["email"] == user_params["email"]
    assert type(user["jwt"]) == str
    assert registration["errors"] is None


@pytest.mark.django_db
def test_register_with_password_fails_cos_email_not_unique(
    graphql_client: Client, user_registration_query: str
) -> None:  # noqa
    AccountsLogic.register_user_with_password(user_params)

    variables = {"input": user_params_to_graphql_variable(user_params)}

    result = graphql_client.execute(
        user_registration_query, variables=variables
    )  # noqa

    registration = result["data"]["registration"]

    assert registration["errors"]["email"] == ATTRIBUTE_NOT_UNIQUE_ERROR_MESSAGE
    assert registration["user"] is None


@pytest.mark.django_db
def test_login_user_with_password_succeeds(login_query, graphql_client):
    login_params = {"email": "a@b.com", "password": "nicePWord"}
    AccountsLogic.register_user_with_password(user_params)

    result = graphql_client.execute(
        login_query, variables={"input": login_params}
    )  # noqa

    user = result["data"]["login"]["user"]

    assert user["email"] == user_params["email"]
    assert type(user["jwt"]) == str


@pytest.mark.django_db
def test_login_user_with_password_fails_cos_wrong_password(
    login_query, graphql_client
):  # noqa
    login_params = {"email": "a@b.com", "password": "bogusPassword"}
    AccountsLogic.register_user_with_password(user_params)

    result = graphql_client.execute(
        login_query, variables={"input": login_params}
    )  # noqa

    error = result["data"]["login"]["error"]

    assert error == USER_LOGIN_ERROR_MESSAGE


@pytest.mark.django_db
def test_login_user_with_password_fails_cos_user_not_found():
    login_params = {"email": "b@b.com", "password": "nicePassword"}
    AccountsLogic.register_user_with_password(user_params)
    result = AccountsLogic.login_with_password(login_params)

    assert result is None
