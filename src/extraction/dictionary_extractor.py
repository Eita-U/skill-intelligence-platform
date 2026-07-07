import pandas as pd

from src.models.skill import Skill


def build_dictionary(dict_path: str) -> dict[str, Skill]:
    df = pd.read_csv(dict_path)

    skill_dict: dict[str, Skill] = {}

    for _, row in df.iterrows():
        skill = Skill(
            uri=row["conceptUri"],
            preferred_label=row["preferredLabel"],
            skill_type=row["skillType"],
            description=row["description"],
        )

        # Preferred label
        preferred = row["preferredLabel"].strip().lower()
        skill_dict[preferred] = skill

        # Alternative labels
        if pd.notna(row["altLabels"]):
            for alt in row["altLabels"].split("\n"):
                alt = alt.strip().lower()
                if alt:
                    skill_dict[alt] = skill

    return skill_dict