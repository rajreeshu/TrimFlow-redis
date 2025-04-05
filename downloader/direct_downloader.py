import io
import os

import requests

from downloader.video.video_downloader_interface import VideoDownloaderInterface
from model.file_model import CustomFile


class DirectVideoDownloader (VideoDownloaderInterface):
    def download(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            file_extension = os.path.splitext(self.url)[1]
            file_path = 'downloaded_video' + file_extension
            with open(file_path, 'wb') as f:
                f.write(response.content)

            # Read the file content into memory
            with open(file_path, 'rb') as f:
                file_content = f.read()

            # Create a SpooledTemporaryFile for the UploadFile
            spooled_file = io.BytesIO(file_content)

            # Create an UploadFile object
            upload_file = CustomFile(
                filename=os.path.basename(file_path),
                file=spooled_file,
            )

            # Clean up the temporary file
            try:
                os.remove(file_path)
            except:
                pass

            return upload_file
        else:
            raise ValueError("Failed to download video")