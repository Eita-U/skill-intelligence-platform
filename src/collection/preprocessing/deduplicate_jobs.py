import re
import hashlib
from pathlib import Path
import json
from tqdm import tqdm
from collections import defaultdict

def normalize_description(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def hash_description(text: str) -> str:
    text = normalize_description(text)
    text_hash = hashlib.sha256(text.encode('utf-8'))
    return text_hash.hexdigest()

def deduplicate_jobs(input_path: Path, output_path: Path):
    output_path.parent.mkdir(parents=True, exist_ok=True)

    companies = defaultdict(set)
    total = 0
    unique = 0

    print(f"\n{'=' * 20} Deduplicate Jobs {'=' * 20}")
    with (
            input_path.open("r", encoding="utf-8") as input_file,
            output_path.open("w", encoding="utf-8") as output_file,
        ):
            for line in tqdm(input_file):
                total += 1
                job_posting = json.loads(line)
                source = job_posting["source_identifier"]
                description = job_posting["description"]
                description_hash = hash_description(description)
                unique_hashes = companies[source]
                if description_hash not in unique_hashes:
                    unique_hashes.add(description_hash)
                    output_file.write(
                    json.dumps(job_posting, ensure_ascii=False) + "\n"
                    )
                    unique += 1

    print(f"Total number of jobs: {total}")
    print(f"Number of unique jobs: {unique}")
    print(f"Deleted jobs: {total - unique}")