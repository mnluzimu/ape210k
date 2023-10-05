import json
import os
import re
from latex2sympy2 import latex2sympy
from tqdm import tqdm
import random

def save_jsonl(datas, file_name):
    with open(file_name, "w", encoding="utf-8") as f:
        for data in datas:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")

def load_jsonl(in_file):
    with open(in_file, "r", encoding="utf-8") as f:
        datas = [json.loads(line) for line in f]
    return datas

def create_new_problem_dataset(in_file, out_file):
    datas = load_jsonl(in_file)
    system_prompt = "请根据以下问题创造一道类似的新问题。"
    random.seed(3407)
    random.shuffle(datas)
    new_datas = []
    for i in range(0, len(datas), 5):
        user_prompt = ""
        if i + 5 >= len(datas):
            break
        for idx, data in enumerate(datas[i:i+4]):
            user_prompt += f"问题{idx + 1}：{data['question']}\n"
        user_prompt += "新问题："
        assistant_prompt = datas[i+5]["question"]
        system = {"role": "system", "content": [{"type": "text", "content": system_prompt}]}
        user = {"role": "user", "content": [{"type": "text", "content": user_prompt}]}
        assistant = {"role": "assistant", "content": [{"type": "text", "content": assistant_prompt}]}
        new_datas.append({"messages":[system, user, assistant]})
    random.shuffle(datas)
    for i in range(0, len(datas), 5):
        user_prompt = ""
        if i + 5 >= len(datas):
            break
        for idx, data in enumerate(datas[i:i+4]):
            user_prompt += f"问题{idx + 1}：{data['question']}\n"
        user_prompt += "新问题："
        assistant_prompt = datas[i+5]["question"]
        system = {"role": "system", "content": [{"type": "text", "content": system_prompt}]}
        user = {"role": "user", "content": [{"type": "text", "content": user_prompt}]}
        assistant = {"role": "assistant", "content": [{"type": "text", "content": assistant_prompt}]}
        new_datas.append({"messages":[system, user, assistant]})
    random.shuffle(datas)
    for i in range(0, len(datas), 5):
        user_prompt = ""
        if i + 5 >= len(datas):
            break
        for idx, data in enumerate(datas[i:i+4]):
            user_prompt += f"问题{idx + 1}：{data['question']}\n"
        user_prompt += "新问题："
        assistant_prompt = datas[i+5]["question"]
        system = {"role": "system", "content": [{"type": "text", "content": system_prompt}]}
        user = {"role": "user", "content": [{"type": "text", "content": user_prompt}]}
        assistant = {"role": "assistant", "content": [{"type": "text", "content": assistant_prompt}]}
        new_datas.append({"messages":[system, user, assistant]})
    random.shuffle(datas)
    for i in range(0, len(datas), 5):
        user_prompt = ""
        if i + 5 >= len(datas):
            break
        for idx, data in enumerate(datas[i:i+4]):
            user_prompt += f"问题{idx + 1}：{data['question']}\n"
        user_prompt += "新问题："
        assistant_prompt = datas[i+5]["question"]
        system = {"role": "system", "content": [{"type": "text", "content": system_prompt}]}
        user = {"role": "user", "content": [{"type": "text", "content": user_prompt}]}
        assistant = {"role": "assistant", "content": [{"type": "text", "content": assistant_prompt}]}
        new_datas.append({"messages":[system, user, assistant]})
    random.shuffle(datas)
    for i in range(0, len(datas), 5):
        user_prompt = ""
        if i + 5 >= len(datas):
            break
        for idx, data in enumerate(datas[i:i+4]):
            user_prompt += f"问题{idx + 1}：{data['question']}\n"
        user_prompt += "新问题："
        assistant_prompt = datas[i+5]["question"]
        system = {"role": "system", "content": [{"type": "text", "content": system_prompt}]}
        user = {"role": "user", "content": [{"type": "text", "content": user_prompt}]}
        assistant = {"role": "assistant", "content": [{"type": "text", "content": assistant_prompt}]}
        new_datas.append({"messages":[system, user, assistant]})
    print(len(new_datas))
    save_jsonl(new_datas, out_file)

def generate_new_problem_dataset(in_file, out_file):
    datas = load_jsonl(in_file)
    system_prompt = "请根据以下问题创造一道类似的新问题。"
    random.seed(3407)
    random.shuffle(datas)
    random.shuffle(datas)
    random.shuffle(datas)
    random.shuffle(datas)
    random.shuffle(datas)
    new_datas = []
    random.shuffle(datas)
    for i in range(0, len(datas), 4):
        user_prompt = ""
        if i + 4 >= len(datas):
            break
        for idx, data in enumerate(datas[i:i+4]):
            user_prompt += f"问题{idx + 1}：{data['question']}\n"
        user_prompt += "新问题："
        new_datas.append({"question":user_prompt})
    random.shuffle(datas)
    for i in range(0, len(datas), 4):
        user_prompt = ""
        if i + 4 >= len(datas):
            break
        for idx, data in enumerate(datas[i:i+4]):
            user_prompt += f"问题{idx + 1}：{data['question']}\n"
        user_prompt += "新问题："
        new_datas.append({"question":user_prompt})
    random.shuffle(datas)
    for i in range(0, len(datas), 4):
        user_prompt = ""
        if i + 4 >= len(datas):
            break
        for idx, data in enumerate(datas[i:i+4]):
            user_prompt += f"问题{idx + 1}：{data['question']}\n"
        user_prompt += "新问题："
        new_datas.append({"question":user_prompt})
    random.shuffle(datas)
    for i in range(0, len(datas), 4):
        user_prompt = ""
        if i + 4 >= len(datas):
            break
        for idx, data in enumerate(datas[i:i+4]):
            user_prompt += f"问题{idx + 1}：{data['question']}\n"
        user_prompt += "新问题："
        new_datas.append({"question":user_prompt})
    random.shuffle(datas)
    for i in range(0, len(datas), 4):
        user_prompt = ""
        if i + 4 >= len(datas):
            break
        for idx, data in enumerate(datas[i:i+4]):
            user_prompt += f"问题{idx + 1}：{data['question']}\n"
        user_prompt += "新问题："
        new_datas.append({"question":user_prompt})
    print(len(new_datas))
    save_jsonl(new_datas, out_file)

if __name__ == "__main__":
    generate_new_problem_dataset("/mnt/cache/luzimu/datasets_ch/ape210k/outs/processed/train.jsonl", "/mnt/cache/luzimu/datasets_ch/ape210k/outs/create_new/infer_create_new.jsonl")
        