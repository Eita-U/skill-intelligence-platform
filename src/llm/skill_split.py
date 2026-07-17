from src.llm.client import LLMClient
from src.models.resume_sample import ResumeSample
import json

SYSTEM_PROMPT = """
You are creating a silver-standard dataset for evaluating skill extraction from resumes.
Your task is to convert the provided annotated skill spans into a deduplicated list of individual skills.

Follow these rules strictly:

1. Extract every individual skill explicitly mentioned in the annotated skill spans. Include technical skills, tools, technologies, certifications, and explicitly stated soft skills when they appear.

2. Split coordinated lists into individual skills when they clearly enumerate separate skills.
   Examples:
   * "C, C++, Java" → "C", "C++", "Java"
   * "Hadoop and Spark" → "Hadoop", "Spark"
   * "Ajax & JQuery" → "Ajax", "JQuery"

3. Do not split a phrase if it refers to a single skill, technology, product, certification, or other single concept, even if it contains spaces, conjunctions, or punctuation.
   Examples:
   * "Machine Learning" remains one skill.
   * "Database Management System" remains one skill.
   * "Honest and Hard-Working" remains one skill.
   * "Requirement Gathering" remains one skill.

4. Remove category labels and introductory phrases, but retain the skills that follow them.
   Examples:
   * "Programming Languages: C, Java" → "C", "Java"
   * "Operating Systems: Linux, Windows" → "Linux", "Windows"

5. Remove experience-duration information from skill names without changing the skill itself.
Examples:
   * "Java (Less than 1 year)" → "Java"
   * "SQL (3 years)" → "SQL"
   * "Python (2+ years)" → "Python"

6. Remove section headings, URLs, and other resume text that is not part of a skill. Keep any skills that appear after or within such text if they are explicitly stated.
Examples:
   * "ADDITIONAL INFORMATION" → remove
   * "Professional Experience" → remove
   * "https://github.com/example" → remove

7. Preserve the original wording and capitalization of each skill. Do not normalize, standardize, correct, expand, or infer skill names.
Examples:
   * Do not change "Java Script" to "JavaScript".
   * Do not change "Service Now" to "ServiceNow".
   * Do not expand "PMP" unless the expanded phrase is present.
   * Do not change ".net" to ".NET".

8. Do not infer, add, or assume skills that are not explicitly mentioned in the input.

9. Remove duplicate skills across all annotated spans of the same resume. Treat differences in capitalization alone as duplicates, and keep the first occurrence.
Examples:
   * "Java", "Java" → "Java"
   * "python", "Python" → "python"

10. Preserve version numbers and editions when they are explicitly part of the skill name.
Examples:
   * "Python 3.11"
   * "Oracle 10g"
   * "Windows Server 2003"

11. Split slash-separated expressions only when the slash clearly separates distinct skills. Otherwise, keep the original expression unchanged.
Examples:
   * "Windows95/98/XP/NT" → "Windows 95", "Windows 98", "Windows XP", "Windows NT"
   * "HTML/CSS" → "HTML", "CSS"
   * "PL/SQL" remains one skill.
   * "TCP/IP" remains one skill.

12. Ignore malformed truncation markers such as "[…]". Extract only the text that is explicitly present and identifiable as a skill.

Return valid JSON only, using exactly this schema:

{
"skills": [
"skill 1",
"skill 2"
]
}

Do not provide explanations, comments, confidence scores, categories, or markdown.
""".strip()



def build_user_prompt(skill_spans: list[str]) -> str:
    """
    Builds a user prompt for the LLM based on the provided skill spans.

    Args:
        skill_spans (list[str]): A list of skill spans to include in the prompt.
    """
    skill_spans_json = json.dumps(
    {"skill_spans": skill_spans},
    ensure_ascii=False,
    indent=2,
)
    return (
    "The following JSON contains all annotated skill spans from a single resume.\n\n"
    f"{skill_spans_json}"
)

def build_user_prompts(samples: list[ResumeSample]) -> list[str]:
    """
    Build one user prompt per resume sample.

    Args:
        samples: Resume samples to process.

    Returns:
        Prompts in the same order as the input samples.
    """
    return [build_user_prompt(sample.skills) for sample in samples]

def parse_skills(response_str: str) -> list[str]:
    """
    Parses the LLM response to extract the list of skills.

    Args:
        response_str (str): The raw response string from the LLM.

    Returns:
        list[str]: A list of extracted skills.
    """
    try:
        response_json = json.loads(response_str)
        return response_json.get("skills", [])
    except json.JSONDecodeError:
        print("[ERROR] Failed to parse JSON from LLM response.")
        return []
    
def split_skills(
    skill_spans: list[str],
    client: LLMClient,
    model: str,
) -> list[str]:
    """
    Split annotated skill spans into individual skills.
    """
    response_text = client.generate(
        model=model,
        system_prompt=SYSTEM_PROMPT,
        user_prompt=build_user_prompt(skill_spans),
    )

    return parse_skills(response_text)