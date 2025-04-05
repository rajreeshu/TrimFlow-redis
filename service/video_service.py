import asyncio
import json
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from typing import Dict

import service.subtitle_service as subtitle_service
import utils.file_utils as file_utils
import utils.validators as validators
from model.file_model import CustomFile
from model.redis_model import ProcessedDataTransfer
from model.video_model import VideoInfo, ProcessingStatus, ProcessInfo

from service.ffmpeg_service import FfmpegService

from config.config import properties

logger = logging.getLogger(__name__)

class VideoService:
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=properties.MAX_WORKERS)
        self.video_jobs: Dict[str, VideoInfo] = {}
        self.ffmpeg_service = FfmpegService()

    def upload_and_process(self, file: CustomFile, video_process_info: ProcessInfo) -> VideoInfo:
        """Upload a video file and submit for processing."""
        try:
            # Validate file
            validators.validate_video_file(file.filename)
            
            # Generate unique filename and ID
            unique_filename, file_id = validators.generate_unique_filename(file.filename)

            # Save video file
            file_path = os.path.join(properties.UPLOAD_DIR, unique_filename)
            file_utils.save_file_in_chunks(file, file_path)

            if video_process_info.start_time is None:
                video_process_info.start_time = subtitle_service.find_movie_start_time(file_path)

            # Remove metadata from the video file
            cleaned_file_path = self.ffmpeg_service.remove_metadata(file_path)

            # Create video info object
            video_info = VideoInfo(
                file_id=file_id,
                filename=unique_filename,
                original_path=cleaned_file_path,
                status=ProcessingStatus.PENDING
            )

            # Submit for processing
            self.video_jobs[file_id] = video_info
            asyncio.run(self._process_video(file_id, video_process_info))
            
            return video_info

        except Exception as e:
            logger.error(f"Error processing upload: {str(e)}")
            raise ValueError(f"Upload failed: {str(e)}")


    async def _process_video(self, file_id: str, video_process_info:ProcessInfo) -> None:
        from redis_queue.job_processor import JobProcessor
        """Process the video in a separate thread."""
        if file_id not in self.video_jobs:
            logger.error(f"Video job not found: {file_id}")
            return
            
        video_info = self.video_jobs[file_id]
        updated_info = self.ffmpeg_service.trim_video(video_info,video_process_info)
        self.video_jobs[file_id] = updated_info

        for segment in updated_info.segments:
            # Send Request to FastApi server to save in DB
            trimmed_video_json = ProcessedDataTransfer(
                file_name=segment,
                location=validators.generate_full_path_from_location(os.path.join(properties.TRIMMED_DIR, segment)),
                original_video_id=video_process_info.original_video_id,
                telegram_chat_id=video_process_info.telegram_chat_id
            )

            JobProcessor().send_to_redis_queue(
                json.dumps(trimmed_video_json.model_dump(exclude_none=True))
            )
