from src.models.skill import Skill


def build_skill_text(skill: Skill, include_description: bool = False) -> str:
    """
    Build a text representation of a skill.

    Args:
        skill: The skill.
        include_description: Whether to append the description.

    Returns:
        The text used for embedding.
    """
    label = skill.preferred_label.strip()
    description = skill.description.strip() if skill.description else ""

    if not include_description or not description:
        return label
    return f"{label}. {description}"