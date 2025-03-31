from enum import Enum
from typing import Optional, List, Tuple

from pydantic import BaseModel

import config.constants as constants

class ProcessingStatus(str, Enum):
    PENDING = constants.STATUS_PENDING
    PROCESSING = constants.STATUS_PROCESSING
    COMPLETED = constants.STATUS_COMPLETED
    FAILED = constants.STATUS_FAILED

class VideoInfo(BaseModel):
    file_id: str
    filename: str
    original_path: str
    status: ProcessingStatus
    segments: List[str] = []
    error: Optional[str] = None

class VideoUploadResponse(BaseModel):
    filename: str
    file_id: str
    status: str
    message: Optional[str] = None

class VideoScreenType(Enum):
    LANDSCAPE = constants.LANDSCAPE
    PORTRAIT = constants.PORTRAIT

class MediaType(Enum):
    VIDEO = constants.VIDEO
    IMAGE = constants.IMAGE

class ProcessInfo(BaseModel):
    # Declaring and setting the default Values
    media_type: MediaType
    url: str
    segment_time: int = constants.DEFAULT_VIDEO_SEGMENT_TIME
    start_time: int = constants.DEFAULT_START_TIME
    end_time: int = constants.DEFAULT_END_TIME
    skip_pairs: List[Tuple[int, int]] = []
    screen_type: VideoScreenType = VideoScreenType.LANDSCAPE
    edit_type: Optional[str] = None # To be done
