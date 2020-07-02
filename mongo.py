from pymongo import MongoClient


class MongoClient(object):
    def __init__(self, login, password, url):
        self.login = login
        self.password = password
        self.url = url
        self.client = MongoClient("mongodb://%s:%s@%s" % (login, password, url))
        self.db = client.scrapper_db
        self.videos_collection = self.db.videos_collection
    
    def insert_one_video(self, video):
        return self.videos_collection.insert_one(video).inserted_id
