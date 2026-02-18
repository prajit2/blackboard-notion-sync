Drexel Blackboard to Notion Sync 🚀
Automate your academic schedule by syncing Blackboard assignments directly to a Notion Database. This tool uses Playwright to navigate Drexel's Blackboard Ultra calendar and the Notion API to create organized, color-coded entries.

✨ Features
- Automatic Scraping: Uses Playwright to handle Blackboard's login and extraction.
- 2FA Bypass: Uses a persistent browser context to maintain your session, avoiding repeated Duo prompts.
- Deadline Accuracy: Automatically forces all assignment times to 11:59 PM EST to prevent timezone shifting in Notion.
- Course Tagging: Uses Regex to identify and tag course codes like CS-171 or PHYS-101.

**Pro Shortcut Tip!**

1. Add alias to ZSH profile:
echo "alias sync-bb='cd ~/blackboard-notion-sync && source .venv/bin/activate && python3 scraper.py && python3 sync.py'" >> ~/.zshrc

2. Refresh terminal
source ~/.zshrc

3. Now just use **sync-bb** to activate the full project!

quick note - use this weekly to ensure all of your assignments are up to date
