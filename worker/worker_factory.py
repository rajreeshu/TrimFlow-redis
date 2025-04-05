from model.video_model import ProcessInfo, MediaType
from worker.video_worker import VideoWorker
from worker.worker_interface import WorkerInterface


class WorkerFactory:
    def __init__(self, process_info: ProcessInfo):
        self.process_info = process_info

    def get(self) -> WorkerInterface:
            match self.process_info.media_type:
                case MediaType.VIDEO:
                    return VideoWorker(self.process_info)
                # case MediaType.IMAGE:
                #     return ImageWorker(self.process_info)
                case _:
                    raise ValueError(f"Unsupported media type: {self.process_info.media_type}")