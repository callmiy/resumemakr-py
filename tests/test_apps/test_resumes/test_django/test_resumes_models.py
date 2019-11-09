# -*- coding: utf-8 -*-

import pytest

from server.apps.resumes.logic import ResumesLogic
from server.apps.resumes.resumes_commons import CreateResumeAttrs


@pytest.mark.django_db
def test_create_resume_success(
    graphql_client, create_resume_query, registered_user
):  # noqa
    title = "t 12"
    attrs = {"title": title}

    result = graphql_client.execute(
        create_resume_query,
        variables={"input": attrs},
        context={"current_user": registered_user},
    )  # noqa

    resume = result["data"]["createResume"]["resume"]
    assert resume["title"] == title
    assert resume["userId"] == str(registered_user.id)


@pytest.mark.django_db
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


@pytest.mark.django_db
def test_create_personal_info_success(
    create_personal_info_query, graphql_client
):  # noqa
    create_params = {"firstName": "kanmii"}
    return create_params
