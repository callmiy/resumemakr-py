# -*- coding: utf-8 -*-

import pytest

from server.apps.accounts.logic.accounts_logic_django import AccountsLogic


@pytest.mark.django_db
def test_login_user_with_password_succeeds():
    user_params = {
        "name": "kanmii",
        "email": "a@b.com",
        "password": "nicePWord",
    }  # noqa

    login_params = {"email": "a@b.com", "password": "nicePWord"}

    AccountsLogic.register_user_with_password(user_params)

    (user, credential) = AccountsLogic.login_with_password(login_params)
    assert user.email == "a@b.com"
    assert credential.source == "password"
    assert credential.token is not None
