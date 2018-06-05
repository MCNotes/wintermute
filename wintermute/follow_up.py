"""Follow up actions for the journal"""
import gidgethub.routing

router = gidgethub.routing.Router()

@router.register("pull_request", action="closed")
async def pr_closed_event(event, gh, *args, **kwargs):
    """When a PR has been closed, say thanks"""
    user = event.data["pull_request"]["user"]["login"]
    is_merged = event.data["pull_request"]["merged"]
    url = event.data["pull_request"]["comments_url"]
    if is_merged:
        message = f"Thanks for the PR @{user}"
        await gh.post(url, data={"body": message})