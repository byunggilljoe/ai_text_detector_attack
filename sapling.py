# It does not output probability
import numpy as np
import time
from playwright.sync_api import sync_playwright

class SaplingDetector:
    def __init__(self):
        URL = "https://sapling.ai/utilities/ai-content-detector"
        
        playwright = sync_playwright().start()

        browser = playwright.chromium.launch(headless=False, channel="msedge")
        context = browser.new_context()

        self.page = context.new_page()
        self.page.goto(URL)

    def get_prob(self, text, delay=0.5):
        # find elements by property
        self.page.locator("[id=\"content-editor\"]").fill("")
        time.sleep(delay)
        self.page.locator("[id=\"content-editor\"]").fill(text)
        
        while True:
            time.sleep(0.5)
            #print(self.page.locator("[id=\"generated-result\"]").text_content())
            if self.page.locator("[id=\"generated-result\"]").text_content().strip().startswith("Real"):
                break
            
        # print()
        real_percent=float(self.page.locator("[id=\"generated-result\"]").text_content().strip().split("probability")[1].split("Fake")[0].strip())/100.0
        return [1 - real_percent, real_percent]

if __name__ == "__main__":
    wd = SaplingDetector()
    p = wd.get_prob("Yes, I am aware of ACT-1 (Adaptive Computation Time) from OpenAI's Adept project. It is a method for dynamically controlling the computation time of AI models, such as GPT-3, to balance speed and accuracy. The aim of ACT-1 is to provide a more efficient and effective use of computational resources in real-world applications, by allowing the model to allocate more or less time to processing a task based on its complexity and the available computational resources. By doing this, ACT-1 helps to reduce energy consumption, lower latency, and increase the overall performance of AI models.")
    print(p)

# https://gptzero.me/