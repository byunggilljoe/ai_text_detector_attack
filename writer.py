import numpy as np
import time
from playwright.sync_api import sync_playwright

class WriterDetector:
    def __init__(self):
        URL = "https://writer.com/ai-content-detector/"
        
        playwright = sync_playwright().start()

        browser = playwright.chromium.launch(headless=False, channel="msedge")
        context = browser.new_context()

        self.page = context.new_page()
        self.page.goto(URL)

    def get_prob(self, text, delay=2.0):
        # find elements by property
        self.page.locator(".ai_textbox").fill("")
        self.page.locator(".ai_textbox").click()
        self.page.keyboard.type(text)
        # find elements by type
        self.page.locator("[type=\"submit\"]").nth(0).click()
        time.sleep(delay)

        MAX_TRIAL = 100
        count = 0

        while True:
            time.sleep(0.1)
            if "dc-btn-gradient_loading" not in self.page.locator("[type=\"submit\"]").nth(0).get_attribute("class"):
                break
            
            count += 1
            if count > MAX_TRIAL:
                self.page.reload()
                return self.get_prob(text)
            

        percent=float(self.page.locator(".ai-percentage-val-wrap").nth(0).text_content().split("%")[0].strip())/100.0
        return [1-percent, percent]

if __name__ == "__main__":
    wd = WriterDetector()
    time.sleep(1)
    wd.page.locator(".ai_textbox").fill("")
    wd.page.locator(".ai_textbox").click()
    wd.page.keyboard.type("Yes, I am aware of ACT-1 (Adaptive Computation Time) from OpenAI's Adept project. It is a method for dynamically controlling the computation time of AI models, such as GPT-3, to balance speed and accuracy. The aim of ACT-1 is to provide a more efficient and effective use of computational resources in real-world applications, by allowing the model to allocate more or less time to processing a task based on its complexity and the available computational resources. By doing this, ACT-1 helps to reduce energy consumption, lower latency, and increase the overall performance of AI models.")
    wd.page.locator("[type=\"submit\"]").nth(0).click()
    
    time.sleep(1)
    while True:
        time.sleep(0.1)
        print(wd.page.locator("[type=\"submit\"]").nth(0).get_attribute("class"))
        if "dc-btn-gradient_loading" not in wd.page.locator("[type=\"submit\"]").nth(0).get_attribute("class"):
            break
    percent=float(wd.page.locator(".ai-percentage-val-wrap").nth(0).text_content().split("%")[0].strip())/100.0
    print(percent)
    while True:
        pass

# https://gptzero.me/