if __name__ == "__main__":
    with open("/mnt/cache/luzimu/datasets_ch/ape210k/outs/train_code/train_out-0804-2314-mj-out-07250113-ape_input_202307191357.jsonl", "r", encoding="utf-8") as f_in:
        with open("/mnt/cache/luzimu/datasets_ch/ape210k/outs/train_code/100.jsonl", "w", encoding="utf-8") as f_out:
            for _ in range(100):
                f_out.write(f_in.readline())
