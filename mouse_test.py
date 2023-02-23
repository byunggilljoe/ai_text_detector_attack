import numpy as np
import time
from playwright.sync_api import sync_playwright
import pyperclip

SUPPORTED = True
try:
    import pynput
    from pynput.mouse import Button, Controller
    from pynput.keyboard import Key
    from pynput import mouse, keyboard
except:
    SUPPORTED = False

class OpenAIDetector:
    def __init__(self):
        if SUPPORTED == False:
            print("[BG] pynput is not supported possibly because of non-gui environment")
            assert(False)
        self.TEXTAREA_POS = (888, 848)
        self.SUBMIT_POS = (652, 1208)
        self.RESULT_POS = (652, 1270)

    def get_prob(self, text, delay=5):
        pyperclip.copy(text)
        mouseController = mouse.Controller()
        keyboardController = keyboard.Controller()
        
        mouseController.position = self.TEXTAREA_POS
        mouseController.press(Button.left)
        mouseController.release(Button.left)

        keyboardController.press(key=Key.ctrl_l)
        keyboardController.press(key='a')
        keyboardController.release(key=Key.ctrl_l)
        keyboardController.release(key='a')
        time.sleep(0.1)
        keyboardController.press(key=Key.ctrl_l)
        keyboardController.press(key='v')
        keyboardController.release(key=Key.ctrl_l)
        keyboardController.release(key='v')

        mouseController.position = self.SUBMIT_POS
        sys.exit(0)        
        mouseController.press(Button.left)
        mouseController.release(Button.left)
        
        mouseController.position = self.RESULT_POS
        time.sleep(delay)

        MAX_TRIAL = 100
        count = 0


        while True:
            mouseController.press(Button.left)
            mouseController.release(Button.left)
            mouseController.press(Button.left)
            mouseController.release(Button.left)
            mouseController.press(Button.left)
            mouseController.release(Button.left)
            
            keyboardController.press(key=Key.ctrl_l)
            keyboardController.press(key='c')
            keyboardController.release(key=Key.ctrl_l)
            keyboardController.release(key='c')
            time.sleep(0.1)
            result_str = pyperclip.paste()
            if "to be" in result_str:
                result_str = result_str.split("to be ")[1].split(" AI-")[0]
                ai_prob_dict = {
                    "very unlikely":0.1,
                    "unlikely":0.25,
                    "unclear if it is":0.5,
                    "possibly":0.75,
                    "likely":0.9
                }
                real_percent = 1 - ai_prob_dict[result_str]

                time.sleep(0.1)

                

                return [1 - real_percent, real_percent]
            else:
                count += 1
                if count > MAX_TRIAL:
                    count = 0
                    
                    keyboardController.press(key=Key.ctrl_l)
                    keyboardController.press(key='r')
                    keyboardController.release(key=Key.ctrl_l)
                    keyboardController.release(key='r')

                    return self.get_prob(text)


# 0. clipboard edit
# 1. Mouse move to text area (888, 1148)
# 2. click
# 3. ctrl + a
# 4. ctrl + v

# 3. Mouse move to submit buton (506, 1457)
# 4. click 
# 5. Mouse move to result text (504, 1153)
# 6. Drag left to right or tripple click
# 7. Ctrl + C

if __name__ == "__main__":
    def on_move(x, y):
        print('Pointer moved to {0}'.format(
            (x, y)))

    def on_click(x, y, button, pressed):
        print('{0} at {1}'.format(
            'Pressed' if pressed else 'Released',
            (x, y)))
        if not pressed:
            # Stop listener
            return False

    def on_scroll(x, y, dx, dy):
        print('Scrolled {0} at {1}'.format(
            'down' if dy < 0 else 'up',
            (x, y)))

    # Collect events until released
    with mouse.Listener(
            on_move=on_move,
            on_click=on_click,
            on_scroll=on_scroll) as listener:
        listener.join()

    # ...or, in a non-blocking fashion:
    listener = mouse.Listener(
        on_move=on_move,
        on_click=on_click,
        on_scroll=on_scroll)
    listener.start()


    # wd = OpenAIDetector()
    # p = wd.get_prob("Yes, I am aware of ACT-1 (Adaptive Computation Time) from OpenAI's Adept project. It is a method for dynamically controlling the computation time of AI models, such as GPT-3, to balance speed and accuracy. The aim of ACT-1 is to provide a more efficient and effective use of computational resources in real-world applications, by allowing the model to allocate more or less time to processing a task based on its complexity and the available computational resources. By doing this, ACT-1 helps to reduce energy consumption, lower latency, and increase the overall performance of AI models. Yes, I am aware of ACT-1 (Adaptive Computation Time) from OpenAI's Adept project. It is a method for dynamically controlling the computation time of AI models, such as GPT-3, to balance speed and accuracy. The aim of ACT-1 is to provide a more efficient and effective use of computational resources in real-world applications, by allowing the model to allocate more or less time to processing a task based on its complexity and the available computational resources. By doing this, ACT-1 helps to reduce energy consumption, lower latency, and increase the overall performance of AI models.")
    # print(p)
