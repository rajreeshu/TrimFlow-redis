import logging
import os
import socketserver
import sys
import threading
from http.server import SimpleHTTPRequestHandler

import config.constants as constants
from config.config import properties
from redis_queue.job_processor import JobProcessor
from redis_queue.redis_client import RedisManager


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
        self.job_processor = JobProcessor()

    def run_redis_consumer(self):
        redis_client = RedisManager.get_client()
        try:
            while True:
                # Wait for a job from the queue with a timeout of 1 second
                job = redis_client.brpop([constants.REDIS_VIDEO_QUEUE_NAME], timeout=properties.QUEUE_TIMEOUT)
                if job:
                    # job is a tuple (queue_name, item)
                    job_id = job[1]
                    self.job_processor.process(job_id)
        except KeyboardInterrupt:
            logging.info("Shutting down job consumer...")
        except Exception as e:
            logging.info(f"Error: {e}")

    def run_server_for_static_file(self):
        # os.chdir("media")

        Handler = SimpleHTTPRequestHandler

        with socketserver.TCPServer(("", properties.PORT), Handler) as httpd:
            print(f"Serving at http://localhost:{properties.PORT}")
            httpd.serve_forever()

    def run(self):
        # Start static file server in a separate thread
        static_server_thread = threading.Thread(target=self.run_server_for_static_file, daemon=True)
        static_server_thread.start()

        # Run Redis consumer in the main thread
        self.run_redis_consumer()

if __name__ == "__main__":
    app = MainApp()
    app.run()