import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def normalize_url(url):
    # Convert mobile URL to desktop version
    if "m.economictimes.com" in url:
        return url.replace("m.economictimes.com", "economictimes.com")
    return url

def scrape_content(url):
    try:
        url = normalize_url(url)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        # Try common class for article text on Economic Times
        article_body = soup.find("div", class_="artText")
        if not article_body:
            article_body = soup.find("div", class_="Normal")

        if not article_body:
            return None  # Fail gracefully

        paragraphs = article_body.find_all("p")
        text = ""
        for para in paragraphs:
            content = para.get_text(strip=True)
            if content and len(content) > 50:
                text += content + " "

        return text.strip() if text else None

    except Exception as e:
        return None
