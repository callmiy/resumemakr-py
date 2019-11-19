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

from logics.accounts import AccountsLogic
from logics.graphql_schema import graphql_schema
from logics.resumes import ResumesLogic
from logics.resumes.resumes_types import (
    CreateSkillAttrs,
    CreateEducationAttrs,
    CreateExperienceAttrs,
)
from logics.logics_utils import data_url_encoded_string_delimiter

typename = "__typename"
user_fragment_name = "UserFragment"
resume_fragment_name = "ResumeFragment"
personal_info_fragment_name = "PersonalInfoFragment"
experience_fragment_name = "ExperienceFragment"
education_fragment_name = "EducationFragment"
skill_fragment_name = "SkillFragment"


ratable_attributes = """
   id
   ownerId
   description
   tag
   level
"""


text_only_fragment = f"""
    {typename}
    id
    text
    ownerId
"""


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
def bogus_uuid():
    return "746d6853-f7b4-4525-bfd0-37af7370c7cb"


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
def user_fragment():
    return f"""
      fragment {user_fragment_name} on User {{
            id
            name
            email
            jwt
            insertedAt
            updatedAt
      }}
    """


@pytest.fixture()
def user_registration_query(user_fragment):

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
def login_query(user_fragment):
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
def education_fragment():
    return f"""
        fragment {education_fragment_name} on Education {{
           id
           resumeId
           index
           course
           school
           fromDate
           toDate

           achievements {{
               {text_only_fragment}
           }}
        }}
    """


@pytest.fixture()
def skill_fragment():
    return f"""
        fragment {skill_fragment_name} on Skill {{
           id
           resumeId
           index
           description
        }}
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

            personalInfo {{
                id
                resumeId
            }}

            educations {{
                id
                resumeId
                achievements {{
                    {text_only_fragment}
                }}
            }}

            skills {{
                id
                resumeId
                achievements {{
                    {text_only_fragment}
                }}
            }}

            hobbies {{
                {text_only_fragment}
            }}

            experiences {{
                id
                resumeId
                achievements {{
                    {text_only_fragment}
                }}
            }}

            languages {{
                {ratable_attributes}
            }}

            supplementarySkills {{
                {ratable_attributes}
            }}
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
def get_resume_query(resume_fragment):
    return f"""
        query GetResume($input: GetResumeInput!) {{
            getResume(input: $input) {{
                ...{resume_fragment_name}
            }}
        }}
        {resume_fragment}
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
def experience_fragment():
    return f"""
        fragment {experience_fragment_name} on Experience {{
           id
           resumeId
           index
           position
           companyName
           fromDate
           toDate
        }}
    """


@pytest.fixture()
def create_experience_query(experience_fragment):
    return f"""
        mutation CreateExperience($input: CreateExperienceInput!) {{
            createExperience(input: $input) {{

                {typename}

                ... on ExperienceSuccess {{
                    experience {{
                        ...{experience_fragment_name}
                    }}
                }}

                ... on CreateExperienceErrors {{
                    errors {{
                        resume
                        error
                    }}
                }}
            }}
        }}
        {experience_fragment}
    """


@pytest.fixture()
def create_education_query(education_fragment):
    return f"""
        mutation CreateEducation($input: CreateEducationInput!) {{
            createEducation(input: $input) {{

                {typename}

                ... on EducationSuccess {{
                    education {{
                        ...{education_fragment_name}
                    }}
                }}

                ... on CreateEducationErrors {{
                    errors {{
                        resume
                        error
                    }}
                }}
            }}
        }}
        {education_fragment}
    """


@pytest.fixture()
def create_skill_query(skill_fragment):
    return f"""
        mutation CreateSkill($input: CreateSkillInput!) {{
            createSkill(input: $input) {{

                {typename}

                ... on SkillSuccess {{
                    skill {{
                        ...{skill_fragment_name}
                    }}
                }}

                ... on CreateSkillErrors {{
                    errors {{
                        resume
                        error
                    }}
                }}
            }}
        }}
        {skill_fragment}
    """


@pytest.fixture()
def create_ratable_query():
    return f"""
        mutation CreateRatable($input: CreateRatableInput!) {{
            createRatable(input: $input) {{

                {typename}

                ... on RatableSuccess {{
                    ratable {{
                       {ratable_attributes}
                    }}
                }}

                ... on CreateRatableErrors {{
                    errors {{
                        owner
                        error
                        tag
                    }}
                }}
            }}
        }}
    """


@pytest.fixture()
def create_text_only_query():
    return f"""
        mutation CreateTextOnly($input: CreateTextOnlyInput!) {{
            createTextOnly(input: $input) {{
                {typename}

                ... on TextOnlySuccess {{
                    textOnly {{
                        {text_only_fragment}
                    }}
                }}

                ... on CreateTextOnlyErrors {{
                    errors {{
                        owner
                        tag
                        error
                    }}
                }}
            }}
        }}
    """


@pytest.fixture()
def make_skill_fixture():
    def create_skill(resume_id, index=0):
        return ResumesLogic.create_skill(
            CreateSkillAttrs(resume_id=resume_id, index=index)
        )  # noqa E501

    return create_skill


@pytest.fixture()
def make_education_fixture():
    def create_education(resume_id, index=0):
        return ResumesLogic.create_education(
            CreateEducationAttrs(resume_id=resume_id, index=index)
        )  # noqa E501

    return create_education


@pytest.fixture()
def make_experience_fixture():
    def create_experience(resume_id, index=0):
        experience = ResumesLogic.create_experience(
            CreateExperienceAttrs(resume_id=resume_id, index=index)
        )  # noqa E501

        return experience

    return create_experience
