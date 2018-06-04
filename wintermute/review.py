"""Handles the reviews to the journal"""
import gidgethub.routing

router = gidgethub.routing.Router()

REVIEW_CODES = ["PRE REVIEW", "REVIEW"]


@router.register("issues", action="opened")
@router.register("issues", action="reopened")
async def issue_opened_event(event, gh, *args, **kwargs):
    """ Whenever an issue is opened, greet the author and say thanks."""
    issue = event.data["issue"]

    if issue["title"].strip() in REVIEW_CODES:
        await gh.post(issue["labels_url"], data=["pre review"])
    else:
        url = issue["comments_url"]
        user = issue["user"]["login"]
        message = (
            f"Thanks for opening the issue @{user}, will look into it (I'm a bot 🤖)"
        )
        await gh.post(url, data={"body": message})


@router.register("issue_comment", action="created")
async def issue_comment_created_event(event, gh, *args, **kwargs):
    """Thumbs up for my own issue comment"""
    url = f"{event.data['comment']['url']}/reactions"
    user = event.data["comment"]["user"]["login"]
    if user == "trallard":
        await gh.post(
            url,
            data={"content": "+1"},
            accept="application/vnd.github.squirrel-girl-preview+json",
        )
