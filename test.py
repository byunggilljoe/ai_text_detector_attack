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
import editdistance

class MyClassifier(oa.Classifier):
    def __init__(self, detector):
        self.model = detector
    
    def get_pred(self, input_):
        return self.get_prob(input_).argmax(axis=1)
    
    def remove_tokenize_artifact(self, sent):
        # return sent
    
        rep_pair_list = [(" .", "."), (" ?", "?"), (" - ", "-"), (" :", ":"), ("( ", "("), (" )", ")"), (" ’ ", "’"),\
                         (" ' s", "'s"), ("s ' ", "s' "),  (" '", "'"), (" ,", ","), ("“ ", "“"), (" ”", "”"), ("\" ", "\""),\
                         (" \"", "\""), (" / ", "/")]
        for rp in rep_pair_list:
            sent = sent.replace(rp[0], rp[1])
        return sent
    
    # access to the classification probability scores with respect input sentences
    def get_prob(self, input_):
        # preprocess unwanted changes
        ret = []
        for sent in input_:
            sent = self.remove_tokenize_artifact(sent)
            res = self.model.get_prob(sent)
            # print("[BG] sent:", sent, "res:", res )
            ret.append(res)
        return np.array(ret)#.squeeze(1)


attack_name = sys.argv[1]
victim_name = sys.argv[2]
start_index = int(sys.argv[3]) if len(sys.argv) == 4 else 0

detector_dict = {"writer":WriterDetector, \
                "gpt2":GPT2Detector, \
                
                "corrector": CorrectorDetector, \
                "openai":OpenAIDetector, \

                "contentatscale":ContentAtScaleDetector, \

                "sapling": SaplingDetector, \
                "gptkit":GPTKitDetector, \
                }

attacker_dict = {"hotflip":oa.attackers.HotFlipAttacker, \
                "genetic":lambda: oa.attackers.GeneticAttacker(pop_size=10, max_iters=100),
                "gan":oa.attackers.GANAttacker,
                "pwws":oa.attackers.PWWSAttacker,
                "pso":oa.attackers.PSOAttacker,
                "deepwordbug":oa.attackers.DeepWordBugAttacker,
                "viper":oa.attackers.VIPERAttacker
                }



victim = MyClassifier(detector_dict[victim_name]())
attacker = attacker_dict[attack_name]()
attack_eval = oa.AttackEval(attacker, victim, invoke_limit=400)

# attack_eval.eval([{"x":"Yes, I am aware of ACT-1 (Adaptive Computation Time) from OpenAI's Adept project. It is a method for dynamically controlling the computation time of AI models, such as GPT-3, to balance speed and accuracy. The aim of ACT-1 is to provide a more efficient and effective use of computational resources in real-world applications, by allowing the model to allocate more or less time to processing a task based on its complexity and the available computational resources. By doing this, ACT-1 helps to reduce energy consumption, lower latency, and increase the overall performance of AI models.", "y":0.0}], visualize=True)
# attack_eval.eval([{"x":"Personal injury law is an area of the law that deals with cases involving physical or psychological harm caused by another person, company, government agency, or other entity. It covers a wide range of legal issues, from medical malpractice to car accidents to workplace injuries. In this blog post, we’ll take a look at what personal injury law entails and how it can help you if you’ve been injured due to someone else’s negligence. First and foremost, personal injury law is designed to provide compensation for victims who have suffered physical or psychological harm due to another party’s negligence. This includes both economic damages (such as medical bills and lost wages) and non-economic damages (such as pain and suffering). The goal of personal injury law is to make sure that victims are made whole again after an accident or incident.", "y":0.0}], visualize=True)

def restart(i, success_cnt, attack_cnt, misclassificatin_cnt, f=None):
    import shlex
    import subprocess

    cmd = f"python {sys.argv[0]} {sys.argv[1]} {sys.argv[2]} {i}"
    cmds = shlex.split(cmd)
    p = subprocess.Popen(cmds, start_new_session=True)
    MSG = f"[BG] Restart {i}, until: {success_cnt}, {attack_cnt}, {attack_cnt + misclassificatin_cnt}" + "\n"
    print(MSG)

    if f is not None:
        f.write(MSG)
        f.flush()

    sys.exit()

f = open(f"output/{attack_name}_{victim_name}.txt", "w" if start_index == 0 else "a", encoding='utf-8')

if __name__ == "__main__":
    text_list, label_list = load_dataset()
    success_cnt = 0
    attack_cnt = 0
    misclassificatin_cnt = 0

    for i in range(start_index, len(text_list)):
        try:
            # restart to prevent unkown errors (javascript garbage collection error, reload hangs)
            if (attack_cnt + misclassificatin_cnt)%100 == 99:
                restart()

            ss = text_list[i][:1200].replace("\n", " ").lower()
            if len(ss) < 1100:
                print("[BG] Skip because it is too short.")
                continue
            if label_list[i] == "machine" and victim.get_pred([ss])[0] == 0:
                summary = attack_eval.eval([{"x":ss, "y":0.0}], visualize=True)
                attack_cnt += 1
                success_cnt += summary["Attack Success Rate"]

                if summary["Attack Success Rate"] > 0:
                    f.write("============")
                    # print("summary.keys():", summary.keys())
                    artifact_removed_adv_example = victim.remove_tokenize_artifact(summary['x_adv_list'][0])
                    ed = editdistance.eval(summary['x_orig_list'][0],  artifact_removed_adv_example)
                    f.write(f"index: {i}, invoke_time: {summary['Avg. Victim Model Queries']}, edit_dist: {ed}\n")
                    f.write(str(summary["y_orig_list"][0]) + ", " + summary["x_orig_list"][0] + "\n")
                    f.write(str(summary["y_adv_list"][0]) + ", " + artifact_removed_adv_example + "\n")
                    f.flush()

                print("===>> ", success_cnt, attack_cnt, attack_cnt+misclassificatin_cnt, flush=True)
            else:
                # print("[BG] misclassified:", ss)
                misclassificatin_cnt += 1
        except:
            restart(i, success_cnt, attack_cnt, misclassificatin_cnt, f)

    print("===>> ", success_cnt, attack_cnt+misclassificatin_cnt)