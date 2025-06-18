from playwright.sync_api import sync_playwright

def connect_to_remote_browser():
    with sync_playwright() as p:
        # Connect to the remote CDP endpoint
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        
        # When using connect_over_cdp(), you need to use browser.contexts[0].pages
        # or create a new context first
        if len(browser.contexts) > 0 and len(browser.contexts[0].pages) > 0:
            page = browser.contexts[0].pages[0]
        else:
            # Create a new context and page if none exists
            context = browser.new_context()
            page = context.new_page()
        
        # Navigate to target website
        page.goto("https://www.amazon.com")
        
        # Perform ad analysis operations
        # For example, extract ad elements
        ad_elements = page.query_selector_all('.ad-class')
        for ad in ad_elements:
            content = ad.inner_text()
            print(f"Ad content: {content}")
        
        # Take screenshot
        page.screenshot(path="screenshot.png")
        
        # Close browser connection
        browser.close()

if __name__ == "__main__":
    connect_to_remote_browser()