# processor/job_processor.py
import json

import redis
from typing import Dict, Any
from config.config import properties
import config.constants as constants
from model.video_model import ProcessInfo
from worker.worker_factory import WorkerFactory
from worker.worker_interface import WorkerInterface


class JobProcessor:
    def __init__(self, redis_client : redis.Redis):
        self.redis_client = redis_client

    def process(self, job_id: str) -> None:
        """Process a job with the given ID"""
        job_data = self._get_job_data(job_id)
        if not job_data:
            raise ValueError(f"Job {job_id} not found")

        result = self._process_data(job_data)
        self._update_job_status(job_id, result)

    def _get_job_data(self, job_id: str) -> Dict:
        """Retrieve job data from Redis"""
        job_data = self.redis_client.hgetall(job_id)
        return job_data

    def _process_data(self, job_data: Dict) -> Any:
        """Process the job data and return result"""
        data_dict = job_data.get("data", "{}")
        data_json = json.loads(data_dict)
        process_info = ProcessInfo.model_validate(data_json)
        worker : WorkerInterface =WorkerFactory(process_info).get()
        return worker.upload()


    def _update_job_status(self, job_id: str, result: str) -> None:
        """Update job status and result in Redis"""
        self.redis_client.hset(job_id, "status", constants.STATUS_COMPLETED)
        self.redis_client.hset(job_id, "result", result)
        self.redis_client.lpush("completed_jobs", job_id)