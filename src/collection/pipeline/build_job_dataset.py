from pathlib import Path
import random

from src.collection.jobs.collect_jobs import collect_jobs
from src.collection.preprocessing.deduplicate_jobs import deduplicate_jobs
from src.collection.preprocessing.sample_jobs import sample_jobs

def main() -> None:
    random.seed(42)
    num_sample = 10

    original_path = Path("data/raw/jobs/greenhouse_jobs.jsonl")
    dedup_path = Path("data/processed/jobs/greenhouse_jobs_dedup.jsonl")
    sampled_path = Path("data/processed/jobs/greenhouse_jobs_sampled.jsonl")


    collect_jobs(original_path)
    deduplicate_jobs(original_path, dedup_path)
    sample_jobs(dedup_path, sampled_path, num_sample)

if __name__ == "__main__":
    main()