from pathlib import Path
import json
from tqdm import tqdm
from collections import defaultdict
import random

def sample_jobs(input_path: Path, output_path: Path, num_jobs: int) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    companies = defaultdict(list)
    total = 0
    sampled = 0

    print(f"\n{'=' * 20} Sample Jobs {'=' * 20}")
    with (
        input_path.open("r", encoding="utf-8") as input_file,
        output_path.open("w", encoding="utf-8") as output_file,
    ):
        for line in tqdm(input_file):
            total += 1
            job_posting = json.loads(line)
            source = job_posting["source_identifier"]
            companies[source].append(job_posting)

        for jobs in companies.values():
            if len(jobs) <= num_jobs:
                selected_jobs = jobs
            else:
                selected_jobs = random.sample(jobs, num_jobs)
                
            for job in selected_jobs:
                sampled += 1
                output_file.write(
                json.dumps(job, ensure_ascii=False) + "\n"
                )
        print(f"Companies: {len(companies)}")
        print(f"Total Jobs: {total}")
        print(f"Sampled Jobs: {sampled}")

def main() -> None:
    random.seed(42)
    input_path = Path("data/processed/jobs/greenhouse_jobs_dedup.jsonl")
    output_path = Path("data/processed/jobs/greenhouse_jobs_sampled.jsonl")

    sample_jobs(input_path, output_path, 10)

if __name__ == "__main__":
    main()