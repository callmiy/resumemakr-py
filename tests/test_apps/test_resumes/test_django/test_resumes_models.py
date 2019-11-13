# -*- coding: utf-8 -*-

from typing import cast, NamedTuple

import pytest
from graphene import Context

from server.apps.resumes.logic import ResumesLogic
from server.apps.resumes.resumes_commons import (  # noqa
    CreatePersonalInfoAttrs,
    CreateResumeAttrs,
    PersonalInfoLike,
    RatableEnumType,
)
from server.data_loader import AppDataLoader

pytestmark = pytest.mark.django_db


class BogusUser(NamedTuple):
    id: str


def test_create_resume_succeeds(
    graphql_client, create_resume_query, registered_user
):  # noqa
    title = "t 12"
    attrs = {"title": title}

    result = graphql_client.execute(
        create_resume_query,
        variables={"input": attrs},
        context=Context(
            current_user=registered_user, app_data_loader=AppDataLoader()
        ),  # noqa
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


def test_create_spoken_languages_succeeds(
    graphql_client, create_ratable_query, user_and_resume_fixture
):
    user, resume = user_and_resume_fixture
    resume_id = str(resume.id)

    params = {
        "ownerId": resume_id,
        "description": "d 1",
        "tag": RatableEnumType.spoken_language.name,
    }

    result = graphql_client.execute(
        create_ratable_query,
        variables={"input": params},
        context=Context(current_user=user),
    )

    spoken_language = result["data"]["createRatable"]["ratable"]
    assert spoken_language["ownerId"] == resume_id
    assert spoken_language["tag"] == RatableEnumType.spoken_language.name


def test_create_spoken_languages_fails_cos_resume_not_found(
    graphql_client, create_ratable_query, bogus_uuid
):

    params = {
        "ownerId": bogus_uuid,
        "description": "d 1",
        "tag": RatableEnumType.spoken_language.name,
    }

    result = graphql_client.execute(
        create_ratable_query,
        variables={"input": params},
        context=Context(current_user=BogusUser(id=bogus_uuid)),
    )

    errors = result["data"]["createRatable"]["errors"]
    assert type(errors["owner"]) == str
    assert errors["tag"] == RatableEnumType.spoken_language.name


def test_create_supplementary_skill_succeeds(
    graphql_client, create_ratable_query, user_and_resume_fixture
):
    user, resume = user_and_resume_fixture
    resume_id = str(resume.id)

    params = {
        "ownerId": resume_id,
        "description": "d 1",
        "tag": RatableEnumType.supplementary_skill.name,
    }

    result = graphql_client.execute(
        create_ratable_query,
        variables={"input": params},
        context=Context(current_user=user),
    )

    spoken_language = result["data"]["createRatable"]["ratable"]
    assert spoken_language["ownerId"] == resume_id
    assert spoken_language["tag"] == RatableEnumType.supplementary_skill.name


def test_create_supplementary_skill_fails_cos_resume_not_found(
    graphql_client, create_ratable_query, bogus_uuid
):

    params = {
        "ownerId": bogus_uuid,
        "description": "d 1",
        "tag": RatableEnumType.supplementary_skill.name,
    }

    result = graphql_client.execute(
        create_ratable_query,
        variables={"input": params},
        context=Context(current_user=BogusUser(id=bogus_uuid)),
    )

    errors = result["data"]["createRatable"]["errors"]
    assert type(errors["owner"]) == str
    assert errors["tag"] == RatableEnumType.supplementary_skill.name


def test_get_all_resume_fields_succeeds(
    graphql_client, user_and_resume_fixture, get_resume_query
):  # noqa
    user, resume = user_and_resume_fixture
    resume_id = str(resume.id)

    _personal_info = ResumesLogic.create_personal_info(
        CreatePersonalInfoAttrs(resume_id=resume_id, first_name="kanmii")
    )

    personal_info = cast(PersonalInfoLike, _personal_info)

    result = graphql_client.execute(
        get_resume_query,
        variables={"input": {"title": resume.title}},
        context=Context(current_user=user, app_data_loader=AppDataLoader()),
    )

    resume_map = result["data"]["getResume"]
    assert resume_map["id"] == resume_id
    assert resume_map["personalInfo"]["id"] == str(personal_info.id)
