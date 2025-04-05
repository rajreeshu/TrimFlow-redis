from downloader.video.video_downloader_factory import VideoDownloaderFactory
from model.video_model import ProcessInfo, VideoUploadResponse
from service.video_service import VideoService
from worker.worker_interface import WorkerInterface


class VideoWorker(WorkerInterface):
    def __init__(self,process_info: ProcessInfo):
        super().__init__(process_info)
        self.video_service = VideoService()


    def upload(self) -> VideoUploadResponse:
        if not self.process_info.url:
            raise ValueError("Video url is required")
        try:
            file = VideoDownloaderFactory(self.process_info.url).get().download()
            if file is None:
                raise ValueError("No video found in the URL")

            """Upload a video file for processing."""

            video_info = self.video_service.upload_and_process(file, self.process_info)
            return VideoUploadResponse(
                filename=video_info.filename,
                file_id=video_info.file_id,
                status="Uploaded Successfully",
                message="Video processing started"
            )
        except Exception as e:
            raise RuntimeError(f"Error downloading video: {str(e)}")