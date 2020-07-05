from youtube_client import YouTubeClient
from sqlalchemy import create_engine
import config as my_config
from postgres.models import Channel
from sqlalchemy.orm import sessionmaker


def main():
    youtube_client = YouTubeClient()
    return 1


if __name__ == "__main__":
    main()
