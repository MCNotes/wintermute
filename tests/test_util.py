import pytest
import json
import pathlib

from wintermute import util

from .test_review import example


def test_labels():
    # testing issues without label
    new_issue = example("issue.json")
    issue_labels = util.labels(new_issue)

    assert not issue_labels

    # testing issue with pre-review label
    new_issue = example("review_issue.json")
    issue_labels = util.labels(new_issue)

    assert len(issue_labels) == 2
    assert "pre-review" in issue_labels


def test_user_login():
    # getting the user login from a simple issue
    new_issue = example("issue.json")
    author = util.user_login(new_issue)

    assert "trallard" == author

    # getting the author of a comment in an issue
    data = {}
    data["issue"] = new_issue
    data["comment"] = example("issue_comments.json")
    author = util.user_login(data["comment"][0])

    assert "trallard" == author


