import re

from downloader.direct_downloader import DirectVideoDownloader
from downloader.instagram_downloader import InstagramVideoDownloader
from downloader.twitter_downloader import TwitterVideoDownloader
from downloader.video.video_downloader_interface import VideoDownloaderInterface
from downloader.youtube_downloader import YoutubeVideoDownloader


class VideoDownloaderFactory:
    def __init__(self, url:str):
        self.url = url

    youtube_pattern = re.compile(r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/.+')
    instagram_pattern = re.compile(r'(https?://)?(www\.)?instagram\.com/.+')
    twitter_pattern = re.compile(r'(https?://)?(www\.)?(twitter|x)\.com/.+')
    direct_video_pattern = re.compile(r'.*\.(mp4|avi|mov|mkv|webm)$')

    def get(self)-> VideoDownloaderInterface:
        if self.youtube_pattern.match(self.url):
            return YoutubeVideoDownloader(self.url)
        elif self.instagram_pattern.match(self.url):
            return InstagramVideoDownloader(self.url)
        elif self.twitter_pattern.match(self.url):
            return TwitterVideoDownloader(self.url)
        elif self.direct_video_pattern.match(self.url):
            return DirectVideoDownloader(self.url)
        else:
            raise ValueError("Unsupported URL format")





