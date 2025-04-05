import io
import os

import yt_dlp

from downloader.video.video_downloader_factory import VideoDownloaderInterface
from model.file_model import CustomFile


class YoutubeVideoDownloader(VideoDownloaderInterface):
    def download(self):
        """Download a YouTube video using yt-dlp"""
        try:
            ydl_opts = {
                'format': 'bestvideo[height<=720]+bestaudio/best[height<=720]/best',
                'outtmpl': '%(title)s.%(ext)s',
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.url, download=True)
                filename = ydl.prepare_filename(info)

                # Get the content type based on file extension
                ext = os.path.splitext(filename)[1].lstrip('.')
                content_type = f"video/{ext}" if ext != 'webm' else "video/webm"

                # Open the file and read its contents into memory
                with open(filename, 'rb') as f:
                    file_content = f.read()

                # Create a SpooledTemporaryFile for the UploadFile
                spooled_file = io.BytesIO(file_content)

                # Create an UploadFile object
                upload_file = CustomFile(
                    filename=os.path.basename(filename),
                    file=spooled_file,
                )

                # Clean up the temporary file
                try:
                    os.remove(filename)
                except:
                    pass

                return upload_file

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None