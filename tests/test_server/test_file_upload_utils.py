# -*- coding: utf-8 -*-

import os

from server.apps.resumes.logic import ResumesLogic


def test_success(data_url_encoded_file, settings):
    url, saved_file_path = ResumesLogic.save_data_url_encoded_file(
        data_url_encoded_file
    )
    assert url.startswith(settings.MEDIA_URL)
    assert os.path.exists(saved_file_path)
    assert saved_file_path.endswith(".jpeg")
