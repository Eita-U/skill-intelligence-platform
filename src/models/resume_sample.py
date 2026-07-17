from dataclasses import dataclass

@dataclass(slots=True)
class ResumeSample:
    text: str
    skills: list[str]