import requests
import tweepy

from downloader.video.video_downloader_interface import VideoDownloaderInterface


class TwitterVideoDownloader(VideoDownloaderInterface):
    def download(self):
        # Set up tweepy with your credentials
        consumer_key = 'your_consumer_key'
        consumer_secret = 'your_consumer_secret'
        access_token = 'your_access_token'
        access_token_secret = 'your_access_token_secret'

        auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
        api = tweepy.API(auth)

        tweet_id = self.url.split('/')[-1]
        tweet = api.get_status(tweet_id, tweet_mode='extended')
        media = tweet.extended_entities['media'][0]
        video_url = media['video_info']['variants'][0]['url']

        response = requests.get(video_url)
        file_path = 'twitter_video.mp4'
        with open(file_path, 'wb') as f:
            f.write(response.content)

        return open(file_path, 'rb')