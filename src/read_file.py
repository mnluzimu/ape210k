import json
import random

def save_jsonl(datas, file_name):
    with open(file_name, "w", encoding="utf-8") as f:
        for data in datas:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")

def load_jsonl(in_file):
    with open(in_file, "r", encoding="utf-8") as f:
        datas = [json.loads(line) for line in f]
    return datas


if __name__ == "__main__":
    # total_num = 0
    # with open("/mnt/cache/luzimu/datasets_ch/ape210k/outs/multi_run_results/Llama2-70b-ape-gsm8k-resume-142315-2023-10-02-23:00/vote0/0_result.jsonl", "r") as f:
    #     with open("/mnt/cache/luzimu/datasets_ch/ape210k/outs/multi_run_results/Llama2-70b-ape-gsm8k-resume-142315-2023-10-02-23:00/vote0/0_result100.jsonl", "w") as f_out:
    #         for line in f:
    #             total_num += 1
    #             if total_num <= 100:
    #                 f_out.write(line)
    # print(total_num)

    in_file = "/mnt/cache/luzimu/datasets_ch/ape210k/outs/multi_run_results/Llama2-70b-ape-gsm8k-resume-142315-2023-10-02-23:00/vote0/0_result.jsonl"
    out_file = "/mnt/cache/luzimu/datasets_ch/ape210k/outs/multi_run_results/Llama2-70b-ape-gsm8k-resume-142315-2023-10-02-23:00/vote0/0_result100.jsonl"

    random.seed(3407)
    
    datas = load_jsonl(in_file)
    random.shuffle(datas)

    print(len(datas))
    save_jsonl(datas[:100], out_file)
