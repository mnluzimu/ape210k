import re
import json
import os

from tqdm import tqdm
from multiprocessing import Pool,RLock
from huggingface_hub import InferenceClient
import fire
from jupyter_client.manager import start_new_kernel
import time
from argparse import ArgumentParser
def timestamp() -> str:
    nowtime = time.strftime('-%Y%m%d-%H%M', time.localtime(time.time()))
    print(nowtime)  
    return nowtime  

def save_jsonl(data: list, path: str, mode='w', add_timestamp=True, verbose=True) -> None:
    if add_timestamp:
        file_name = f"{path.replace('.jsonl','')}{timestamp()}.jsonl"
    else:
        file_name = path
    with open(file_name, mode, encoding='utf-8') as f:
        if verbose:
            for line in tqdm(data, desc='save'):
                f.write(json.dumps(line, ensure_ascii=False) + '\n')
        else:
            for line in data:
                f.write(json.dumps(line, ensure_ascii=False) + '\n')


def load_jsonl(path: str):
    with open(path, "r", encoding='utf-8') as fh:
        return [json.loads(line) for line in fh.readlines() if line]
    

class JupyterNotebookKernel(object):

    lock = RLock()

    def __init__(self):
        JupyterNotebookKernel.lock.acquire()
        self.manager, self.client = start_new_kernel(kernel_name='python')
        JupyterNotebookKernel.lock.release()
                

    
    def shutdown(self):
        if self.manager:
            self.manager.shutdown_kernel()
            self.manager = None
            self.client = None


    def handle_iopub_msg(self):
        result = ''

        while msg := self.client.get_iopub_msg(timeout=10):
            
            if msg['msg_type'] == 'status' and msg['content']['execution_state'] == 'idle':
                break

            if msg['msg_type'] == 'stream':
                result += msg['content']['text']
            
            if msg['msg_type'] == 'execute_result':
                result += msg['content']['data']['text/plain']
            
            if msg['msg_type'] == 'error':
                if isinstance(msg['content']['traceback'], list):
                    msg['content']['traceback'] = ' '.join(msg['content']['traceback'])

                error = re.sub(
                    '\x1B\\[([0-9]{1,2}(;[0-9]{1,2})?)?[mGK]',
                    '',
                    msg['content']['traceback'],
                )

                result += error
        
        if len(result) == 0:
            result = '<empty_execution>'

        return result.strip()

    def run_code(self, code):
        try:
            self.client.execute(code, allow_stdin=False, reply=True, timeout=6)
            return self.handle_iopub_msg()
        except Exception as e:
            return f'{"-"*75} {str(e)}{" "*32}Traceback (most recent call last) '


class API:

    def __init__(self, port='8001', ip='10.119.29.124'):
        self.client = InferenceClient(model=f'http://{ip}:{port}')

    def get_result(self, inputs, parameters=None):

        local_parameters = dict(max_new_tokens=512, details=True, decoder_input_details=True)

        if parameters is not None:
            local_parameters.update(parameters)
        
        try:
            result = self.client.text_generation(prompt=inputs, **local_parameters)

            text = result.generated_text
            # print(type(result.details))
            if result.details.tokens[0].special and not text.startswith(result.details.tokens[0].text.strip()):
                text = result.details.tokens[0].text.strip() + text

            if result.details.tokens[-1].special and not text.endswith(result.details.tokens[-1].text.strip()):
                text = text + result.details.tokens[-1].text.strip()

            return text
        except:
            import traceback
            traceback.print_exc()
            print(inputs) 
            return None
        

def code_generation(query):
    query = query.replace("请回答以下问题并把答案放在\\boxed{}里：", '').replace("Solve the problem and put your answer in '\\boxed{}'. \n", "")
    system = ""
    # system = "Solve the problem below, and you must put your answer in one and only one '\\boxed{}'.\n\nTo solve the problem using code step by step, even in every sub-step."
    prompt = f'<|system|><|text|>{system}<|endofblock|><|endofmessage|><|user|><|text|>{query}<|endofblock|><|endofmessage|><|assistant|>'

    messages = [
        {'role': 'system', 'content': system},
        {'role': 'user', 'content': query}
    ]

    jupyter = JupyterNotebookKernel()

    parameters=dict(
        do_sample=False,
        max_new_tokens=512,
        stop_sequences=['<|endofmessage|>', '<|endofblock|>'], 
        truncate=3072,
        details=True, 
        decoder_input_details=True
    )
    code = ''
    for _ in range(16):
        result = api.get_result(prompt, parameters=parameters)

        if result is None:
            messages.append({'role': 'exceed_max_length/return_first_code', 'content': code})
            jupyter.shutdown()
            return messages

        prompt += result 
        results = result.split('<|')
        for id, sub_result in enumerate(results):
            if id > 0:
                sub_result = '<|' + sub_result
            if len(sub_result.replace('<|assistant|>','').replace('<|code|>','').replace('<|text|>','').replace('<|endofblock|>','')) == 0:
                continue
            # print(sub_result)
            if sub_result.startswith('<|code|>'):
                code = sub_result.replace('<|code|>', '').replace('<|endofblock|>', '')
                messages.append({'role': 'code', 'content': code})
                
                execution = jupyter.run_code(code)

                prompt += f"<|execution|>{execution}<|endofblock|>"
                messages.append({'role': 'execution', 'content': execution})
            elif not sub_result.endswith('<|endofmessage|>'):
                messages.append({'role': 'text', 'content': sub_result.replace('<|text|>', '').replace('<|endofblock|>', '')})
        if  result.endswith('<|endofmessage|>') or result.endswith('<|endoftext|>'):
            break
    
    jupyter.shutdown()
    return messages

def process_full(data, key='question'):

    query = data[key]

    debug_result = code_generation(query)

    data['debug_result'] = debug_result

    return data


if __name__ == '__main__':
    NP = {
        'wk': '20031',
        'swk': '20021',
        'lzm': '20041',
        'rhx': '20001'
    }
    parser = ArgumentParser(description="A simple argument parser")
    parser.add_argument("ch", type=str, help="checkpoint_number")

    args = parser.parse_args()
    print(args.ch)

    ip = {
        "0": "",
        "1": "",
        "2": "",
        "3": "10.119.18.26",
        "4": "10.119.23.239",
        "5": "10.119.31.234",
        "6": "10.119.23.73",
        "7": "10.119.24.221",
        "8": "10.119.26.251",
        "9": "10.119.31.235",
        "10": "10.119.23.74",
        "11": "10.119.24.222",
        "12": "10.119.22.91"
    }
    
    api = API(port="8001", ip=ip[args.ch])

    input_path = f'/mnt/cache/luzimu/datasets_ch/ape210k/outs/train_to_be_run/{args.ch}.jsonl'
    output_path = f'/mnt/cache/luzimu/datasets_ch/ape210k/outs/train_run_results/{args.ch}_result.jsonl'

    # output_path = f'/mnt/cache/wangke/code_generation/outs/debug/{name}/{name}_test_result.jsonl'
    if not os.path.exists("/".join(output_path.split("/")[:-1])):
        os.makedirs("/".join(output_path.split("/")[:-1]))
    
    try:
        all = load_jsonl(output_path)
    except FileNotFoundError:
        all = []

    BEGIN = len(all)

    OVER_WRITE = True
    humaneval = load_jsonl(input_path)
    END = len(humaneval)
    outs = []


    counter = BEGIN
    while counter < END:
        pool = Pool(16)
        try:
            results = pool.imap(process_full, humaneval[BEGIN:END])
            for d in tqdm(results, total=len(humaneval[BEGIN:END])):
                d['completion'] = d['debug_result'][-1]['content']
                outs.append(d)
                all.append(d)
                counter += 1
                if counter % 10 == 0 or counter == END:
                    if counter <= 10 and OVER_WRITE:
                        save_jsonl(outs, output_path,mode='w', add_timestamp=False, verbose=False)
                    else:
                        save_jsonl(outs, output_path,mode='a', add_timestamp=False, verbose=False)
                    outs = []
                    BEGIN = counter
        except Exception as e:
            print(f'<|{str(e)}|>')
            pool.terminate()  # 立即终止所有子进程
            continue  # 重新开始while循环
        finally:
            pool.close()  # 关闭pool，防止新的任务提交到pool
            pool.join()   # 等待子进程结束

    
    print('Total: ', counter)

    '''  

    for d in tqdm(humaneval[10:20]):
        d = process_full(d)
        
    '''


    save_jsonl(all, output_path, add_timestamp=True)


