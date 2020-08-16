import aiohttp


class AioYoutubeClient(object):
    def __init__(self, api_key, base_url):
        self.api_key = api_key
        self.base_url = base_url

    @staticmethod
    async def create_session():
        return aiohttp.ClientSession()

    async def search(self, channel_id, published_after='1970-01-01T00:00:00Z', search_type='video', part='snippet', order="date", max_results=5):
        """Youtube search
        url: GET {BASE_URL}/search/?q=q&part=part&
        params (*)
        q       ->  stands for query, search key. default: empty string.
        part    ->  snippet, contentDetails, player, statistics, status. default: snippet
        type    ->  types: 'video', 'playlist', 'channel'. default: video.
        video_category -> 10: Music.
        returns a json response from youtube data api v3.
        """

        url = "{}/search?key={}&part={}&type={}&maxResults={}&order={}&channel_id={}&publishedAfter={}".format(
            self.base_url,
            self.api_key,
            part,
            search_type,
            max_results,
            order,
            channel_id,
            published_after)
        print(url)
        headers = {"Accept": "application/json"}
        async with aiohttp.ClientSession() as session:
            response = await session.get(url, headers=headers)
            search_results = await response.json()
        return search_results

    async def get_detail(self, video_id=""):
        request_url = "{}/videos?id={}&part=contentDetails&key={}".format(self.base_url,
                                                                          video_id,
                                                                          self.api_key)
        async with aiohttp.ClientSession() as session:
            response = await session.get(request_url)
            search_results = await response.json()
        return search_results

    async def get_playlist(self, part="snippet", max_results=7, playlist_id="", playlist_url=""):
        """fetch playlist items
        get playlist from a given playlist_id or playlist_url.
        """

        url = "{}/playlistItems?key={}&part={}&maxResults={}&playlistId={}".format(self.base_url,
                                                                                   self.api_key,
                                                                                   part,
                                                                                   max_results,
                                                                                   playlist_id)
        async with aiohttp.ClientSession() as session:
            response = await session.get(url)
            search_results = await response.json()
        return search_results
