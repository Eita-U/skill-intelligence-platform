import json
import os
from pathlib import Path

from dotenv import load_dotenv

from src.data.resume_ner import load_resume_skill_entities
from src.llm.skill_split import split_skills
from src.llm.client import LLMClient
from src.models.resume_sample import ResumeSample

from tqdm import tqdm

INPUT_PATH = Path(
    "data/raw/resume_ner/Entity Recognition in Resumes.json"
)


# MODEL_NAME = "qwen/qwen3-235b-a22b-2507"

# OUTPUT_PATH = Path(
#     "data/processed/resume_skills_silver_qwen.jsonl"
# )

# MODEL_NAME = "deepseek/deepseek-chat-v3.1"

# OUTPUT_PATH = Path(
#     "data/processed/resume_skills_silver_deepseek.jsonl"
# )

MODEL_NAME = "google/gemini-2.5-pro"

OUTPUT_PATH = Path(
    "data/processed/resume_skills_silver_gemini.jsonl"
)

def build_silver_dataset(
    samples: list[ResumeSample],
    client: LLMClient,
    model: str,
    output_path: str | Path,
) -> None:
    """
    Generate a silver-standard skill dataset using an LLM.

    Each resume is processed independently and immediately written
    to a JSONL file.

    Args:
        samples: Resume samples containing annotated skill spans.
        client: LLM client used to generate individual skills.
        model: Model identifier passed to the LLM client.
        output_path: Path to the output JSONL file.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as file:
        for index, sample in enumerate(tqdm(samples, desc="Processing Resumes")):
            skill_spans = sample.skills
    
            if not skill_spans:
                print(
                    f"[{index + 1}/{len(samples)}] "
                    "WARNING: No annotated skills"
                )

                silver_sample = {
                    "id": index,
                    "skill_spans": skill_spans,
                    "skills": [],
                    "model": model,
                    "warning": "No annotated skills",
                }

            else:
                try:
                    skills = split_skills(
                        skill_spans=skill_spans,
                        client=client,
                        model=model,
                    )

                    silver_sample = {
                        "id": index,
                        "skill_spans": skill_spans,
                        "skills": skills,
                        "model": model,
                    }

                except Exception as error:
                    silver_sample = {
                        "id": index,
                        "skill_spans": skill_spans,
                        "skills": [],
                        "model": model,
                        "error": str(error),
                    }

                    print(
                        f"[{index + 1}/{len(samples)}] "
                        f"ERROR: {error}"
                    )

            file.write(
                json.dumps(silver_sample, ensure_ascii=False) + "\n"
            )
            file.flush()


def main() -> None:
    load_dotenv(override=True)

    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        raise ValueError(
            "OPENROUTER_API_KEY is not defined in the .env file."
        )

    client = LLMClient(api_key=api_key)

    samples = load_resume_skill_entities(INPUT_PATH)
    #samples = samples[:1]

    print(f"Loaded {len(samples)} resume samples.")
    print(f"Model: {MODEL_NAME}")
    print(f"Output: {OUTPUT_PATH}")
    print()

    build_silver_dataset(
        samples=samples,
        client=client,
        model=MODEL_NAME,
        output_path=OUTPUT_PATH,
    )


if __name__ == "__main__":
    main()