
import httpx
from bs4 import BeautifulSoup


def retrieve_page(url: str) -> dict:
    if not url.startswith(("https://", "http://")):
        raise ValueError("Only HTTP and HTTPS URLs are allowed.")

    headers = {
        "User-Agent": "DeepResearchAgent/1.0"
    }

    with httpx.Client(
        timeout=15.0,
        follow_redirects=True,
        headers=headers,
    ) as client:
        response = client.get(url)
        response.raise_for_status()

    content_type = response.headers.get(
        "content-type", ""
    )

    if "text/html" not in content_type.lower():
        raise ValueError("The URL did not return an HTML page.")

    soup = BeautifulSoup(response.text, "html.parser")

    for element in soup([
        "script",
        "style",
        "nav",
        "footer",
        "header",
        "noscript",
    ]):
        element.decompose()

    title = (
        soup.title.get_text(" ", strip=True)
        if soup.title
        else url
    )

    content = soup.get_text(" ", strip=True)

    return {
        "url": str(response.url),
        "title": title,
        "content": content[:15000],
    }