import pandas as pd
from pathlib import Path

from src.models.skill import Skill


def load_esco_skills(path: str | Path) -> list[Skill]:
    df = pd.read_csv(path).fillna("")
    skills = []

    for row in df.itertuples(index=False):
        skill = Skill(uri = row.conceptUri, preferred_label = row.preferredLabel, skill_type = row.skillType, description = row.description)
        skills.append(skill)
        
        if row.altLabels:
            for label in row.altLabels.splitlines():
                label = label.strip()
                if not label:
                    continue
                skill = Skill(uri = row.conceptUri, preferred_label = label, skill_type = row.skillType, description = row.description)
                skills.append(skill)

    return skills
