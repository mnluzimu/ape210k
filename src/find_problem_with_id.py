import json
from tqdm import tqdm

def save_jsonl(datas, file_name):
    with open(file_name, "w", encoding="utf-8") as f:
        for data in datas:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")

def load_json(in_file):
    with open(in_file, "r", encoding="utf-8") as f:
        datas = [json.loads(line) for line in f]
    return datas

if __name__ == "__main__":
    new_datas = []
    ids = []
    datas = load_json("/mnt/cache/luzimu/datasets_ch/ape210k/outs/processed/train.jsonl")
    with open("/mnt/cache/k12_data/test.jsonl", "r") as f:
        for line in f:
            print(line)
            id = line[5:-2]
            print(id)
            ids.append(id)
        
    print(ids)
    for data in tqdm(datas):
        if data["id"] in ids:
            new_datas.append(data)
            
    save_jsonl(new_datas, "/mnt/cache/luzimu/datasets_ch/ape210k/outs/train_code/gpt_code_wrong_problem_and_gt.jsonl")
        