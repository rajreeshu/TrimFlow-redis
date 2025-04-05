from abc import abstractmethod, ABC

from model.file_model import CustomFile


class VideoDownloaderInterface(ABC):
    def __init__(self, url: str):
        self.url = url

    @abstractmethod
    def download(self)->CustomFile:
        pass