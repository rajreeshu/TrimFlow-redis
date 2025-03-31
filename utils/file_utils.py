import logging

from model.file_model import CustomFile

logger = logging.getLogger(__name__)

def save_file_in_chunks(file: CustomFile, file_path: str, chunk_size: int = 8192) -> None:
    """Save a large file in chunks synchronously."""
    try:
        with open(file_path, 'wb') as f:
            while chunk := file.file.read(chunk_size):
                f.write(chunk)
        logger.info(f"File saved successfully: {file_path}")
    except Exception as e:
        logger.error(f"Error saving file {file_path}: {str(e)}")
        raise