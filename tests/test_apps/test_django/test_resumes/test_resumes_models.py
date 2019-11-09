# -*- coding: utf-8 -*-

import pytest


@pytest.mark.django_db
def test_create_resume_success(
    graphql_client, create_resume_query, registered_user
):  # noqa
    attrs = {"title": "resume 1"}

    result = graphql_client.execute(
        create_resume_query,
        variables={"input": attrs},
        context={"current_user": registered_user},
    )  # noqa

    resume = result["data"]["createResume"]["resume"]
    assert resume["title"] == "resume 1"
    assert resume["userId"] == str(registered_user.id)


@pytest.mark.django_db
def test_create_personal_info_success(
    create_personal_info_query, graphql_client
):  # noqa
    create_params = {"firstName": "kanmii"}
    return create_params
