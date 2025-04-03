from patchright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        with p.chromium.launch_persistent_context(
            user_data_dir="browser", 
            channel="chrome", 
            headless=False, 
            no_viewport=True, 
            ) as browser:

            page = browser.pages[0]
            page.set_default_navigation_timeout(0)
            page.set_default_timeout(0)

if __name__ == "__main__":
    main()