# It does not output probability
import numpy as np
import time
from playwright.sync_api import sync_playwright

class CopyleaksDetector:
    def __init__(self):
        URL = "https://copyleaks.com/features/ai-content-detector"
        
        playwright = sync_playwright().start()

        browser = playwright.chromium.launch(headless=False, channel="msedge")
        context = browser.new_context()

        self.page = context.new_page()
        self.page.goto(URL)

    def get_prob(self, text, delay=2):
        # find elements by property
        self.page.locator(".scan-text-editor").fill(text)
        time.sleep(delay)
        # while True:
        #     time.sleep(0.5)
        #     if self.page.locator("[id=\"message\"]").text_content().startswith("Prediction based "):
        #         break
            
        # print()
        real_percent=float(self.page.locator("[id=\"real-percentage\"]").text_content().strip().split("%")[0])/100.0
        return [1 - real_percent, real_percent]

if __name__ == "__main__":
    wd = GPT2Detector()
    p = wd.get_prob("Yes, I am aware of ACT-1 (Adaptive Computation Time) from OpenAI's Adept project. It is a method for dynamically controlling the computation time of AI models, such as GPT-3, to balance speed and accuracy. The aim of ACT-1 is to provide a more efficient and effective use of computational resources in real-world applications, by allowing the model to allocate more or less time to processing a task based on its complexity and the available computational resources. By doing this, ACT-1 helps to reduce energy consumption, lower latency, and increase the overall performance of AI models.")
    print(p)

# https://gptzero.me/