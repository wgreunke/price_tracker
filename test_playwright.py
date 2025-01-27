#https://screenshotone.com/blog/how-to-take-website-screenshots-in-python/#playwright-in-python
from playwright.sync_api import sync_playwright

#Asks me to install playwright but then get error.

def run(playwright):
    # launch the browser
    browser = playwright.chromium.launch()
    # opens a new browser page
    page = browser.new_page()
    # navigate to the website
    page.goto('https://www.google.com')
    # take a full-page screenshot
    page.screenshot(path='example.png', full_page=True)
    # always close the browser
    browser.close()

with sync_playwright() as playwright:
    run(playwright)