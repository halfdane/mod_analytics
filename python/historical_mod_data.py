import asyncio
import config
from influxdb_client import InfluxDBClient

import logging

import asyncpraw

asyncreddit = asyncpraw.Reddit(
		client_id=config.CLIENT_ID,
		client_secret=config.CLIENT_SECRET,
        password=config.REDDIT_PASSWORD,
        username=config.REDDIT_USERNAME,
		user_agent="com.halfdane.superstonk_mod_analytics_bot:v0.xx (by u/half_dane)"
	)


async def main():
    async with asyncreddit as reddit:
        redditor = await reddit.user.me()
        print(f"Logged in as {redditor.name}")

        subreddit = await reddit.subreddit('SuperStonk')
        client = InfluxDBClient(url="http://localhost:8086")
        print(client.get_list_database())
        async for log in subreddit.mod.log(limit=5):
            print(f"Mod: {log.mod}, {log.action}, {log.created_utc}")



logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(name)s]: %(message)s'
)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
