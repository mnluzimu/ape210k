import json
import os
import re
from latex2sympy2 import latex2sympy
from tqdm import tqdm

def delete_extra_zero(n):
    '''删除小数点后多余的0'''
    try:
        n=float(n)
    except:
        print("None {}".format(n))
        return n
    if isinstance(n, int):
        return str(n)
    if isinstance(n, float):
        n = str(n).rstrip('0')  # 删除小数点后多余的0
        n = int(n.rstrip('.')) if n.endswith('.') else float(n)  # 只剩小数点直接转int，否则转回float
        n=str(n)
        return n


def _fix_fracs(string):
    substrs = string.split("\\frac")
    new_str = substrs[0]
    if len(substrs) > 1:
        substrs = substrs[1:]
        for substr in substrs:
            new_str += "\\frac"
            if len(substr) > 0 and substr[0] == "{":
                new_str += substr
            else:
                try:
                    assert len(substr) >= 2
                except:
                    return string
                a = substr[0]
                b = substr[1]
                if b != "{":
                    if len(substr) > 2:
                        post_substr = substr[2:]
                        new_str += "{" + a + "}{" + b + "}" + post_substr
                    else:
                        new_str += "{" + a + "}{" + b + "}"
                else:
                    if len(substr) > 2:
                        post_substr = substr[2:]
                        new_str += "{" + a + "}" + b + post_substr
                    else:
                        new_str += "{" + a + "}" + b
    string = new_str
    return string


def _fix_a_slash_b(string):
    if len(string.split("/")) != 2:
        return string
    a = string.split("/")[0]
    b = string.split("/")[1]
    try:
        a = int(a)
        b = int(b)
        assert string == "{}/{}".format(a, b)
        new_string = "\\frac{" + str(a) + "}{" + str(b) + "}"
        return new_string
    except:
        return string


def _remove_right_units(string):
    # "\\text{ " only ever occurs (at least in the val set) when describing units
    splits = string.split("\\text{ ")
    # assert len(splits) == 2
    return splits[-1]


def _fix_sqrt(string):
    if "\\sqrt" not in string:
        return string
    splits = string.split("\\sqrt")
    new_string = splits[0]
    for split in splits[1:]:
        if len(split) > 0 and split[0] != "{":
            a = split[0]
            new_substr = "\\sqrt{" + a + "}" + split[1:]
        else:
            new_substr = "\\sqrt" + split
        new_string += new_substr
    return new_string

    
def _strip_string(string):
    # linebreaks
    string = string.replace("\n", "")
    # print(string)

    # remove inverse spaces
    string = string.replace("\\!", "")
    # print(string)

    # replace \\ with \
    string = string.replace("\\\\", "\\")
    # print(string)

    # replace tfrac and dfrac with frac
    string = string.replace("tfrac", "frac")
    string = string.replace("dfrac", "frac")
    # print(string)

    # remove \left and \right
    string = string.replace("\\left", "")
    string = string.replace("\\right", "")
    # print(string)

    # Remove circ (degrees)
    string = string.replace("^{\\circ}", "")
    string = string.replace("^\\circ", "")

    # remove dollar signs
    string = string.replace("\\$", "")
    string = string.replace("$", "")

    # remove units (on the right)
    string = _remove_right_units(string)

    # remove percentage
    string = string.replace("\\%", "")
    string = string.replace("\%", "")

    # " 0." equivalent to " ." and "{0." equivalent to "{." Alternatively, add "0" if "." is the start of the string
    string = string.replace(" .", " 0.")
    string = string.replace("{.", "{0.")
    # if empty, return empty string
    if len(string) == 0:
        return string
    if string[0] == ".":
        string = "0" + string

    # to consider: get rid of e.g. "k = " or "q = " at beginning
    if len(string.split("=")) == 2:
        string = string.split("=")[-1]
    if len(string.split("\\approx")) == 2:
        string = string.split("\\approx")[-1]

    # fix sqrt3 --> sqrt{3}
    if 'sqrt' in string:
        string = _fix_sqrt(string)

    # remove spaces
    string = string.replace(" ", "")

    # \frac1b or \frac12 --> \frac{1}{b} and \frac{1}{2}, etc. Even works with \frac1{72} (but not \frac{72}1). Also does a/b --> \\frac{a}{b}
    if 'sqrt' in string:
        string = _fix_fracs(string)

    # manually change 0.5 --> \frac{1}{2}
    if string == "0.5":
        string = "\\frac{1}{2}"

    # NOTE: X/Y changed to \frac{X}{Y} in dataset, but in simple cases fix in case the model output is X/Y
    string = _fix_a_slash_b(string)

    return string

    
def find_math_answer(s:str, type="gpt"):
    s = s.lower()
    if '{}' in s:
        s = s.replace('{}','')
    try:
        pattern = re.compile('oxed{(.*)}',flags=re.S)
        ans = pattern.findall(s)[-1]
    except:
        if type == "gpt":
            ans = ""
        else:
            ans = s
 
    if ans.find('}') != -1 and(ans.find('{') ==-1 or  ans.find('}') < ans.find('{')):
        ans=ans.split('}')[0]
    # remove
    ans = ans.split('=')[-1]
    ans = ans.split('\\approx')[-1]
    ans = ans.replace(" ", "")
    ans = ans.replace("\\,", "")
    ans = ans.replace('∞','\\infty').replace("+\infty", "\infty")
    ans = ans.replace("\\\\", "\\")
    ans = ans.replace("\n", "")
    ans = ans.replace('\\text', '').replace('\\mbox', '')
    ans = ans.replace('bmatrix', 'pmatrix')
    ans = ans.replace("\\left", "").replace('\\right', '')
    ans = ans.replace("^{\\circ}", "").replace("^\\circ", "")
    ans = ans.replace("{m}^3", "").replace("m^3", "")
    ans = ans.replace("{units}", "").replace("units", "")
    ans = ans.replace("{km}", "").replace("km", "")
    return _strip_string(ans)


def eval_tuple(s):
    """
    (a,b,c,...)
    """
    sl = s[1:-1].split(',')
    try :
        if s[0] == '(' and s[-1] == ')' and len(sl) > 1:
            s = ','.join([str(round(eval(str(latex2sympy(sub))),2)) if 'infty' not in sub and sub not in ['a', '-a'] else sub for sub in sl])
            return f"({s})"
    except:
        return s
    return s


def is_equal(asw:str, gt_asw:str) -> bool:
    """
    Judge if asw is equivalent to gt_asw.
    """
    asw = find_math_answer(asw, "gt")
    gt_asw = find_math_answer(gt_asw, "gt")
    asw = eval_tuple(asw)
    gt_asw = eval_tuple(gt_asw)
    if gt_asw == "" or asw == "":
        return False
    if gt_asw in asw or asw in gt_asw:
        return True
    else:
        try:
            if ',' in gt_asw:
                if set(gt_asw.split(',')) == set(asw.split(',')):
                    return True
            if str(round(eval(str(latex2sympy(gt_asw))),2)) == str(round(eval(str(latex2sympy(asw))),2)):
                return True
            
            else:
                return False
        except:
            return False


def compute_accuracy_ape_gpt(in_file, out_path):
    with open(in_file, "r", encoding="utf-8") as f:
        datas = [json.loads(line) for line in f]

    correct_ans = []
    wrong_ans = []
    no_ans = []
    for data in datas:
        try:
            solution = ""
            contents = data["all_answers"][0]["contents"]
            for e in contents[2:]:
                content = e["message"]["content"]
                type = content["content_type"]
                if type == "text":
                    solution += content["parts"][0]
                elif type == "code":
                    solution += "<|code|>" + content["text"] + "<|code|>"
                elif type == "execution_output":
                    solution += "<|execution|>" + content["text"] + "<|execution|>"
            model_ans = find_math_answer(solution)
            gt_ans = data["extra"]["answer"]
            data["model_answer"] = model_ans
            data["gt_answer"] = gt_ans

            if is_equal(model_ans, gt_ans):
                correct_ans.append(data)
            else:
                wrong_ans.append(data)
        except:
            no_ans.append(data)

    with open(os.path.join(out_path, "correct.jsonl"), "w") as f:
        for data in correct_ans:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")
    with open(os.path.join(out_path, "wrong.jsonl"), "w") as f:
        for data in wrong_ans:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")
    with open(os.path.join(out_path, "none.jsonl"), "w") as f:
        for data in no_ans:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")
    print(f"correct_num: {len(correct_ans)}")
    print(f"wrong_num: {len(wrong_ans)}")
    print(f"none_num: {len(no_ans)}")
    print(f"acc: {100 * len(correct_ans) / len(datas)}")

def compute_accuracy_ape_Llama(in_file, out_path):
    with open(in_file, "r", encoding="utf-8") as f:
        datas = [json.loads(line) for line in f]

    correct_ans = []
    wrong_ans = []
    no_ans = []
    for data in datas:
        try:
            model_solution = data["completion"]
            strip_strings = ["<|endoftext|>", "<|system|>", "<|text|>", "<|endofblock|>", "<|endofmessage|>", "<|user|>", "<|assistant|>"]
            for strip_string in strip_strings:
                model_solution = model_solution.replace(strip_string, "")
            model_ans = find_math_answer(model_solution)
            gt_ans = data["extra"]["answer"]
            data["model_answer"] = model_ans
            data["gt_answer"] = gt_ans
            data["completion"] = model_solution
            if is_equal(model_ans, gt_ans):
                correct_ans.append(data)
            else:
                wrong_ans.append(data)
        except:
            no_ans.append(data)

    with open(os.path.join(out_path, "correct.jsonl"), "w") as f:
        for data in correct_ans:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")
    with open(os.path.join(out_path, "wrong.jsonl"), "w") as f:
        for data in wrong_ans:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")
    with open(os.path.join(out_path, "none.jsonl"), "w") as f:
        for data in no_ans:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")
    print(f"correct_num: {len(correct_ans)}")
    print(f"wrong_num: {len(wrong_ans)}")
    print(f"none_num: {len(no_ans)}")
    print(f"acc: {100 * len(correct_ans) / len(datas)}")
    

if __name__ == "__main__":
    # compute_accuracy("/mnt/cache/luzimu/code_generation-master/outs/Llama-2-7b-hf-math-2023-08-27-09:58/MATH_test_result.jsonl", "/mnt/cache/luzimu/code_generation-master/outs/Llama-2-7b-hf-math-2023-08-27-09:58/MATH_results", "/mnt/cache/luzimu/gsm8k-rft-llama7b-u13b_evaluation/MATH_test_orig.jsonl")

    # compute_accuracy_ceval_gpt("/home/SENSETIME/luzimu/Documents/datasets_ch/ape210k/outs/results/gpt_3_ape210k_test_result/out.jsonl",
    #                        "/home/SENSETIME/luzimu/Documents/datasets_ch/ape210k/outs/results/gpt_3_ape210k_test_result")
    compute_accuracy_ape_Llama("/mnt/cache/luzimu/datasets_ch/ape210k/outs/results/sensecode_200.jsonl", "/mnt/cache/luzimu/datasets_ch/ape210k/outs/results/sensecode_1w_200")
