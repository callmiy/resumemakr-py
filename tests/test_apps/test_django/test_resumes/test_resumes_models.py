# -*- coding: utf-8 -*-

import pytest


@pytest.mark.django_db
def test_create_resume_success(
    graphql_client, create_resume_query, registered_user
):  # noqa
    attrs = {"title": "resume 1", "userId": registered_user.id}
    variables = {"input": attrs}
    result = graphql_client.execute(create_resume_query, variables=variables)
    resume = result["data"]["resume"]
    assert resume["title"] == "resume 1"
    assert resume["userId"] == registered_user.id


@pytest.mark.django_db
def test_create_personal_info_success(
    create_personal_info_query, graphql_client
):  # noqa
    create_params = {"firstName": "kanmii"}
