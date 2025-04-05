# redis_queue/job_processor.py
import json
import logging
import uuid
from typing import Dict

import config.constants as constants
from model.redis_model import DocumentReceiver
from model.video_model import ProcessInfo
from redis_queue.redis_client import RedisManager
from worker.worker_factory import WorkerFactory
from worker.worker_interface import WorkerInterface


class JobProcessor:

    def process(self, job_id: str):
        """Process a job with the given ID"""
        try:
            job_data = self._get_job_data(job_id)
            if not job_data:
                raise ValueError(f"Job {job_id} not found")

            self._process_data(job_data)
        except Exception as e:
            logging.error("Error processing job %s: %s", job_id, str(e))

    def _get_job_data(self, job_id: str) -> Dict:
        """Retrieve job data from Redis"""
        job_data = RedisManager.get_client().hgetall(job_id)
        return job_data

    def _process_data(self, job_data: Dict):
        """Process the job data and return result"""
        data_dict = job_data.get("data", "{}")
        data_json = json.loads(data_dict)
        transfer_doc = DocumentReceiver.model_validate(data_json)
        # Convert TransferDocument to ProcessInfo using model_dump
        process_info = ProcessInfo.model_validate(transfer_doc.model_dump(exclude_none=True))
        worker : WorkerInterface =WorkerFactory(process_info).get()
        worker.upload()


    def send_to_redis_queue(self, result: str) -> None:
        """Update job status and result in Redis"""
        job_id = str(uuid.uuid4())
        RedisManager.get_client().hset(job_id, "status", constants.STATUS_COMPLETED)
        RedisManager.get_client().hset(job_id, "data", result)
        RedisManager.get_client().lpush(constants.REDIS_VIDEO_PROCESSING_COMPLETED_NAME, job_id)