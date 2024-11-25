from bs4 import BeautifulSoup

def is_valid_html(fragment: str) -> bool:
    """Check if the given fragment is a valid HTML document."""
    soup = BeautifulSoup(fragment, "html.parser")
    return bool(soup.find())
