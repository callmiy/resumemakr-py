# -*- coding:utf-8 -*-

import os

import pytest


@pytest.hookimpl(tryfirst=True)
def pytest_load_initial_conftests(early_config, parser, args):
    os.environ["DJANGO_ENV"] = "test"
