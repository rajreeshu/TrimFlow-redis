import ast
import os
import re
import uuid
from typing import Tuple

from config.config import properties


def validate_video_file(filename: str) -> None:
    """Validate if file is a video based on extension."""
    valid_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.webm']
    ext = os.path.splitext(filename)[1].lower()
    
    if ext not in valid_extensions:
        raise ValueError(f"Invalid file type. Accepted types: {', '.join(valid_extensions)}")

def generate_unique_filename(filename: str) -> Tuple[str, str]:
    """Generate a unique filename to avoid conflicts."""
    base_name = os.path.splitext(filename)[0]
    extension = os.path.splitext(filename)[1]
    file_id = str(uuid.uuid4())
    unique_filename = f"{base_name}-{file_id}{extension}"
    unique_filename = re.sub(r'[^a-zA-Z0-9.-]', '-', unique_filename)
    return unique_filename, file_id

def generate_full_path_from_location(location: str) -> str:
    return properties.COMPLETE_BASE_URL + "/" +location
