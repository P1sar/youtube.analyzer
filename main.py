import json
from aio_youtube_client import AioYoutubeClient
from sqlalchemy import create_engine
import config as my_config
from sqlalchemy.orm import load_only, sessionmaker
from datetime import datetime, timezone, timedelta
from postgres import models
import asyncio

ioloop = asyncio.get_event_loop()


async def get_videos(channel_id, published_after):
    aio_youtube_client = AioYoutubeClient(api_key="AIzaSyCDOu0GKzY_6DIib3gGYQ5XZIJ9n-6Zkmk",
                                          base_url="https://www.googleapis.com/youtube/v3")
    res = await aio_youtube_client.search(channel_id, published_after=published_after, max_results=10)
    videos = []
    print(res)
    items = res.get("items", None)
    if items is None:
        raise Exception
    for r in items:
        date_time_obj = datetime.strptime(r["snippet"]["publishedAt"], '%Y-%m-%dT%H:%M:%SZ')
        v = models.Video(id=r["id"]["videoId"],
                         name=r["snippet"]["title"],
                         description=r["snippet"]["description"],
                         added_at=date_time_obj, channel_id=r["snippet"]["channelId"])
        videos.append(v)
    return videos


async def main():
    engine = create_engine(my_config.DATABASE_URI)
    session_fabric = sessionmaker(bind=engine)
    session = session_fabric()

    published_after = models.KeyValue.get_time_of_last_execution(session)

    existed_channels = session.query(models.Channel).options(load_only("id")).all()
    channel_id_ids = [c.id for c in existed_channels]
    videos = []
    tasks = [get_videos(channel_id, published_after) for channel_id in channel_id_ids[:10]]
    for future in asyncio.as_completed(tasks):
        result = await future
        videos += result

    models.KeyValue.set_time_of_last_execution(session, datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'))

    session.bulk_save_objects(videos)
    session.commit()


ioloop.run_until_complete(main())
ioloop.close()
