# -*- coding: utf-8 -*-

"""
This module is used to provide configuration, fixtures, and plugins for pytest.

It may be also used for extending doctest's context:
1. https://docs.python.org/3/library/doctest.html
2. https://docs.pytest.org/en/latest/doctest.html
"""

import base64
import os
from pathlib import PurePath

import pytest
from graphene.test import Client

from server.file_upload_utils import data_url_encoded_string_delimiter
from server.apps.graphql_schema import graphql_schema

typename = "__typename"

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


resume_fragment_name = "ResumeFragment"


@pytest.fixture()
def test_root():
    return PurePath(os.path.abspath(__file__)).parent


@pytest.fixture(autouse=True)
def _media_root(settings, test_root):
    """Forces django to save media files into custom location."""
    settings.MEDIA_ROOT = test_root.joinpath("media")


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
def data_url_encoded_file(settings, test_root):
    with open(test_root.joinpath("test-files/dog.jpeg"), "rb") as dog_file:
        dog_string = base64.urlsafe_b64encode(dog_file.read()).decode()
        return f"data:image/jpeg{data_url_encoded_string_delimiter}{dog_string}"


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
               {typename}

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


@pytest.fixture()
def resume_fragment():
    return f"""
        fragment {resume_fragment_name} on Resume {{
            id
            title
            description
            userId
        }}
    """


@pytest.fixture()
def create_resume_query(resume_fragment):
    return f"""
        mutation CreateResume($input: CreateResumeInput!) {{
            createResume(input: $input) {{
                {typename}

                ... on ResumeSuccess {{
                    ...{resume_fragment_name}
                }}

                ... on CreateResumeErrors {{
                    errors
                }}
            }}
        }}

        {resume_fragment}
    """


@pytest.fixture()
def create_personal_info_query():
    return f"""
    """
