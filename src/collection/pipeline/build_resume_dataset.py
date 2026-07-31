from pathlib import Path
import random

from src.collection.resumes.resume_loader import load_resumes

def main() -> None:
    random.seed(42)
    num_sample = 10

    input_path = Path("data/raw/resume_dataset_2400/Resume/Resume.csv")
    output_path = Path("data/processed/resumes/resumes.jsonl")

    load_resumes(input_path, output_path)

if __name__ == "__main__":
    main()