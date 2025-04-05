from typing import Optional, List, Tuple

from pydantic import BaseModel

from model.video_model import MediaType, VideoScreenType



class DocumentReceiver(BaseModel):
    media_type: Optional[MediaType] = None
    url: Optional[str] = None
    file_name: Optional[str] = None
    segment_time: Optional[int] = None
    start_time: Optional[int] = None
    end_time: Optional[int] = None
    skip_pairs: Optional[List[Tuple[int, int]]] = None
    screen_type: Optional[VideoScreenType] = None
    edit_type: Optional[str] = None
    original_video_id: Optional[int] = None
    telegram_chat_id: Optional[int] = None

class ProcessedDataTransfer(BaseModel):
    original_video_id: Optional[int] = None
    file_name : Optional[str] = None
    location: Optional[str] = None
    telegram_chat_id: Optional[int] = None


