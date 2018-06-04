import os

import aiohttp
import asyncio
from gidgethub.aiohttp import GitHubAPI

async def main():
    # First create a GH instance
   async with aiohttp.ClientSession() as session:
       gh = GitHubAPI(session, "trallard", oauth_token=os.getenv("GH_AUTH"))

       # here we create an issue
       await gh.post('/repos/MCNotes/wintermute/issues',
             data={
                 'title': 'We got a problem',
                 'body': 'Use more emoji!',
             })

loop = asyncio.get_event_loop()
loop.run_until_complete(main())