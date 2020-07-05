from services.scrapper.client import YouTubeClient
from mongo import MongoClient

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def main():

    client = YouTubeClient(api_key="AIzaSyAvR8lglUbc6KnEtWHGub-lRAU_QDaDa7o")
    mongo_client = MongoClient(login="root", password="password", url = "localhost:27017")

    channelID = "UC-yTIuKauNecL0Tl6ChD0yw"

    video = "rZdzB0SBYvs"

    res = client.searh_videos(channelID)
    # print(res)
    for a in res["items"]:
        # if a["snippet"]["type"] == "upload":
            print(a["snippet"]["title"])
            print(a["snippet"]["publishedAt"])



if __name__ == "__main__":
    main()