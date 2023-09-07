import json


if __name__ == "__main__":
    total_num = 0
    with open("/mnt/cache/luzimu/datasets_ch/ape210k/outs/train_code/train_out-0804-2314-mj-out-07250113-ape_input_202307191357.jsonl", "r") as f:
        with open("/mnt/cache/luzimu/datasets_ch/ape210k/outs/train_code/no_extract_out-0804-2314-mj-out-07250113-ape_input_202307191357.jsonl", "w") as f_out:
            for line in f:
                total_num += 1
                data = json.loads(line)
                data.pop("extra", None)
                f_out.write(json.dumps(data) + "\n")
    print(total_num)