"""Open the Streamlit app in a headless browser so Community Cloud counts it as a visit.
If the app is already asleep, click the wake-up button and wait for it to start."""
import re
from playwright.sync_api import sync_playwright

URL = "https://pharmapilot-ai.streamlit.app/"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(URL, wait_until="networkidle", timeout=90_000)

    wake = page.get_by_role("button", name=re.compile("get this app back up", re.I))
    if wake.count():
        print("App was asleep - waking it up")
        wake.first.click()
        page.wait_for_timeout(90_000)   # give it time to boot
    else:
        print("App is awake")
        page.wait_for_timeout(20_000)   # stay long enough to count as a visit

    browser.close()
