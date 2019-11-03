# -*- coding: utf-8 -*-


def test_root_url(client):
    """This test ensures that root url works."""
    response = client.get("/")

    assert response.status_code == 200
