import numpy as np
import time
from playwright.sync_api import sync_playwright
import code
class ContentAtScaleDetector:
    def __init__(self):
        URL = "https://contentatscale.ai/ai-content-detector/"
        
        playwright = sync_playwright().start()

        browser = playwright.chromium.launch(headless=True, channel="msedge")
        context = browser.new_context()

        self.page = context.new_page()
        self.page.goto(URL)

    def get_prob(self, text, delay=5.0):
        # find elements by property
        self.page.locator(".editor").fill(text)
        # find elements by type
        self.page.locator(".check-ai-score").nth(0).click()
        time.sleep(delay)
        MAX_TRIAL = 100
        count = 0
        while True:
            time.sleep(0.1)
            # print(self.page.locator(".det-details").text_content())
            if self.page.locator(".det-details").text_content().strip().endswith("words."):
                break
            
            count += 1
            if count > MAX_TRIAL:
                self.page.reload()
                return self.get_prob(text)

        percent=float(self.page.locator(".progress-circle").text_content().split("%")[0].strip())/100.0
        return [1-percent, percent]

if __name__ == "__main__":
    wd = ContentAtScaleDetector()
    time.sleep(1)
    wd.page.locator(".editor").fill("Personal injury law is an area of the law that deals with cases involving physical or psychological harm caused by another person, company, government agency, or other entity. It covers a wide range of legal issues, from medical malpractice to car accidents to workplace injuries. In this blog post, we’ll take a look at what personal injury law entails and how it can help you if you’ve been injured due to someone else’s negligence.")
    wd.page.locator(".check-ai-score").nth(0).click()
    time.sleep(5)
    print(float(wd.page.locator(".progress-circle").text_content().split("%")[0].strip())/100.0)
    code.interact(local=locals())
    while True:
        pass

# https://gptzero.me/