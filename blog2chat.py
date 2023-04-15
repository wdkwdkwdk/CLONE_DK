# 批量将文章转成可用于训练对话的数据集
# 需注意，这里需要配合 chatgpt 使用，因为众所周知的原因，我将调用chatgpt的脚本放在了海外，并做成了封装接口形式，供服务器调用，详细 prompt 见 blog_handle_readme.md 文件
# by: wdkwdkwdk
# Date: 2023-04-15


import os
import time

import requests
import json

from tqdm import tqdm


def read_csv_files(folder_path):
    """
    读取一个文件夹内所有的csv文件，返回转为纯文本的内容
    """
    texts = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            print("handle:"+filename)
            filepath = os.path.join(folder_path, filename)
            with open(filepath, encoding="utf-8") as f:
                text = f.read()
                text = text.replace("content", "")
                text = text.replace('"', "")
                texts.append(text)
    return "\n".join(texts)

def request_remote_url(text):
    """
    将文本内容每1000个字分段请求一个远程URL，并将返回的json加在一起
    """
    url = "https://service-jf3wigx2-1251731618.hk.apigw.tencentcs.com/release/blog2chat" # 部署好的远程接口，接口会调用chatgpt接口，
    headers = {"Content-Type": "application/json"}
    result = []
    for i in tqdm(range(0, len(text), 500)):
        data = {"text": text[i:i+500]}
        try:
            json_data = json.dumps(data)
            response = requests.post(url, headers=headers, data=json_data, timeout=50)
            json_result = json.loads(response.text)
            if json_result['data'] != None:
                print(json_result)
                result.append(json_result['data'])
                print(result)
            else:
                print("fail to json,record it ")
                fullcontent = json_result["full"]
                json_data2 = json.loads(fullcontent[fullcontent.find('['):])  # 找到第一个[开始解析json数据
                with open("fail_log", "w", encoding="utf-8") as f:
                    f.write(json_data2)
                    f.close()
        except Exception as e:
            print(e)
            print('Network error')
            time.sleep(5)
            continue

    return result

def write_json_to_file(json_str, output_path):
    """
    将json字符串写入文件
    """
    if os.path.exists(output_path):
        os.remove(output_path)  # 删除已存在的文件
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(json_str, f, ensure_ascii=False)

if __name__ == "__main__":
    input_folder = "blogs"
    output_file = "blog_output.json"
    text = read_csv_files(input_folder)
    result = request_remote_url(text)
    write_json_to_file(result, output_file)
