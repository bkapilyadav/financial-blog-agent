import requests
from bs4 import BeautifulSoup

def extract_full_text(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove unwanted tags
        for tag in soup(['script', 'style', 'noscript', 'iframe']):
            tag.decompose()
        
        text = ' '.join(p.get_text() for p in soup.find_all(['p', 'h1', 'h2', 'li']))
        return text.strip()
    except Exception as e:
        return f"Error while scraping: {str(e)}"
