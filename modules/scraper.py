import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def normalize_url(url):
    parsed = urlparse(url)
    if parsed.netloc.startswith("m."):
        return url.replace("m.economictimes.com", "economictimes.com")
    return url

def scrape_content(url):
    try:
        url = normalize_url(url)
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")

        # Most ET articles are inside this div class
        main_content = soup.find('div', class_='artText')

        if not main_content:
            paragraphs = soup.find_all('p')
        else:
            paragraphs = main_content.find_all('p')

        text = ""
        for p in paragraphs:
            txt = p.get_text(strip=True)
            if len(txt) > 40 and "also read" not in txt.lower():
                text += txt + " "

        return text.strip()
    except Exception as e:
        return None
