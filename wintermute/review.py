"""Handles the reviews to the journal"""

from gidgethub import routing

router = routing.Router()

REVIEW_CODES = [
    "PRE REVIEW",
    "REVIEW",
]


@router.register("issues", action="opened")
@router.register("issues", action="reopened")
async def issue_opened_event(event, gh, *args, **kwargs):
    """ Whenever an issue is opened, greet the author and say thanks."""
    issue = event.data["issue"]

    if issue["title"].strip() in REVIEW_CODES:
        await gh.post(issue['labels_url'], data=['pre review'])
    else:
        url = issue["comments_url"]
        user = issue["user"]["login"]
        message = f"Thanks for opening the issue @{user}, will look into it (I'm a bot 🤖)"
        await gh.post(url, data={"body": message})