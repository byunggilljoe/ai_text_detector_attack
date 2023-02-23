import sys
import numpy as np
import matplotlib.pyplot as plt


fn = sys.argv[1]

f = open(fn)

before_prob_list = []
after_prob_list = []
edit_dist_list = []
invoke_time_list = []

total_cnt = 0
attack_cnt = 0
success_cnt = 0

while True:
    l = f.readline()
    if l == "":
        break
    # print(l)
    if l.startswith("============index:"):
        invoke_time = int(float(l.split("invoke_time: ")[1].split(",")[0]))
        edit_dist = int(l.split("edit_dist: ")[1].strip())
        before_prob = float(f.readline().split(" ")[0][1:])
        after_prob = float(f.readline().split(" ")[1].split("],")[0])

        before_prob_list.append(before_prob)
        after_prob_list.append(after_prob)
        edit_dist_list.append(edit_dist)
        invoke_time_list.append(invoke_time)

    elif l.startswith("[BG] Restart"):
        summary_line = l.split("until:")[1].split(",")
        sc = int(float(summary_line[0]))
        ac = int(summary_line[1])
        tc = int(summary_line[2])
        success_cnt += sc
        attack_cnt += ac
        total_cnt += tc

print(success_cnt, attack_cnt, total_cnt)
print(success_cnt/attack_cnt, attack_cnt/total_cnt)


counts, bins = np.histogram(invoke_time_list, bins=len(invoke_time_list)*2)
plt.hist(bins[:-1], bins, weights=counts)
plt.savefig(fn.split(".txt")[0]+"_hist_invoke_time.jpg")
plt.close()

counts, bins = np.histogram(edit_dist_list, bins=len(invoke_time_list)*2)
plt.hist(bins[:-1], bins, weights=counts)
plt.savefig(fn.split(".txt")[0]+"_hist_edit_dist.jpg")
plt.close()


counts, bins = np.histogram(before_prob_list, bins=len(invoke_time_list)*2)
plt.hist(bins[:-1], bins, weights=counts)
plt.savefig(fn.split(".txt")[0]+"_hist_before_prob.jpg")
plt.close()

counts, bins = np.histogram(after_prob_list, bins=len(invoke_time_list)*2)
plt.hist(bins[:-1], bins, weights=counts)
plt.savefig(fn.split(".txt")[0]+"_hist_after_prob.jpg")
plt.close()