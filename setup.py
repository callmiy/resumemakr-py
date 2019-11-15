# -*- coding:utf-8 -*-

from setuptools import setup

setup(
    name="resumemakr",
    packages=setuptools.find_packages(),
    entry_points={
        "pytest11": [
            "name_of_plugin = resumemakr_pytest_plugins.pytest_django_run_first"
        ]
    },
)
