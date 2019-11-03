# -*- coding: utf-8 -*-

import pytest
from graphene.test import Client

from server.apps.accounts.logic import (
    AccountsLogic,
    user_params_to_graphql_variable,
)  # noqa

from server.apps.accounts.accounts_interfaces import (
    ATTRIBUTE_NOT_UNIQUE_ERROR_MESSAGE,
)  # noqa


user_params = {
    "name": "kanmii",
    "email": "a@b.com",
    "password": "nicePWord",
    "password_confirmation": "nicePWord",
    "source": "password",
}  # noqa


@pytest.mark.django_db
def test_login_user_with_password_succeeds():

    login_params = {"email": "a@b.com", "password": "nicePWord"}

    AccountsLogic.register_user_with_password(user_params)

    (user, credential) = AccountsLogic.login_with_password(login_params)
    assert user.email == "a@b.com"
    assert credential.source == "password"
    assert credential.token is not None


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
