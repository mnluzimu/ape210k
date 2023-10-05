import json
import os
import re
from latex2sympy2 import latex2sympy
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
    datas = load_json("/mnt/cache/luzimu/datasets_ch/ape210k/outs/wk_data/run_results/out0.jsonl")
    split_num = 10000
    n = len(datas) // split_num + 1
    for i in range(n):
        # new_datas = [{"question":data["messages"][1]["content"][0]["content"], "id":data["id"]} for data in datas[i * split_num: i * split_num + split_num]]
        new_datas = [data for data in datas[i * split_num: i * split_num + split_num]]
        save_jsonl(new_datas, f"/mnt/cache/luzimu/datasets_ch/ape210k/outs/wk_data/run_results_0/{i}_result.jsonl")