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

from server.apps.accounts.logic import AccountsLogic
from server.apps.graphql_schema import graphql_schema
from server.apps.resumes.logic import ResumesLogic
from server.file_upload_utils import data_url_encoded_string_delimiter

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

personal_info_fragment_name = "PersonalInfoFragment"


timestamps_fragment = """
    insertedAt
    updatedAt
"""


@pytest.fixture()
def test_root():
    return PurePath(os.path.abspath(__file__)).parent


@pytest.fixture()
def graphql_client():
    return Client(graphql_schema)


@pytest.fixture()
def data_url_encoded_file(settings, test_root):
    with open(test_root.joinpath("test-files/dog.jpeg"), "rb") as dog_file:
        dog_string = base64.urlsafe_b64encode(dog_file.read()).decode()
        return f"data:image/jpeg{data_url_encoded_string_delimiter}{dog_string}"


@pytest.fixture()
def create_user_params():
    return {
        "name": "kanmii",
        "email": "a@b.com",
        "password": "nicePWord",
        "password_confirmation": "nicePWord",
        "source": "password",
    }


@pytest.fixture()
def registered_user(db, create_user_params):
    user_credential = AccountsLogic.register_user_with_password(
        create_user_params
    )  # noqa
    return user_credential[0]


@pytest.fixture()
def user_and_resume_fixture(registered_user):
    resume = ResumesLogic.create_resume(
        dict(user_id=registered_user.id, title="title 1")
    )  # noqa
    return (registered_user, resume)


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
            {timestamps_fragment}
        }}
    """


@pytest.fixture()
def create_resume_query(resume_fragment):
    return f"""
        mutation CreateResume($input: CreateResumeInput!) {{
            createResume(input: $input) {{
                {typename}

                ... on ResumeSuccess {{
                   resume {{
                        ...{resume_fragment_name}
                   }}
                }}

                ... on CreateResumeErrors {{
                    errors
                }}
            }}
        }}

        {resume_fragment}
    """


@pytest.fixture()
def personal_info_fragment():
    return f"""
        fragment {personal_info_fragment_name} on PersonalInfo {{
            id
            firstName
            lastName
            profession
            address
            email
            phone
            photo
            dateOfBirth
            resumeId
        }}
    """


@pytest.fixture()
def create_personal_info_query(personal_info_fragment):
    return f"""
        mutation CreatePersonalInfo($input: CreatePersonalInfoInput!) {{
            createPersonalInfo(input: $input) {{
                {typename}

                ... on PersonalInfoSuccess {{
                    personalInfo {{
                        ...{personal_info_fragment_name}
                    }}
                }}

                ... on CreatePersonalInfoErrors {{
                    errors {{
                        resume
                        error
                    }}
                }}
            }}
        }}

        {personal_info_fragment}
    """


@pytest.fixture()
def bogus_uuid():
    return "746d6853-f7b4-4525-bfd0-37af7370c7cb"
