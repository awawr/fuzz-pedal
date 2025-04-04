import time
import random
import string
from bs4 import BeautifulSoup
from patchright.sync_api import sync_playwright
from pymailtm import MailTm, Account

brainrot = ["skibidi", "toilet", "rizz", "brainrot", "gyatt", "ohio", "tax", "gooner", "comp"]
names = ["zentrr", "arctic", "rodrigo", "gonzalez"]
triggers = ["pedo", "minor", "racist", "hard r"]
char = ["o", "j", "0", "x", "1", "l", "9"]
char2 = ["y", "F", "0", "a", "g", "9", "6"]

def generate_userpass():
    username = random.choice(brainrot) + random.choice(names) + random.choice(triggers)
    password = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    return (username, password)

def verify_email(email):
    email_html = None
    messages = None
    while True: 
        messages = email.get_messages()
        if (len(messages) >= 2): # Wait for 2 or more messages to be received
            break
        time.sleep(3)
    for i in range(len(messages)):
        if "please confirm your email address" in messages[i].subject: # Find confirmation email
            email_html = str(messages[i].html)
            break
    soup = BeautifulSoup(email_html, features="html.parser") # Parse email HTML
    verify_link = None
    links = soup.select('a[style="background-color:#f12c18; border:0px solid #f12c18; border-color:#f12c18; border-radius:50px; border-width:0px; color:#ffffff; display:inline-block; font-size:16px; font-weight:bold; letter-spacing:0px; line-height:normal; padding:10px 20px 10px 20px; text-align:center; text-decoration:none; border-style:solid; font-family:helvetica,sans-serif;"]')
    for link in links:
        verify_link = link.get("href")
    return verify_link

def generate_account(email: Account, name: str, password: str, talents: list[str], genres: list[str], artists: list[str], username: str = None, profile_pic: str = None):
    with sync_playwright() as p:
        with p.chromium.launch_persistent_context(
            user_data_dir="browser", 
            channel="chrome", 
            headless=False, 
            no_viewport=True
            ) as browser:

            browser.clear_cookies() # Clear old cookies
            page = browser.pages[0]
            page.set_default_navigation_timeout(0)
            page.set_default_timeout(0)
            page.goto('https://www.bandlab.com/sign-up')
            page.get_by_placeholder("Enter your name").fill(name) # Name
            page.get_by_placeholder("you@example.com").fill(email.address) # Email
            page.get_by_placeholder("Enter at least 6 characters").fill(password) # Password
            page.locator("select[ng-model='pickDate.day']").select_option("1") # Day
            page.locator("select[ng-model='pickDate.month']").select_option("1") # Month
            page.locator("select[ng-model='pickDate.year']").select_option("2000") # Year
            page.get_by_role("button", name="Sign up").click()

            page.wait_for_url("https://www.bandlab.com/onboarding")
            if profile_pic != None:
                page.locator("div[class='quick-upload-cover-cta form-field-upload-picture-img-circle']").click()
                page.locator("input[type='file']").set_input_files(profile_pic)
                page.get_by_role("button").get_by_text("Upload Picture").click() # Upload profile picture
            if (username != None):
                page.get_by_placeholder("Set a custom username").fill(username) # Username
            page.get_by_role("button", name="Continue").click()
            page.wait_for_selector("div[class='complete-profile-goals']")
            page.get_by_role("button", name="Continue").click()

            # Talents
            t_element = page.get_by_label("Tell Us More About You")
            for t in talents:
                try:
                    t_element.get_by_text(t).click()
                except:
                    print(f"No talent found for: {t}")
            page.get_by_role("button", name="Continue").click()

            # Favourite genres
            g_element = page.get_by_label("Pick Your Favorite Genres")
            for g in genres:
                try:
                    g_element.get_by_text(g).click()
                except:
                    print(f"No genre found for: {t}")
            page.get_by_role("button", name="Continue").click()

            # Search and select inspired-by artists
            for a in artists:
                page.get_by_placeholder("Search Artists…").fill(a)
                page.locator("div[class='mentions-suggestions-fullname']").filter(has_text=a).nth(1).click()
            page.get_by_role("button", name="Done").click()

            page.wait_for_url("https://www.bandlab.com/feed/trending") # Wait for sign up to finish

            page.goto(verify_email(email))
            page.wait_for_selector("svg[style='color: var(--ds-color-tint-green-base)']")

def main():
    client = MailTm()
    account = client.get_account() # Create temp email
    userpass = generate_userpass()
    generate_account(account, userpass[0], userpass[1], ["Other"], ["Other"], ["Deez Nuts"])
    
if __name__ == "__main__":
    main()