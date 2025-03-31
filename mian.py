import asyncio
import logging
import sys

import redis
from config.config import properties
import config.constants as constants
from processor.job_processor import JobProcessor


def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("app.log")
        ]
    )


class MainApp:
    def __init__(self):
        configure_logging()
        self.redis_client = redis.Redis(host=properties.BASE_URL, port=properties.PORT, decode_responses=True)
        self.job_processor = JobProcessor(redis_client=self.redis_client)

    def run(self):
        try:
            while True:
                # Wait for a job from the queue with a timeout of 1 second
                job = self.redis_client.brpop([constants.REDIS_VIDEO_QUEUE_NAME], timeout=properties.QUEUE_TIMEOUT)
                if job:
                    # job is a tuple (queue_name, item)
                    job_id = job[1]
                    self.job_processor.process(job_id)
                else:
                    # No job available, just print a dot to show we're alive
                    print(".", end="", flush=True)
        except KeyboardInterrupt:
            logging.info("Shutting down job consumer...")
        except Exception as e:
            logging.info(f"Error: {e}")
            sys.exit(1)



if __name__ == "__main__":
    app = MainApp()
    app.run()