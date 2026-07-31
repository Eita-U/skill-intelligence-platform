import json
from pathlib import Path
from src.models.resume_sample import ResumeSample


def load_resume_skill_entities(path: str | Path) -> list[ResumeSample]:
    path = Path(path)

    with open(path, encoding="utf-8") as f:
        resumes = [json.loads(line) for line in f if line.strip()]
    
    samples = []

    for resume in resumes:
        resume_text = resume['content']
        gold_skills = []

        for annotation in resume["annotation"]:
            if "Skills" not in annotation["label"]:
                continue

            for point in annotation["points"]:
                gold_skills.append(point["text"])
        resume_sample = ResumeSample(text=resume_text, skills=gold_skills)
        samples.append(resume_sample)
    return samples


def inspect_skill_spans(
    samples: list[ResumeSample],
    start: int = 0,
    count: int = 10,
) -> None:
    end = min(start + count, len(samples))

    for resume_id in range(start, end):
        skill_spans = samples[resume_id].skills

        print("=" * 80)
        print(f"RESUME ID: {resume_id}")
        print(f"NUMBER OF SKILL SPANS: {len(skill_spans)}")
        print("=" * 80)

        if not skill_spans:
            print("[NO SKILLS ANNOTATED]")
            continue

        for span_id, span in enumerate(skill_spans):
            print(f"\n--- SKILL SPAN {span_id} ---")
            print(span.strip())

        print()

def prepare_skill_span(span: str) -> str:
    span = span.replace("[…]", " ")
    span = span.replace("\r\n", "\n")
    return span.strip()

load_resume_skill_entities("data/raw/resume_ner/Entity Recognition in Resumes.json")