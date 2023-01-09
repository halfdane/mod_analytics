import asyncio
import config
from influxdb import InfluxDBClient

import logging

import asyncpraw

asyncreddit = asyncpraw.Reddit(
		client_id=config.CLIENT_ID,
		client_secret=config.CLIENT_SECRET,
        password=config.REDDIT_PASSWORD,
        username=config.REDDIT_USERNAME,
		user_agent="com.halfdane.superstonk_mod_analytics_bot:v0.xx (by u/half_dane)"
	)

def to_json(item):
    return {
            "measurement": "activity",
            "tags": {
                "mod": item.mod,
                "action": item.action
            },
            "time": int(item.created_utc)*1_000_000_000,
            "fields": {
                "value": 1
            }
        }
    

async def main():
    async with asyncreddit as reddit:
        redditor = await reddit.user.me()
        print(f"Logged in as {redditor.name}")

        subreddit = await reddit.subreddit('SuperStonk')
        client = InfluxDBClient(host="localhost", port=8086, database="sample_database")
        result = client.query('select value from random_ints;')
        print("Result: {0}".format(result))
        points = [to_json(log) async for log in subreddit.mod.log(limit=100)]
        client.write_points(points)
        print(points)



logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(name)s]: %(message)s'
)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
