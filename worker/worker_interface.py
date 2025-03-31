from abc import ABC, abstractmethod

from model.video_model import ProcessInfo


class WorkerInterface(ABC):
    @abstractmethod
    def upload(self) -> str:
        pass