from abc import ABC, abstractmethod

from model.video_model import ProcessInfo, VideoUploadResponse


class WorkerInterface(ABC):
    def __init__(self, process_info: ProcessInfo):
        self.process_info = process_info
    @abstractmethod
    def upload(self) -> VideoUploadResponse:
        pass