import json
from tqdm import tqdm
import re

def save_jsonl(datas, file_name):
    with open(file_name, "w", encoding="utf-8") as f:
        for data in datas:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")

def load_json(in_file):
    with open(in_file, "r", encoding="utf-8") as f:
        datas = [json.loads(line) for line in f]
    return datas

def find_last_number(text):
    # The regex pattern to match any number (integer or floating-point)
    pattern = r'\d+(?:\.\d+)?'
    
    # Using findall to get all occurrences of numbers in the string
    all_numbers = re.findall(pattern, text)
    
    # If there are no numbers in the string, return None
    if not all_numbers:
        return None
    
    # Return the last number found in the string
    return all_numbers[-1]

def find_all_numbers(text):
    # The regex pattern to match any number (integer or floating-point)
    pattern = r'\d+(?:\.\d+)?'
    
    # Using findall to get all occurrences of numbers in the string
    all_numbers = re.findall(pattern, text)
    
    # If there are no numbers in the string, return None
    if not all_numbers:
        return None
    
    # Return the last number found in the string
    return all_numbers

def check(gt_answer, all_numbers):
    for number in all_numbers:
        if gt_answer == number:
            return True

    return False

def process_gpt_code_to_train(in_file, out_file):
    datas = load_json(in_file)
    error_num = 0
    new_datas = []
    error_datas = []
    wrong_datas = []
    for data in tqdm(datas):
        try:
            all_answers = data["all_answers"][0]["contents"]
            if len(all_answers) < 3:
                error_num += 1
                continue
            system = {"role": "system", "content": [{"type":"text", "content":""}]}
            user = {"role": "user", "content":[{"type":"text", "content":all_answers[1]["message"]["content"]["parts"][0]}]}
            assistant_contents = []
            for entry in all_answers[2:]:
                message = entry["message"]["content"]
                if message["content_type"] == "text":
                    assistant_contents.append({"type":"text", "content":message["parts"][0]})
                elif message["content_type"] == "code":
                    assistant_contents.append({"type":"code", "content":message["text"]})
                elif message["content_type"] == "execution_output":
                    assistant_contents.append({"type":"execution", "content":message["text"]})
            
            if len(assistant_contents) == 0:
                error_num += 1
                continue
            last_block = assistant_contents[-1]["content"]
            model_answers = find_all_numbers(last_block)
            model_answer = find_last_number(last_block)
            gt_answer = data["extra"]["answer"]
            assistant_contents.append({"type":"text", "content":data["extra"]["answer"]})
            assistant = {"role": "assistant", "content": assistant_contents}
            new_data = {"messages":[system, user, assistant], "extra":{"last_block":last_block,"model_answer": model_answer, "answer":gt_answer}}
            if not check(gt_answer, model_answers):
                wrong_datas.append(data)
            else:
                new_datas.append(new_data)
        except:
            error_datas.append(data)
    save_jsonl(new_datas, out_file)
    save_jsonl(error_datas, out_file[:-6] + "_error.jsonl")
    save_jsonl(wrong_datas, out_file[:-6] + "_wrong.jsonl")
    save_jsonl(new_datas[:100], out_file[:-6] + "_100.jsonl")
    print(f"error_num: {len(error_datas)}")
    print(f"ok_num: {len(new_datas)}")
    print(f"wrong_num: {len(wrong_datas)}")
    
if __name__ == "__main__":
    process_gpt_code_to_train("/mnt/cache/luzimu/datasets_ch/ape210k/outs/train_code/train_out-0804-2314-mj-out-07250113-ape_input_202307191357_wrong.jsonl",
                              "/mnt/cache/luzimu/datasets_ch/ape210k/outs/train_code/wrong_to_correct.jsonl")