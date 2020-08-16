import asyncio
from aio_youtube_client import AioYoutubeClient
from sqlalchemy import create_engine
import config as my_config
from sqlalchemy.orm import load_only, sessionmaker
from datetime import datetime
from postgres import models


#TODO: except out of credits exeption. And log it properly
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


class KeysProviderSync(object):
    def __init__(self, keys, max_reuse=8):
        self.keys = keys
        self.max_reuse = max_reuse
        self.reuses = 0
        self.i = 0

    def get_key(self):
        while self.i < len(self.keys):
            self.reuses += 1
            yield self.keys[self.i]
            if self.reuses == self.max_reuse:
                self.i += 1
                self.reuses = 0


async def fetch_video(channel_id, kp, lock):
    async with lock:
        k = next(kp)
    await asyncio.sleep(2)
    print("channel_id:{} key:{}".format(channel_id, k))


async def main():
    engine = create_engine(my_config.DATABASE_URI)
    session_fabric = sessionmaker(bind=engine)
    session = session_fabric()

    while True:
        channels_ids = models.Channel.get_channels_ids(session)
        keys = models.AccountKey.get_all_keys(session)
        kp = KeysProviderSync(keys=keys)
        ks = kp.get_key()
        lock = asyncio.Lock()
        tasks = [fetch_video(channel_id, ks, lock) for channel_id in channels_ids[:100]]
        videos = []
        await asyncio.wait(tasks)
        await asyncio.sleep(15)


loop = asyncio.get_event_loop()
task = loop.create_task(main())
try:
    loop.run_until_complete(task)
finally:
    loop.close()


    # published_after = models.KeyValue.get_time_of_last_execution(session)
    #
    # existed_channels = session.query(models.Channel).options(load_only("id")).all()
    # channel_id_ids = [c.id for c in existed_channels]
    # videos = []
    # tasks = [get_videos(channel_id, published_after) for channel_id in channel_id_ids[:10]]
    # for future in asyncio.as_completed(tasks):
    #     result = await future
    #     videos += result
    #
    # models.KeyValue.set_time_of_last_execution(session, datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'))
    #
    # session.bulk_save_objects(videos)
    # session.commit()
