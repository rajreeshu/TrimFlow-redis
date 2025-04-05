import redis_queue
import time
import random
import sys

# Connect to Redis
r = redis_queue.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# List of sample words to choose from
word_list = [
    "apple", "banana", "cherry", "dragon", "elephant", "forest",
    "giraffe", "hammer", "igloo", "jacket", "kangaroo", "lemon",
    "mountain", "notebook", "orange", "penguin", "queen", "rabbit",
    "sunshine", "tiger", "umbrella", "volcano", "window", "xylophone",
    "yellow", "zebra"
]


def add_job():
    """Add a new job with two random words to Redis"""
    # Select two random words
    word1 = random.choice(word_list)
    word2 = random.choice(word_list)

    # Create a unique job ID using timestamp
    job_id = f"job:{int(time.time() * 1000)}"

    # Store the job in Redis as a hash
    r.hset(job_id, mapping={
        "word1": word1,
        "word2": word2,
        "status": "pending"
    })

    # Add job to the queue
    r.lpush("job_queue", job_id)

    print(f"Added job {job_id}: word1='{word1}', word2='{word2}'")


def main():
    print("Job Producer Started")
    print("Adding a new job every 3 seconds. Press Ctrl+C to stop.")

    try:
        while True:
            add_job()
            time.sleep(3)  # Wait for 3 seconds before adding next job
    except KeyboardInterrupt:
        print("\nShutting down job producer...")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()