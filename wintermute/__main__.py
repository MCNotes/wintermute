import aiohttp

from aiohttp import web

from gidgethub import routing, sansio
from gidgethub import aiohttp as gh_aiohttp

router = routing.Router()

# registering the appropriate coroutine
# event: representation of GH webhook's event (payload-> event.data)
# gh: gidgethub GH API
@router.register("issues", action="opened")
async def issue_opened_event(event, gh, *args, **kwargs):
    """ Whenever an issue is opened, greet the author and say thanks."""
    url = event.data["issue"]["comments_url"]
    author = event.data["issue"]["user"]["login"]

    message = f'🤖 Thanks for the report @{author}. I will have someone to look into this'

    await gh.post(url, data={"body": message})

#-------------------------
async def main(request):
    # Our bot coroutine
    body = await request.read()

    # our authentication token and secret
    secret = os.environ.get("GH_SECRET")
    oauth_token = os.environ.get("GH_AUTH")

    # a representation of the  GitHub webhook event
    event = sansio.Event.from_http(request.headers, body, secret=secret)

    # start a GH session
    async with aiohttp.ClientSession() as session:
        gh = gh_aiohttp.GitHubAPI(
            session,
            os.environ.get("GH_USERNAME"),
            oauth_token=oauth_token
        )

        # Give GitHub some time to reach internal consistency.
        await asyncio.sleep(1)

        # call the appropriate callback for the event
        await router.dispatch(event, gh)

    # if successful return OK code
    return web.Response(status=200)


if __name__ == "__main__":
    app = web.Application()

    # enables GitHub to send POST requests via the webhook
    app.router.add_post("/", main)
    port = os.environ.get("PORT")
    if port is not None:
        port = int(port)

    web.run_app(app, port=port)
