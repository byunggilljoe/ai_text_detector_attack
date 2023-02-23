# It does not output probability
import numpy as np
import time
from playwright.sync_api import sync_playwright

class CorrectorDetector:
    def __init__(self):
        self.URL = "https://corrector.app/ai-content-detector/"
        
        playwright = sync_playwright().start()

        browser = playwright.chromium.launch(headless=True, channel="msedge")
        self.context = browser.new_context()

        self.page = self.context.new_page()
        self.page.goto(self.URL)

        self.PROB_REFRESH_COUNT = 5
        self.prob_count = 0

    def get_prob(self, text, delay=0.5):
        # refresh not to incur javascript garbage collection error
        self.prob_count += 1
        if self.prob_count > self.PROB_REFRESH_COUNT:
            self.prob_count = 0
            self.page.close()

            self.page = self.context.new_page()
            self.page.goto(self.URL)

        # find elements by property
        self.page.locator("[id=\"checktext\"]").fill("")
        time.sleep(delay)
        self.page.locator("[id=\"checktext\"]").fill(text)
        
        
        MAX_TRIAL = 5
        count = 0

        while True:
            time.sleep(0.5)
            if self.page.locator("[id=\"fakeo\"]").text_content().endswith("%"):
                break
            
            count += 1
            if count > MAX_TRIAL:
                self.page.reload()
                return self.get_prob(text)
            time.sleep(2)
            
        # print()
        real_percent=1-float(self.page.locator("[id=\"fakeo\"]").text_content().strip().split("%")[0].split(" ")[1])/100.0
        return [1 - real_percent, real_percent]

if __name__ == "__main__":
    wd = CorrectorDetector()
    p = wd.get_prob("Yes, I am aware of ACT-1 (Adaptive Computation Time) from OpenAI's Adept project. It is a method for dynamically controlling the computation time of AI models, such as GPT-3, to balance speed and accuracy. The aim of ACT-1 is to provide a more efficient and effective use of computational resources in real-world applications, by allowing the model to allocate more or less time to processing a task based on its complexity and the available computational resources. By doing this, ACT-1 helps to reduce energy consumption, lower latency, and increase the overall performance of AI models.")
    print(p)

# https://gptzero.me/