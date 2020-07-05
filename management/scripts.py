import sys
sys.path = ['', '..'] + sys.path[1:]

import os
import config as my_config

from sqlalchemy.orm import load_only, sessionmaker
from postgres.models import Channel
from sqlalchemy import create_engine
from s3 import S3Client`


def propagate_db_with_channels_from_s3():
    channels_provider = S3Client(key="minio-key",secret="minio-secret", endpoint_url="http://localhost:9000")
    channels_map = channels_provider.channels_map(os.environ.get("BUCKET_NAME", "channels"), os.environ.get("CHANNELS_FILENAME", "channels.csv"))

    engine = create_engine(my_config.DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()

    existed_channels = session.query(Channel).options(load_only("id")).all()
    ids = [c.id for c in existed_channels]

    channels_to_add = []
    for channel_id in channels_map:
        if channel_id not in ids:
            c = Channel(id=channel_id, name=channels_map[channel_id])
            channels_to_add.append(c)

    session.bulk_save_objects(channels_to_add)
    session.commit()


propagate_db_with_channels_from_s3()