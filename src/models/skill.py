from dataclasses import dataclass

@dataclass(slots=True)
class Skill:
    uri: str
    preferred_label: str
    skill_type: str
    description: str | None = None