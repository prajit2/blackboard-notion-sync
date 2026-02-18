import os
import json
import re
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

# Initialize environment variables from .env file
load_dotenv()

# Path to the user's browser profile to maintain login sessions (e.g., Blackboard/Duo)
# For GitHub users: Set this in your .env to avoid re-authenticating every run
COMET_PROFILE_PATH = os.getenv("COMET_PROFILE_PATH")

def scrape_calendar():
    """
    Automates the navigation to Drexel Blackboard's calendar and extracts
    assignment names, course codes, and due dates.
    """
    with sync_playwright() as p:
        # Launching a persistent context allows the scraper to use saved cookies/sessions
        browser = p.chromium.launch_persistent_context(
            user_data_dir=COMET_PROFILE_PATH,
            channel="chrome",
            headless=False  # Set to True for headless/background execution
        )

        page = browser.new_page()
        print("Navigating to Blackboard Calendar...")
        # Direct URL to the Ultra Calendar view
        page.goto("https://learn.dcollege.net/ultra/calendar")

        # Interactive pause: Blackboard often requires 2FA (Duo)
        print("\n👉 STEP 1: Complete login/Duo if prompted.")
        print("👉 STEP 2: Ensure 'Due Dates' list view is active.")
        print("👉 STEP 3: Press ENTER in this terminal once the assignments appear.")
        input("Waiting for user to confirm calendar view...")

        print("Searching for assignment elements...")
        try:
            # Wait for the specific element cards found in Blackboard Ultra's DOM
            page.wait_for_selector("div.element-card", timeout=15000)
        except Exception:
            print("❌ Error: Element 'div.element-card' not found. Check login status.")
            browser.close()
            return []

        # Scrape all visible assignment cards
        items = page.query_selector_all("div.element-card")
        scraped_results = []

        for item in items:
            try:
                # Extract Assignment Title
                assignment_el = item.query_selector("a")
                assignment = assignment_el.inner_text().strip() if assignment_el else "Unknown"

                # Extract metadata block (contains Course and Date)
                details_el = item.query_selector("div.element-details")
                details_text = details_el.inner_text() if details_el else ""

                # Regex to isolate course codes like CS-171 or PHYS-101
                match = re.search(r'[A-Z]{2,4}-\d{3}', details_text)
                course_code = match.group(0) if match else "Other"

                # Parse the specific 'Due date:' line from the details block
                due_info = "No Date"
                for line in details_text.split('\n'):
                    if "Due date:" in line:
                        due_info = line.replace("Due date:", "").strip()
                        break

                print(f"✅ Found: [{course_code}] - {assignment} | Due: {due_info}")

                scraped_results.append({
                    "course": course_code,
                    "assignment": assignment,
                    "due": due_info
                })
            except Exception as e:
                # Log errors for individual items but continue scraping the rest
                print(f"⚠️ Item Parsing Error: {e}")
                continue

        browser.close()
        return scraped_results

if __name__ == "__main__":
    # Main entry point: Scrape and save to JSON for the sync script to consume
    final_data = scrape_calendar()

    if final_data:
        with open('blackboard_data.json', 'w') as f:
            json.dump(final_data, f, indent=4)
        print(f"\n🚀 Success! {len(final_data)} items saved to blackboard_data.json")
    else:
        print("\n⚠️ Scraping failed. No data written.")