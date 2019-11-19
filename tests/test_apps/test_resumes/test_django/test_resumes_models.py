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
    CreateEducationAttrs,
    EducationLike,
    SkillLike,
    CreateSkillAttrs,
    CreateTextOnlyAttr,
    TextOnlyLike,
    TextOnlyEnumType,
    CreateExperienceAttrs,
    ExperienceLike,
    CreateRatableAttrs,
    Ratable,
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
    graphql_client,
    user_and_resume_fixture,
    get_resume_query,
    make_skill_fixture,
    make_education_fixture,
):
    user, resume = user_and_resume_fixture
    resume_id = str(resume.id)

    hobby = cast(
        TextOnlyLike,
        ResumesLogic.create_text_only(
            CreateTextOnlyAttr(
                tag=TextOnlyEnumType.resume_hobby,
                owner_id=resume_id,
                text="rh",  # noqa E501
            )
        ),
    )

    personal_info = cast(
        PersonalInfoLike,
        ResumesLogic.create_personal_info(
            CreatePersonalInfoAttrs(resume_id=resume_id, first_name="kanmii")
        ),
    )

    education = make_education_fixture(resume_id)

    education_achievement = cast(
        TextOnlyLike,
        ResumesLogic.create_text_only(
            CreateTextOnlyAttr(
                tag=TextOnlyEnumType.education_achievement,
                owner_id=education.id,
                text="ea",  # noqa E501
            )
        ),
    )

    skill = make_skill_fixture(resume_id)
    skill_achievement = cast(
        TextOnlyLike,
        ResumesLogic.create_text_only(
            CreateTextOnlyAttr(
                tag=TextOnlyEnumType.skill_achievement,
                owner_id=skill.id,
                text="sa",  # noqa E501
            )
        ),
    )

    experience = cast(
        ExperienceLike,
        ResumesLogic.create_experience(
            CreateExperienceAttrs(resume_id=resume_id, index=0)
        ),
    )

    experience_achievement = cast(
        TextOnlyLike,
        ResumesLogic.create_text_only(
            CreateTextOnlyAttr(
                tag=TextOnlyEnumType.experience_achievement,
                owner_id=experience.id,
                text="exa",  # noqa E501
            )
        ),
    )

    language = cast(
        Ratable,
        ResumesLogic.create_ratable(
            CreateRatableAttrs(
                owner_id=resume_id,
                tag=RatableEnumType.spoken_language,
                description="aa",
            )
        ),
    )

    supplementary_skill = cast(
        Ratable,
        ResumesLogic.create_ratable(
            CreateRatableAttrs(
                owner_id=resume_id,
                tag=RatableEnumType.supplementary_skill,
                description="bb",
            )
        ),
    )

    result = graphql_client.execute(
        get_resume_query,
        variables={"input": {"title": resume.title}},
        context=Context(current_user=user, app_data_loader=AppDataLoader()),
    )

    resume_map = result["data"]["getResume"]
    assert resume_map["id"] == resume_id
    assert resume_map["personalInfo"]["id"] == str(personal_info.id)

    education_obj = resume_map["educations"][0]
    assert education_obj["id"] == str(education.id)

    education_achievement_obj = education_obj["achievements"][0]
    assert education_achievement_obj["id"] == str(education_achievement.id)

    skill_obj = resume_map["skills"][0]
    assert skill_obj["id"] == str(skill.id)
    skill_achievement_obj = skill_obj["achievements"][0]
    assert skill_achievement_obj["id"] == str(skill_achievement.id)

    hobby_obj = resume_map["hobbies"][0]
    assert hobby_obj["id"] == str(hobby.id)

    experience_obj = resume_map["experiences"][0]
    assert experience_obj["id"] == str(experience.id)
    experience_achievement_obj = experience_obj["achievements"][0]
    assert experience_achievement_obj["id"] == str(experience_achievement.id)

    language_obj = resume_map["languages"][0]
    assert language_obj["id"] == str(language.id)

    supplementary_skill_obj = resume_map["supplementarySkills"][0]
    assert supplementary_skill_obj["id"] == str(supplementary_skill.id)


def test_create_resume_hobby_succeeds(
    user_and_resume_fixture, create_text_only_query, graphql_client
):
    user, resume = user_and_resume_fixture
    resume_id = str(resume.id)

    result = graphql_client.execute(
        create_text_only_query,
        variables={"ownerId": resume_id, "text": "aa"},
        context=Context(current_user=user, app_data_loader=AppDataLoader()),
    )

    hobby = result["data"]["createTextOnly"]["textOnly"]

    assert hobby["ownerId"] == resume_id
    assert hobby["tag"] == TextOnlyEnumType.resume_hobby.name


def test_create_resume_child_text_only_child_succeeds(
    user_and_resume_fixture,
    create_text_only_query,
    graphql_client,
    make_education_fixture,
    make_experience_fixture,
    make_skill_fixture,
):
    user, resume = user_and_resume_fixture
    resume_id = str(resume.id)

    for fixture_fn, tag_name in (
        (make_education_fixture, TextOnlyEnumType.education_achievement.name,),
        (make_skill_fixture, TextOnlyEnumType.skill_achievement.name,),
        (
            make_experience_fixture,
            TextOnlyEnumType.experience_achievement.name,
        ),  # noqa E501
    ):

        owner = fixture_fn(resume_id)

        owner_id_str = str(owner.id)

        result = graphql_client.execute(
            create_text_only_query,
            variables={"ownerId": owner_id_str, "text": "aa"},
            context=Context(current_user=user, app_data_loader=AppDataLoader()),
        )

        text_only_obj = result["data"]["createTextOnly"]["textOnly"]

        assert text_only_obj["ownerId"] == owner_id_str
        assert text_only_obj["tag"] == tag_name
