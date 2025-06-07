from playwright.sync_api import sync_playwright

def scrape_with_playwright(url: str) -> str:
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
            page = context.new_page()
            page.goto(url, timeout=60000)
            
            # Wait for main article content to load (adjust selector as per site)
            page.wait_for_selector("div.artText", timeout=30000)
            
            # Extract the content text
            content_element = page.query_selector("div.artText")
            if content_element:
                content = content_element.inner_text()
            else:
                content = ""
            
            browser.close()
            return content.strip()
    except Exception as e:
        print(f"Scraping failed: {e}")
        return ""
