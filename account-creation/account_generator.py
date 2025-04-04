import time
import random
from pathlib import Path
from bs4 import BeautifulSoup
from patchright.sync_api import sync_playwright
from pymailtm import MailTm

brainrot = ["skibidi", "toilet", "rizz", "brainrot", "gyatt", "ohio", "tax", "gooner", "comp"]
names = ["zentrr", "arctic", "rodrigo", "gonzalez"]
triggers = ["pedo", "minor", "racist", "hard r"]
char = ["o", "j", "0", "x", "1", "l", "9"]
char2 = ["y", "F", "0", "a", "g", "9", "6"]

def main():
    client = MailTm()
    account = client.get_account() # Create temp email
    with sync_playwright() as p:
        with p.chromium.launch_persistent_context(
            user_data_dir="browser", 
            channel="chrome", 
            headless=False, 
            no_viewport=True, 
            ) as browser:

            browser.clear_cookies() # Clear old cookies
            page = browser.pages[0]
            page.set_default_navigation_timeout(0)
            page.set_default_timeout(0)
            page.goto('https://www.bandlab.com/sign-up')
            page.get_by_placeholder("Enter your name").fill(random.choice(brainrot) + random.choice(names) + random.choice(triggers)) # Name
            page.get_by_placeholder("you@example.com").fill(account.address) # Email
            page.get_by_placeholder("Enter at least 6 characters").fill() # Password
            page.locator("select[ng-model='pickDate.day']").select_option("1") # Day
            page.locator("select[ng-model='pickDate.month']").select_option("1") # Month
            page.locator("select[ng-model='pickDate.year']").select_option("2000") # Year
            page.get_by_role("button", name="Sign up").click()

            # Todo: captcha solve

            page.wait_for_url("https://www.bandlab.com/onboarding")
            # page.locator("div[class='quick-upload-cover-cta form-field-upload-picture-img-circle']").click()
            # page.locator("input[type='file']").set_input_files("000c269a70f1e0f246ea44d947027167.jpg")
            # page.get_by_role("button").get_by_text("Upload Picture").click() # Upload profile picture
            # page.get_by_placeholder("Set a custom username").fill() # Username
            page.get_by_role("button", name="Continue").click()
            page.wait_for_selector("div[class='complete-profile-goals']")
            page.get_by_role("button", name="Continue").click()
            page.get_by_label("Tell Us More About You").get_by_text("Other").click() # Talents
            page.get_by_role("button", name="Continue").click()
            page.get_by_label("Pick Your Favorite Genres").get_by_text("Other").click() # Favourite genres
            page.get_by_role("button", name="Continue").click()
            page.get_by_placeholder("Search Artists…").fill("Deez Nuts")
            page.locator("div[class='mentions-suggestions-fullname']").filter(has_text="Deez Nuts").nth(1).click() # Click favourite artist
            page.get_by_role("button", name="Done").click()

            page.wait_for_url("https://www.bandlab.com/feed/trending") # Wait for sign up to finish

            # Terrible implementation of email verification
            email_html = None
            while True:
                messages = account.get_messages()
                if (len(messages) > 1):
                    email_html = str(messages[1].html)
                    break
                time.sleep(3)
            soup = BeautifulSoup(email_html, features="html.parser")
            verify_link = None
            links = soup.select('a[style="background-color:#f12c18; border:0px solid #f12c18; border-color:#f12c18; border-radius:50px; border-width:0px; color:#ffffff; display:inline-block; font-size:16px; font-weight:bold; letter-spacing:0px; line-height:normal; padding:10px 20px 10px 20px; text-align:center; text-decoration:none; border-style:solid; font-family:helvetica,sans-serif;"]')
            for link in links:
                verify_link = link.get("href")
            print(verify_link)
            page.goto(verify_link)
            # Todo: Email verification requires captcha solve
            input()

if __name__ == "__main__":
    main()
