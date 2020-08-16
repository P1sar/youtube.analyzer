import asyncio
from aio_youtube_client import AioYoutubeClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from postgres import models
import os


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


#TODO: except out of credits exeption. And log it properly
async def fetch_video(channel_id, kp, published_after, lock):
    credError = True
    while credError:
        async with lock:
            k = next(kp)
        yclient = AioYoutubeClient(api_key=k, base_url="https://www.googleapis.com/youtube/v3")
        res = await yclient.search(channel_id, published_after=published_after, max_results=30)
        e = res.get("error")
        if e:
            if "The request cannot be completed because you have exceeded your" in e.get("message"):
                print("cred error excited retrying")
                continue
        else:
            credError = False

    print(res)
    videos = []
    items = res.get("items", None)
    if items is None:
        raise Exception
    for r in items:
        date_time_obj = datetime.strptime(r["snippet"]["publishedAt"], '%Y-%m-%dT%H:%M:%SZ')
        v = models.Video(id=r["id"]["videoId"],
                         name=r["snippet"]["title"],
                         description=r["snippet"]["description"],
                         parsed_at=datetime.utcnow(),
                         added_at=date_time_obj,
                         channel_id=r["snippet"]["channelId"])
        videos.append(v)
    return videos


async def main():
    env_var = os.environ
    database_uri = env_var.get("DATABASE_URI", "postgres://postgres:password@localhost:5432/videos-data")
    fetch_freq = env_var.get("FETCH_FREQ", "5")
    engine = create_engine(database_uri)
    session_fabric = sessionmaker(bind=engine)
    session = session_fabric()

    published_after = models.KeyValue.get_time_of_last_execution(session)

    while True:
        channels_ids = models.Channel.get_channels_ids(session)
        keys = models.AccountKey.get_all_keys(session)
        kp = KeysProviderSync(keys=keys)
        ks = kp.get_key()
        lock = asyncio.Lock()
        tasks = [fetch_video(channel_id, ks, published_after, lock) for channel_id in channels_ids[:8]]
        videos = []
        for future in asyncio.as_completed(tasks):
            result = await future
            videos += result
            print(len(videos))
        published_after = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        models.KeyValue.set_time_of_last_execution(session, published_after)
        session.bulk_save_objects(videos)
        session.commit()
        await asyncio.sleep(int(fetch_freq))


loop = asyncio.get_event_loop()
task = loop.create_task(main())
try:
    loop.run_until_complete(task)
finally:
    loop.close()
