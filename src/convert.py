import json


if __name__ == "__main__":
    total_num = 0
    with open("/mnt/cache/luzimu/datasets_ch/ape210k/outs/train_code/train_out-0804-2314-mj-out-07250113-ape_input_202307191357_wrong.jsonl", "r") as f:
        with open("/mnt/cache/luzimu/datasets_ch/ape210k/outs/train_code/gpy_code_wrong_problem_and_gt.jsonl", "w") as f_out:
            for line in f:
                total_num += 1
                data = json.loads(line)
                answer = data["extra"]["answer"]
                solution = data["extra"]["solution"]
                problem = data["text"][0]["content"]
                new_data = {"problem": problem, "answer": answer, "solution": solution}
                f_out.write(json.dumps(new_data, ensure_ascii=False) + "\n")
    print(total_num)