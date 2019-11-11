# -*- coding: utf-8 -*-

from collections import namedtuple
from typing import cast

import pytest

from server.apps.resumes.logic import ResumesLogic
from server.apps.resumes.resumes_commons import (
    CreateResumeAttrs,
    CreatePersonalInfoAttrs,
    CreateResumeComponentErrors,
    CreateExperienceAttrs,
    CreateEducationAttrs,
    CreateSkillAttrs,
)

pytestmark = pytest.mark.django_db

Context = namedtuple("Context", ("current_user",))
BogusUser = namedtuple("BogusUser", ("id",))


def test_create_resume_succeeds(
    graphql_client, create_resume_query, registered_user
):  # noqa
    title = "t 12"
    attrs = {"title": title}

    result = graphql_client.execute(
        create_resume_query,
        variables={"input": attrs},
        context=Context(current_user=registered_user),
    )  # noqa

    resume = result["data"]["createResume"]["resume"]
    assert resume["title"] == title
    assert resume["userId"] == str(registered_user.id)


def test_create_resume_with_non_unique_title_succeeds(registered_user):
    title = "title 1"
    resume1 = ResumesLogic.create_resume(
        CreateResumeAttrs(title=title, user_id=str(registered_user.id))
    )

    assert resume1.title == title

    resume2 = ResumesLogic.create_resume(
        CreateResumeAttrs(title=title, user_id=str(registered_user.id))
    )

    assert resume2.title.index(title) > -1


def test_create_personal_info_no_photo_succeeds(
    create_personal_info_query, graphql_client, user_and_resume_fixture
):  # noqa
    user, resume = user_and_resume_fixture
    resume_id = str(resume.id)

    create_params = {"firstName": "kanmii", "resumeId": resume_id}

    result = graphql_client.execute(
        create_personal_info_query,
        variables={"input": create_params},
        context=Context(current_user=user),
    )

    personal_info = result["data"]["createPersonalInfo"]["personalInfo"]

    assert personal_info["firstName"] == "kanmii"
    assert personal_info["resumeId"] == resume_id


def test_create_personal_info_with_photo_succeeds(
    create_personal_info_query,
    graphql_client,
    user_and_resume_fixture,
    data_url_encoded_file,
    settings,
):  # noqa
    user, resume = user_and_resume_fixture
    resume_id = str(resume.id)

    create_params = {
        "firstName": "kanmii",
        "resumeId": resume_id,
        "photo": data_url_encoded_file,
    }  # noqa

    result = graphql_client.execute(
        create_personal_info_query,
        variables={"input": create_params},
        context=Context(current_user=user),
    )

    personal_info = result["data"]["createPersonalInfo"]["personalInfo"]
    photo = personal_info["photo"]

    assert photo.startswith(settings.MEDIA_URL)
    assert photo.endswith(".jpeg")


def test_create_personal_info_fails_cos_resume_not_found(
    create_personal_info_query, graphql_client, bogus_uuid
):  # noqa

    create_params = {"firstName": "kanmii", "resumeId": bogus_uuid}

    result = graphql_client.execute(
        create_personal_info_query,
        variables={"input": create_params},
        context=Context(current_user=BogusUser(id=bogus_uuid)),
    )

    assert type(result["data"]["createPersonalInfo"]["errors"]["resume"]) == str


def test_create_personal_info_fails_due_to_exception():
    attrs = cast(CreatePersonalInfoAttrs, {})
    result = cast(
        CreateResumeComponentErrors, ResumesLogic.create_personal_info(attrs)
    )  # noqa
    assert type(result.error) == str


def test_create_experience_succeeds(
    graphql_client, create_experience_query, user_and_resume_fixture
):
    user, resume = user_and_resume_fixture
    resume_id = str(resume.id)

    params = {"resumeId": resume_id, "index": 1, "position": "pos 1"}

    result = graphql_client.execute(
        create_experience_query,
        variables={"input": params},
        context=Context(current_user=user),
    )

    experience = result["data"]["createExperience"]["experience"]
    assert experience["resumeId"] == resume_id
    assert experience["index"] == 1


def test_create_experience_fails_cos_resume_not_found(
    graphql_client, create_experience_query, bogus_uuid
):

    params = {"resumeId": bogus_uuid, "index": 1, "position": "pos 1"}

    result = graphql_client.execute(
        create_experience_query,
        variables={"input": params},
        context=Context(current_user=BogusUser(id=bogus_uuid)),
    )

    errors = result["data"]["createExperience"]["errors"]
    assert type(errors["resume"]) == str


def test_create_experience_fails_due_to_exception():
    attrs = cast(CreateExperienceAttrs, {})

    result = cast(
        CreateResumeComponentErrors, ResumesLogic.create_experience(attrs)
    )  # noqa
    assert type(result.error) == str


def test_create_education_succeeds(
    graphql_client, create_education_query, user_and_resume_fixture
):
    user, resume = user_and_resume_fixture
    resume_id = str(resume.id)

    params = {"resumeId": resume_id, "index": 1, "school": "school 1"}

    result = graphql_client.execute(
        create_education_query,
        variables={"input": params},
        context=Context(current_user=user),
    )

    education = result["data"]["createEducation"]["education"]
    assert education["resumeId"] == resume_id
    assert education["index"] == 1


def test_create_education_fails_cos_resume_not_found(
    graphql_client, create_education_query, bogus_uuid
):

    params = {"resumeId": bogus_uuid, "index": 1, "school": "school 1"}

    result = graphql_client.execute(
        create_education_query,
        variables={"input": params},
        context=Context(current_user=BogusUser(id=bogus_uuid)),
    )

    errors = result["data"]["createEducation"]["errors"]
    assert type(errors["resume"]) == str


def test_create_education_fails_due_to_exception():
    attrs = cast(CreateEducationAttrs, {})

    result = cast(
        CreateResumeComponentErrors, ResumesLogic.create_education(attrs)
    )  # noqa
    assert type(result.error) == str


############################ title ############################## noqa
def test_create_skill_succeeds(
    graphql_client, create_skill_query, user_and_resume_fixture
):
    user, resume = user_and_resume_fixture
    resume_id = str(resume.id)

    params = {"resumeId": resume_id, "index": 1, "description": "d 1"}

    result = graphql_client.execute(
        create_skill_query,
        variables={"input": params},
        context=Context(current_user=user),
    )

    skill = result["data"]["createSkill"]["skill"]
    assert skill["resumeId"] == resume_id
    assert skill["index"] == 1


def test_create_skill_fails_cos_resume_not_found(
    graphql_client, create_skill_query, bogus_uuid
):

    params = {"resumeId": bogus_uuid, "index": 1, "description": "d 1"}

    result = graphql_client.execute(
        create_skill_query,
        variables={"input": params},
        context=Context(current_user=BogusUser(id=bogus_uuid)),
    )

    errors = result["data"]["createSkill"]["errors"]
    assert type(errors["resume"]) == str


def test_create_skill_fails_due_to_exception():
    attrs = cast(CreateSkillAttrs, {})

    result = cast(CreateResumeComponentErrors, ResumesLogic.create_skill(attrs))
    assert type(result.error) == str

