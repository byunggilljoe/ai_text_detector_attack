import sys

sys.path.append("./OpenAttack-master")
import OpenAttack as oa
import numpy as np
import time
from playwright.sync_api import sync_playwright
import code
from gpt_2_detector import GPT2Detector
from writer import WriterDetector
from gptkit import GPTKitDetector
from contentatscale import ContentAtScaleDetector
from writer import WriterDetector
from corrector import CorrectorDetector
from sapling import SaplingDetector
from openaidetector import OpenAIDetector

from data import load_dataset

from OpenAttack.attack_eval.utils import attack_process
      
class MyClassifier(oa.Classifier):
    def __init__(self, detector):
        self.model = detector
    
    def get_pred(self, input_):
        return self.get_prob(input_).argmax(axis=1)

    # access to the classification probability scores with respect input sentences
    def get_prob(self, input_):

        ret = []
        for sent in input_:
            res = self.model.get_prob(sent)
            # print("[BG] sent:", sent, "res:", res )
            ret.append(res)
        return np.array(ret)#.squeeze(1)


attack_name = sys.argv[1]
victim_name = sys.argv[2]

detector_dict = {"writer":WriterDetector, \
                "gpt2":GPT2Detector, \
                "contentatscale":ContentAtScaleDetector, \
                "corrector": CorrectorDetector, \
                "openai":OpenAIDetector, \

                "sapling": SaplingDetector, \
                "gptkit":GPTKitDetector, \
                }

attacker_dict = {"hotflip":oa.attackers.HotFlipAttacker, \
                "genetic":lambda: oa.attackers.GeneticAttacker(pop_size=10, max_iters=100),
                "gan":oa.attackers.GANAttacker}

victim = MyClassifier(detector_dict[victim_name]())
attacker = attacker_dict[attack_name]()
attack_eval = oa.AttackEval(attacker, victim, invoke_limit=200)

# attack_eval.eval([{"x":"Yes, I am aware of ACT-1 (Adaptive Computation Time) from OpenAI's Adept project. It is a method for dynamically controlling the computation time of AI models, such as GPT-3, to balance speed and accuracy. The aim of ACT-1 is to provide a more efficient and effective use of computational resources in real-world applications, by allowing the model to allocate more or less time to processing a task based on its complexity and the available computational resources. By doing this, ACT-1 helps to reduce energy consumption, lower latency, and increase the overall performance of AI models.", "y":0.0}], visualize=True)
# attack_eval.eval([{"x":"Personal injury law is an area of the law that deals with cases involving physical or psychological harm caused by another person, company, government agency, or other entity. It covers a wide range of legal issues, from medical malpractice to car accidents to workplace injuries. In this blog post, we’ll take a look at what personal injury law entails and how it can help you if you’ve been injured due to someone else’s negligence. First and foremost, personal injury law is designed to provide compensation for victims who have suffered physical or psychological harm due to another party’s negligence. This includes both economic damages (such as medical bills and lost wages) and non-economic damages (such as pain and suffering). The goal of personal injury law is to make sure that victims are made whole again after an accident or incident.", "y":0.0}], visualize=True)

f = open(f"output/{attack_name}_{victim_name}.txt", "w", encoding='utf-8')
if __name__ == "__main__":
    text_list, label_list = load_dataset()
    success_cnt = 0
    total_cnt = 0
    misclassificatin_cnt = 0
    for i in range(len(text_list)):
        ss = text_list[i][:1200].lower()
        if label_list[i] == "machine" and victim.get_pred([ss])[0] == 0:
            summary = attack_eval.eval([{"x":ss, "y":0.0}], visualize=True)
            total_cnt += 1
            success_cnt += summary["Attack Success Rate"]


            f.write(str(summary["y_orig_list"][0]) + ", " + summary["x_orig_list"][0] + "\n")
            f.write(str(summary["y_adv_list"][0]) + ", " + summary["x_adv_list"][0] + "\n")
            f.flush()

            print("===>> ", success_cnt, total_cnt, misclassificatin_cnt, flush=True)
        else:
            misclassificatin_cnt +=1

    print(success_cnt, total_cnt)