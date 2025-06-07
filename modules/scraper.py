from playwright.sync_api import sync_playwright

def scrape_with_playwright(url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=60000)
            page_content = page.content()
            page_text = page.inner_text('body')
            browser.close()
            return page_text
    except Exception as e:
        return None
