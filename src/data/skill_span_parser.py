

def parse_skill_spans(text: str) -> list[str]:
    """
    Parses skills from the input text and returns a list of skill spans.

    Args:
        text (str): The input text containing skill spans.
    """
    skill_spans = []
    lines = text.splitlines()

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Assuming each line contains a skill span
        skill_spans.append(line)

    return skill_spans