import os
from abc import ABC

from instaloader import Instaloader, Post

from downloader.video.video_downloader_interface import VideoDownloaderInterface
from model.file_model import CustomFile


class InstagramVideoDownloader(VideoDownloaderInterface):
    def download(self):
        loader = Instaloader()
        post = Post.from_shortcode(loader.context, self.url.split('/')[-2])
        file_path = loader.download_post(post, target='.')
        file = open(file_path, 'rb')
        return CustomFile(
            filename=os.path.basename(file_path),
            file=file
        )
