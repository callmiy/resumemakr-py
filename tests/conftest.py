# -*- coding: utf-8 -*-

"""
This module is used to provide configuration, fixtures, and plugins for pytest.

It may be also used for extending doctest's context:
1. https://docs.python.org/3/library/doctest.html
2. https://docs.pytest.org/en/latest/doctest.html
"""

import pytest
from graphene.test import Client

from server.apps.graphql_schema import graphql_schema


user_fragment_name = "UserFragment"

user_fragment = f"""
      fragment {user_fragment_name} on User {{
            id
            name
            email
            jwt
            insertedAt
            updatedAt
      }}
    """


@pytest.fixture(autouse=True)
def _media_root(settings, tmpdir_factory):
    """Forces django to save media files into temp folder."""
    settings.MEDIA_ROOT = tmpdir_factory.mktemp("media", numbered=True)


@pytest.fixture(autouse=True)
def _password_hashers(settings):
    """Forces django to use fast password hashers for tests."""
    settings.PASSWORD_HASHERS = [
        "django.contrib.auth.hashers.MD5PasswordHasher"
    ]  # noqa


@pytest.fixture(autouse=True)
def _auth_backends(settings):
    """Deactivates security backend from Axes app."""
    settings.AUTHENTICATION_BACKENDS = (
        "django.contrib.auth.backends.ModelBackend",
    )  # noqa


@pytest.fixture()
def graphql_client():
    return Client(graphql_schema)


@pytest.fixture()
def user_registration_query():

    return f"""
        mutation RegisterUser($input: RegistrationInput!) {{
            registration(input: $input) {{
                user {{
                    ...{user_fragment_name}
                }}

                errors {{
                    email
                }}
            }}

        }}

        {user_fragment}
    """


@pytest.fixture()
def login_query():
    return f"""
        mutation LoginUser($input: LoginInput!) {{
            login(input: $input) {{
                __typename

                ... on UserSuccess {{
                    user {{
                        ...{user_fragment_name}
                    }}
                }}

                ... on LoginUserError {{
                    error
                }}
            }}
        }}

        {user_fragment}
    """
