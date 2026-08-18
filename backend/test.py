# test.py
import sys
import logging
import time
from pipeline import run_pipeline   # ✅ make sure pipeline.py is in the same folder

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S"
)

def main():
    if len(sys.argv) < 2:
        logging.error("Usage: python test.py '<research topic>'")
        sys.exit(1)

    topic = sys.argv[1]
    logging.info(f"Starting multi-agent research pipeline for topic: {topic}")

    start_time = time.time()
    result = run_pipeline(topic)
    end_time = time.time()

    logging.info("Pipeline execution finished")
    logging.info(f"Total runtime: {end_time - start_time:.2f} seconds")

    print("\n" + "="*60)
    print("FINAL OUTPUT")
    print("="*60)
    print(f"Topic: {result['topic']}\n")
    print("=== Research Report ===\n")
    print(result['report'])
    print("\n=== Critic Feedback ===\n")
    print(result['feedback'])
    print("\n=== Fact Check Results ===\n")
    print(result['fact_check'])
    print("\n=== Citations ===\n")
    print(result['citations'])
    print("="*60)

if __name__ == "__main__":
    main()
