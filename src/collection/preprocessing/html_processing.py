from bs4 import BeautifulSoup
from html import unescape

def process_html_content(html_content: str) -> str:
    """
    Process the HTML content of a job description to extract plain text.

    Args:
        html_content (str): The HTML content of the job description.

    Returns:
        str: The extracted plain text from the HTML content.
    """
    decoded = unescape(html_content)
    soup = BeautifulSoup(decoded, "html.parser")
    return soup.get_text(separator="\n", strip=True)