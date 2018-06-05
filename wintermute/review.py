"""Handles the reviews to the journal"""
import re

import gidgethub.routing

router = gidgethub.routing.Router()

REVIEW_CODES = ["PRE-REVIEW", "REVIEW"]
REVIEW_RE = re.compile(r"\[[A-Z]+\-*[A-Z]+\]")


@router.register("issues", action="opened")
@router.register("issues", action="reopened")
async def new_issue(event, gh, *args, **kwargs):
    """ Whenever an issue is opened, greet the author and say thanks."""
    issue = event.data["issue"]
    status_label_found = REVIEW_RE.search(issue["title"])

    if status_label_found:
        label = status_label_found.group().strip("[]")
        await gh.post(issue["labels_url"], data=[label])

    else:
        comments_url = issue["comments_url"]
        user = issue["user"]["login"]
        message = (
            f" 🤖 Thanks for opening this issue @{user}. \n\n\n"
            f"However, if this issue is related to the journal itself "
            f"you should open an issue at"
            f"[https://github.com/MCNotes/MCNotes.github.io/issues](https://github.com/MCNotes/MCNotes.github.io/issues)"
        )
        await gh.post(comments_url, data={"body": message})


@router.register("issue_comment", action="created")
async def new_issue_comment(event, gh, *args, **kwargs):
    """Thumbs up for my own issue comment"""
    url = f"{event.data['comment']['url']}/reactions"
    user = event.data["comment"]["user"]["login"]
    if user == "trallard":
        await gh.post(
            url,
            data={"content": "+1"},
            accept="application/vnd.github.squirrel-girl-preview+json",
        )


@router.register("pull_request", action="closed")
async def pr_closed_event(event, gh, *args, **kwargs):
    """When a PR has been closed, say thanks"""
    user = event.data["pull_request"]["user"]["login"]
    is_merged = event.data["pull_request"]["merged"]
    url = event.data["pull_request"]["comments_url"]
    if is_merged:
        message = f"Thanks for the PR @{user}"
        await gh.post(url, data={"body": message})
