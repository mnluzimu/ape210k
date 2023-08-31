import os
import pandas as pd
import json

def save_jsonl(datas, file_name):
    with open(file_name, "w", encoding="utf-8") as f:
        for data in datas:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")

def load_json(in_file):
    with open(in_file, "r", encoding="utf-8") as f:
        datas = [json.loads(line) for line in f]
    return datas

def orig_to_processed(in_file, out_file):
    datas = load_json(in_file)
    new_datas = []
    for data in datas:
        new_data = {
            "id": data["id"],
            "question": data["original_text"],
            "answer": data["ans"],
            "equation": data["equation"]
        }
        new_datas.append(new_data)

    save_jsonl(new_datas, out_file)

if __name__ == "__main__":

    orig_to_processed("/mnt/cache/luzimu/datasets_ch/ape210k/data/test.ape.json", "/mnt/cache/luzimu/datasets_ch/ape210k/processed/test.jsonl")
    orig_to_processed("/mnt/cache/luzimu/datasets_ch/ape210k/data/train.ape.json", "/mnt/cache/luzimu/datasets_ch/ape210k/processed/train.jsonl")
    orig_to_processed("/mnt/cache/luzimu/datasets_ch/ape210k/data/valid.ape.json", "/mnt/cache/luzimu/datasets_ch/ape210k/processed/valid.jsonl")

