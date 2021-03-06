"""Handles the reviews to the journal"""
import re

import gidgethub.routing

from . import util

router = gidgethub.routing.Router()

REVIEW_CODES = ["PRE-REVIEW", "REVIEW"]
REVIEW_RE = re.compile(r"\[[A-Z]+\-*[A-Z]+\]")
NEW_ISSUE_COMMENT = (
    "Thanks for opening this issue @{user}. \n\n\n"
    "However, if this issue is related to the journal itself "
    "it should have been opened at"
    "[https://github.com/MCNotes/MCNotes.github.io/issues](https://github.com/MCNotes/MCNotes.github.io/issues)"
    "\n---"
    "\n\n 🤔 Do you want me to migrate this issue for you? "
    "Type in `sure thing` to migrate the issue or `nope` to do nothing. "
    "\n\n Note that the issue might get closed if not transferred."
)

PREREVIEW_COMMENT = (
    "Hi there! I am here to help sort out some editorial tasks."
    "First, I need to check that all the required files are in place"
    "Shall you need some help type `@wintermute help`"
)

REVIEW_COMMENT = (
    "### Instructions for the review "
)


@router.register("issues", action="opened")
@router.register("issues", action="reopened")
async def new_issue(event, gh, *args, **kwargs):
    """ Whenever an issue is opened, greet the author and say thanks."""
    issue = event.data["issue"]
    status_label_found = REVIEW_RE.search(issue["title"])

    if status_label_found:
        label = status_label_found.group().strip("[]")
        # generate the post request -> create label coroutine
        await gh.post(url=issue["labels_url"], data=[label])
    else:
        comments_url = issue["comments_url"]
        user = issue["user"]["login"]
        message = NEW_ISSUE_COMMENT.format(user=user)
        # generate post request -> create comment coroutine
        await gh.post(comments_url, data={"body": message})


def review_stage(issue):
    """Checks if this is a review or pre-review"""
    labels = util.labels(issue)

    if "pre-review" in labels:
        status = "pre-review"
        return status
    elif "review" in labels:
        status = "review"
        return status
    else:
        return None


@router.register("issue", action="labeled")
def start_review(event, gh, *args, **kwargs):
    """Decide what steps need to be followed. 
    This is entirely based on the label added by wintermute
    in previous steps
    """
    issue = event.data["issue"]
    status = review_stage(issue)
    if status == 'pre-review':
        pre_review_steps()
    elif status == 'review':
        review_steps()


async def pre_review_steps():
    """Starts pre-review and checks the files"""
    await gh.post(comments_url, data={"body": PREREVIEW_COMMENT})
    # TODO: add steps to verify the files

async def review_steps():
    """Starts pre-review and checks the files"""
    await gh.post(comments_url, data={"body": PREREVIEW_COMMENT})
    # TODO: add steps to verify the files