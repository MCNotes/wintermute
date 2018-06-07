import http
import json
import pathlib

import gidgethub
from gidgethub import sansio
import pytest

from wintermute import review


class FakeGH:
    def __init__(self, *, getiter=None, getitem=None, delete=None, post=None):
        self._getiter_return = getiter
        self._getitem_return = getitem
        self._delete_return = delete
        self._post_return = post
        self.getitem_url = None
        self.delete_url = None
        self.post_ = []

    async def getiter(self, url, url_vars={}):
        self.getiter_url = sansio.format_url(url, url_vars)
        to_iterate = self._getiter_return[self.getiter_url]
        for item in to_iterate:
            yield item

    async def getitem(self, url, url_vars={}):
        self.getitem_url = sansio.format_url(url, url_vars)
        to_return = self._getitem_return[self.getitem_url]
        if isinstance(to_return, Exception):
            raise to_return
        else:
            return to_return

    async def delete(self, url, url_vars={}):
        self.delete_url = sansio.format_url(url, url_vars)

    async def post(self, url, url_vars={}, *, data):
        post_url = sansio.format_url(url, url_vars)
        self.post_.append((post_url, data))
        self.post_data = data
        self.post_url = post_url


def example(file_name):
    """Opens one of the .json files stored in examples/github """
    this_dir = pathlib.Path(__file__).parent
    examples = this_dir / "examples" / "github"
    example = examples / file_name
    with example.open("r", encoding="utf-8") as file:
        return json.load(file)


async def test_new_issue():
    # testing on any issue- No review
    data = {"action": "opened"}
    data["issue"] = example("issue.json")
    data["comment"] = example("issue_comments.json")
    event = sansio.Event(data, event="issues", delivery_id="12345")

    gh = FakeGH()
    await review.router.dispatch(event, gh)
    post_data = gh.post_data

    assert len(gh.post_) == 1
    assert post_data["body"] == review.NEW_ISSUE_COMMENT.format(
        user=data["issue"]["user"]["login"]
    )

    # testing for PRE-REVIEW issues
    data = {"action": "opened"}
    data["issue"] = example("review_issue.json")
    event = sansio.Event(data, event="issues", delivery_id="12345")

    gh = FakeGH()
    await review.router.dispatch(event, gh)
    post_data = gh.post_data

    assert len(gh.post_) == 1
    post_ = gh.post_[0]
    assert post_[0] == "https://api.github.com/repos/MCNotes/MCNOTES-reviews/issues/5/labels"
    assert post_data == ["PRE-REVIEW"]


def test_review_stage():
    # Random label for issue
    issue = example("issue.json")
    issue["labels"] = [{"name": "bug"}]

    assert review.review_stage(issue) == None

    # Pre-review issue
    issue = example("review_issue.json")

    assert review.review_stage(issue) == "pre-review"