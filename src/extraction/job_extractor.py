from dataclasses import asdict, dataclass
from typing import Literal

from pathlib import Path
from tqdm import tqdm
import json

from src.extraction.client import LLMClient
from src.extraction.job_prompts import SYSTEM_PROMPT, build_user_prompt

from concurrent.futures import ThreadPoolExecutor, as_completed

@dataclass(frozen=True)
class JobSkill:
    name: str
    mention_type: Literal[
        "required",
        "preferred",
        "responsibility",
    ]

@dataclass
class ExtractedJob:
    id: str
    text: str
    skills: list[JobSkill]

def process_response(response_str: str) -> list[JobSkill]:
    try:
        response_json = json.loads(response_str)
    except json.JSONDecodeError as error:
        raise ValueError(
            f"Failed to parse LLM response as JSON:\n{response_str}"
        ) from error

    skills = response_json.get("skills")

    if not isinstance(skills, list):
        raise ValueError(
            f"Expected 'skills' to be a list:\n{response_json}"
        )

    extracted_skills = []
    valid_mention_types = {
                "required",
                "preferred",
                "responsibility",
            }

    for skill in skills:
        if not isinstance(skill, dict):
            print(f"Skipped non-object skill: {skill}")
            continue

        name = skill.get("name")
        mention_type = skill.get("mention_type")

        if not isinstance(name, str) or not name.strip():
            print(f"Skipped skill with invalid name: {skill}")
            continue

        if mention_type not in valid_mention_types:
            print(f"Skipped invalid mention_type: {skill}")
            continue

        extracted_skills.append(
            JobSkill(
                name=name,
                mention_type=mention_type,
            )
        )

    return extracted_skills

def extract(text: str) -> list[JobSkill]:
    client = LLMClient()
    response = client.generate(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=build_user_prompt(text),
        )
    return process_response(response)

def skill_extraction(input_path: Path, output_path: Path, num_jobs=-1):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    

    with (
            input_path.open("r", encoding="utf-8") as input_file,
            output_path.open("w", encoding="utf-8") as output_file,
        ):
        with ThreadPoolExecutor(max_workers=25) as executor:
            future_to_row = {}
            for i, line in enumerate(input_file):
                if num_jobs > 0 and i >= num_jobs:
                    break

                row = json.loads(line)

                future = executor.submit(
                    extract,
                    row["description"],
                )

                future_to_row[future] = row

            total_jobs = 0
            total_skills = 0

            for future in tqdm(as_completed(future_to_row), total=len(future_to_row)):
                row = future_to_row[future]

                try:
                    extracted_skills = future.result()
                except Exception as error:
                    print(f'\nFailed job {row["id"]}: {error}')
                    continue

                total_jobs += 1
                total_skills += len(extracted_skills)

                extracted_document = ExtractedJob(id=row["id"], text=row["description"], skills=extracted_skills,)
                output_file.write(json.dumps(asdict(extracted_document), ensure_ascii=False) + "\n")

            print(f"Jobs: {total_jobs}")
            print(f"Skills: {total_skills}")
            print(f"Average: {total_skills / total_jobs:.2f}")  

def main() -> None:
    input_path_resume = Path("data/processed/jobs/greenhouse_jobs_sampled.jsonl")
    output_path_resume = Path("data/processed/jobs/greenhouse_jobs_extracted.jsonl")

    skill_extraction(input_path_resume, output_path_resume, num_jobs=100)

if __name__ == "__main__":
    main()