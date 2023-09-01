import json
import os

def generate_Llama_train(in_files, out_file):
    new_datas = []
    for in_file in in_files:
        datas = load_json(in_file)

        for data in datas:
            user_prompt = data["question"]
            system = {"role":"system", "content":[{"type":"text", "content":""}]}
            user = {"role":"user", "content":[{"type":"text", "content":user_prompt}]}
            assistant_content = []
            for block in ...
            answer = data["answer"]
            equation = data["equation"]
            id = data["id"]
            extra = {"id":id, "answer":answer, "equation":equation}

            new_data = {"messages":[system, user], "extra":extra}
            new_datas.append(new_data)

    save_jsonl(new_datas, out_file)
    
if __name__ == "__main__":
    