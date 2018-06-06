"""Handles the reviews to the journal"""
import re

import gidgethub.routing

router = gidgethub.routing.Router()

REVIEW_CODES = ["PRE-REVIEW", "REVIEW"]
REVIEW_RE = re.compile(r"\[[A-Z]+\-*[A-Z]+\]")
NEW_ISSUE_COMMENT = (
    " 🤖 Thanks for opening this issue @{user}. \n\n\n"
    "However, if this issue is related to the journal itself "
    "you should open an issue at "
    "[https://github.com/MCNotes/MCNotes.github.io/issues](https://github.com/MCNotes/MCNotes.github.io/issues)"
    "\n\n Do you want me to migrate this issue for you? "
    "Type in `sure thing` to migrate the issue or `nope` to do nothing"
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

