Drexel Blackboard to Notion Sync 🚀
Automate your academic schedule by syncing Blackboard assignments directly to a Notion Database. This tool uses Playwright to navigate Drexel's Blackboard Ultra calendar and the Notion API to create organized, color-coded entries.

✨ Features
- Automatic Scraping: Uses Playwright to handle Blackboard's login and extraction.
- 2FA Bypass: Uses a persistent browser context to maintain your session, avoiding repeated Duo prompts.
- Deadline Accuracy: Automatically forces all assignment times to 11:59 PM EST to prevent timezone shifting in Notion.
- Course Tagging: Uses Regex to identify and tag course codes like CS-171 or PHYS-101.
