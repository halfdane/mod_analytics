import asyncio
import logging
import re
import sqlite3
from datetime import date, datetime, timedelta
from pprint import pprint
from unittest.mock import MagicMock
from urllib.parse import urlparse

import asyncpraw

configuration = ModerationBotConfiguration()

asyncreddit = asyncpraw.Reddit(
    **configuration.qvbot_reddit_settings(),
    user_agent="com.halfdane.superstonk_moderation_bot:v0.xx (by u/half_dane)")

async def main():
    async with asyncreddit as reddit:
        redditor = await reddit.user.me()
        print(f"Logged in as {redditor.name}")

        for i in ['DRSyourGME']:
            await handle_subreddit(await reddit.subreddit(i))



logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(name)s]: %(message)s'
)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
