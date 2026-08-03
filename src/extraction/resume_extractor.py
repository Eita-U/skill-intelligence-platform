from dataclasses import asdict, dataclass
from typing import Literal

from pathlib import Path
from tqdm import tqdm
import json

from src.extraction.client import LLMClient
from src.extraction.resume_prompts import SYSTEM_PROMPT, build_user_prompt

from concurrent.futures import ThreadPoolExecutor, as_completed

@dataclass
class ExtractedResume:
    id: str
    text: str
    skills: list[str]

def process_response(response_str: str) -> list[str]:
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

    for skill in skills:
        if not isinstance(skill, str):
            raise ValueError(
                f"Each skill must be a string:\n{skill}"
            )

    return skills

def extract(text: str) -> list[str]:
    client = LLMClient()
    response = client.generate(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=build_user_prompt(text),
        )
    return process_response(response)

def skill_extraction(input_path: Path, output_path: Path, num_resumes=-1):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    

    with (
            input_path.open("r", encoding="utf-8") as input_file,
            output_path.open("w", encoding="utf-8") as output_file,
        ):
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_row = {}
            for i, line in enumerate(input_file):
                if num_resumes > 0 and i >= num_resumes:
                    break

                row = json.loads(line)

                future = executor.submit(
                    extract,
                    row["description"],
                )

                future_to_row[future] = row

            for future in tqdm(as_completed(future_to_row), total=len(future_to_row)):
                row = future_to_row[future]
                extracted_skills = future.result()

                extracted_document = ExtractedResume(id=row["id"], text=row["description"], skills=extracted_skills,)
                output_file.write(json.dumps(asdict(extracted_document), ensure_ascii=False) + "\n")

def main() -> None:
    input_path_resume = Path("data/processed/resumes/resumes.jsonl")
    output_path_resume = Path("data/processed/resumes/resumes_extracted_gpt5nano.jsonl")

    skill_extraction(input_path_resume, output_path_resume, num_resumes=100)

if __name__ == "__main__":
    main()