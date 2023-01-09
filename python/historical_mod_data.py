import asyncio
import config
from influxdb import InfluxDBClient

from datetime import datetime

import logging
import asyncpraw

asyncreddit = asyncpraw.Reddit(
		client_id=config.CLIENT_ID,
		client_secret=config.CLIENT_SECRET,
        password=config.REDDIT_PASSWORD,
        username=config.REDDIT_USERNAME,
		user_agent="com.halfdane.superstonk_mod_analytics_bot:v0.xx (by u/half_dane)"
	)

class InfluxDBClientWrapper():
    client = None

    def __init__(self, host, port, database) -> None:
        if config.ENVIRONMENT == "production":
            self.client = InfluxDBClient(host=host, port=port, database=database)
    
    def write_points(self, points):
        if self.client is not None:
            self.client.write_points(points=points)
        else:
            print(points)
    

def to_json(item):
    created = datetime.utcfromtimestamp(item.created_utc).strftime("%d.%m.%Y, %H:%M:%S")
    print(created)
    return {
            "measurement": "mod_activity",
            "tags": {
                "mod": item.mod.name,
                "action": item.action,
                "fullname":  item.target_fullname,
                "author": item.target_author,
                "description": item.description,
                "details": item.details,
                "type": "post" 
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
        client = InfluxDBClientWrapper(host="localhost", port=8086, database="sample_database")
        async for log in subreddit.mod.log(limit=None):
            created = datetime.utcfromtimestamp(log.created_utc).strftime("%d.%m.%Y, %H:%M:%S")
            print(f"{created} ({log.created_utc})")

            if log.created_utc > 1666994476:
                continue

            await asyncio.sleep(0.001)
            client.write_points([to_json(log)])





logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(name)s]: %(message)s'
)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
