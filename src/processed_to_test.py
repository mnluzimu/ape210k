import json
import os


def save_jsonl(datas, file_name):
    with open(file_name, "w", encoding="utf-8") as f:
        for data in datas:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")

def load_json(in_file):
    with open(in_file, "r", encoding="utf-8") as f:
        datas = [json.loads(line) for line in f]
    return datas

def generate_GPT_test(in_files, out_file):
    new_datas = []
    for in_file in in_files:
        datas = load_json(in_file)

        for data in datas:
            prompt = "请回答以下问题并把答案放在\\boxed{}里：" + f"{data['question']}"
            answer = data["answer"]
            equation = data["equation"]
            id = data["id"]

            new_data = {"text":[{"content":prompt}], "first_text_length":len(prompt), "extra":{"id":id, "answer":answer, "equation":equation}}
            new_datas.append(new_data)

    save_jsonl(new_datas, out_file)

def generate_Llama_test(in_files, out_file):
    new_datas = []
    for in_file in in_files:
        datas = load_json(in_file)

        for data in datas:
            system = {"role":"system", "content":[{"type":"text", "content":""}]}
            user = {"role":"user", "content":[{"type":"text", "content":"请回答以下问题并把答案放在\\boxed{}里：" + f"{data['question']}"}]}
            answer = data["answer"]
            equation = data["equation"]
            id = data["id"]
            extra = {"id":id, "answer":answer, "equation":equation}

            new_data = {"messages":[system, user], "extra":extra}
            new_datas.append(new_data)

    save_jsonl(new_datas, out_file)

def generate_gsm8k_rft_test(in_files, out_file):
    new_datas = []
    for in_file in in_files:
        datas = load_json(in_file)

        for data in datas:
            question = "请回答以下问题并把答案放在\\boxed{}里：" + f"{data['question']}"
            answer = data["answer"]
            equation = data["equation"]
            id = data["id"]
            extra = {"id":id, "answer":answer, "equation":equation}

            new_data = {"question":question, "extra":extra}
            new_datas.append(new_data)

    save_jsonl(new_datas, out_file)

if __name__ == "__main__":
    in_files = [
        "/mnt/cache/luzimu/datasets_ch/ape210k/outs/processed/test.jsonl",
    ]
    out_file = "/mnt/cache/luzimu/datasets_ch/ape210k/outs/test/gpt_test.jsonl"

    generate_GPT_test(in_files, out_file)

    in_files = [
        "/mnt/cache/luzimu/datasets_ch/ape210k/outs/processed/test.jsonl",
    ]
    out_file = "/mnt/cache/luzimu/datasets_ch/ape210k/outs/test/Llama_test.jsonl"

    generate_Llama_test(in_files, out_file)

    in_files = [
        "/mnt/cache/luzimu/datasets_ch/ape210k/outs/processed/test.jsonl",
    ]
    out_file = "/mnt/cache/luzimu/datasets_ch/ape210k/outs/test/gsm8k_rft_test_boxed.jsonl"

    generate_gsm8k_rft_test(in_files, out_file)