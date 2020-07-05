from googleapiclient.discovery import build


class YouTubeClient(object):
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_service_name = "youtube"
        self.api_version = "v3"
        self.youtube = build(self.api_service_name, self.api_version, developerKey=self.api_key)

    def get_play_list_items(self, plId):
        return self.youtube.playlistItems().list(
            part="snippet",
            playlistId=plId,
            maxResults=2
        ).execute()

    def get_play_lists(self, channelID):
        return self.youtube.playlists().list(
            part="snippet,contentDetails",
            channelId=channelID,
            maxResults=50
        ).execute()

    def get_channel_details(self, channelID):
        return self.youtube.channels().list(
            part="snippet",
            id=channelID
        ).execute()

    def get_channel_activities(self, channelID):
        return self.youtube.activities().list(
            part="snippet",
            channelId=channelID,
            maxResults=25
        ).execute()

    def get_video_rating(self, videoID):
        return self.youtube.videos().getRating(
            id=videoID
        ).execute()

    def get_video_list(self, id):
        return self.youtube.videos().list(
            part="snippet,contentDetails,statistics,status",
            id=id
        ).execute()

    def search_videos(self, channel_id, max_results=25):
        return self.youtube.search().list(
            part="snippet",
            channelId=channel_id,
            order="date",
            type="video",
            maxResults=max_results
        ).execute()