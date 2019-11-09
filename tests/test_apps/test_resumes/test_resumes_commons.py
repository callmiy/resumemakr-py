# -*- coding:utf-8 -*-

from server.apps.resumes.resumes_commons import (
    uniquify_resume_title,
    RESUME_TITLE_WITH_TIME,
)


def test_uniquify_title_with_no_time():
    title = "t1"
    unique_title = uniquify_resume_title(title)
    matched = RESUME_TITLE_WITH_TIME.match(unique_title)
    assert matched is not None
    assert matched.group(1) == title


def test_uniquify_title_with_time_part():
    title1 = uniquify_resume_title("ti")
    time1 = RESUME_TITLE_WITH_TIME.match(title1).group(2)
    title2 = uniquify_resume_title(title1)
    time2 = RESUME_TITLE_WITH_TIME.match(title2).group(2)
    assert time1 != time2
