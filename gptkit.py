import numpy as np
import time
from playwright.sync_api import sync_playwright

class GPTKitDetector:
    def __init__(self):
        URL = "https://gptkit.ai/"
        
        playwright = sync_playwright().start()

        browser = playwright.chromium.launch(headless=False, channel="msedge")
        context = browser.new_context()

        self.page = context.new_page()
        self.page.goto(URL)

    def get_prob(self, text, delay=5.0):
        # find elements by property
        self.page.locator("[id=\"textarea\"]").fill(text)
        # find elements by type
        self.page.locator("[type=\"submit\"]").nth(1).click()
        time.sleep(delay)
        
        percent=float(self.page.locator(".py-3 .w-full").nth(0).text_content().split("%")[0].strip())/100.0
        return [1-percent, percent]