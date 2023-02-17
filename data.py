import json

def load_dataset():
    f = open("./generator_mega_dataset_p0.94.jsonl")
    text_list = []
    label_list = []
    

    for l in f.readlines():
        line = json.loads(l)

        text_list.append(line["article"])
        label_list.append(line["label"])
    
    return text_list, label_list

