import redis_queue
import time
import sys

# Connect to Redis
r = redis_queue.Redis(host='localhost', port=6379, decode_responses=True)


def process_job(job_id):
    """Process a job by interleaving characters from the two words"""
    # Retrieve job data from Redis
    job_data = r.hgetall(job_id)

    if not job_data:
        print(f"Job {job_id} not found")
        return

    # Get the words
    word1 = job_data.get("word1", "")

    # reverse word1
    result = word1[::-1]

    # Update job status in Redis
    r.hset(job_id, "status", "completed")
    r.hset(job_id, "result", result)

    # Add to completed jobs list
    r.lpush("completed_jobs", job_id)

    print(f"Processed {job_id}:")
    print(f"  Word 1: {word1}")
    print(f"  Result: {result}")
    print("-" * 40)
    # time.sleep(random.randint(1, 3))  # Simulate processing time


def main():
    print("Job Consumer Started")
    print("Waiting for jobs. Press Ctrl+C to stop.")

    try:
        while True:
            # Wait for a job from the queue with a timeout of 1 second
            job = r.brpop("video_status_queue", timeout=1)

            if job:
                # job is a tuple (queue_name, item)
                job_id = job[1]
                process_job(job_id)
            else:
                # No job available, just print a dot to show we're alive
                print(".", end="", flush=True)
                time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nShutting down job consumer...")
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()