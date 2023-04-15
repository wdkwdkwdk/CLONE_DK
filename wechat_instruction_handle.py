# 微信原始聊天记录转成json问答格式
# by: wdkwdkwdk
# Date: 2023-04-15
# Description: 用于将导出好的txt格式的聊天记录，转换成可以用于训练的json数据


import os
import json
from tqdm import tqdm

data_dir = "wx_chat"  # 设定需要遍历的文件夹路径

output = []  # 存放遍历过程中生成的json对象的列表

for file_name in tqdm(os.listdir(data_dir), desc="Processing files"):  # tqdm展示遍历进度
    if file_name.endswith(".txt"):  # 只处理txt文件
        with open(os.path.join(data_dir, file_name), "r", encoding="utf-8") as f:
            lines = f.readlines()

            last_speaker = None  # 初始化发言人
            last_message = None  # 初始化上一条发言

            for line in lines:
                if ":" not in line:  # 如果没有":",跳过该行
                    continue
                if len(line.split(' (')) < 2 or len(line.split('):')) < 2:
                    # 格式不符合要求，跳过该行
                    continue
                parts = line.strip().split(":", maxsplit=1)  # 只进行一次分割，并将剩余部分合并成一个字符串
                if len(parts) != 2:  # 如果分割后的部分多于2个，说明该行无法处理，跳过
                    continue
                try:
                    speaker, time_and_chat = line.strip().split(' (', 1)
                    time, chat = time_and_chat.split('):', 1)
                except Exception as e:
                    print(e)
                    print(line)
                if speaker == "圣经上的子弹":  # 检查是否为小王发言，这里写要提取的人的微信昵称
                    if "你的密码" in chat or "你的关键信息" in chat  or "[图片]" in chat or "[表情]" in chat or last_message is "[图片]":
                        continue
                    if last_speaker is not None:  # 判断是否存在上一条发言
                        output.append({  # 存入json
                            "instruction": last_message,
                            "input": "",
                            "output": chat
                        })
                last_speaker = speaker  # 更新发言人
                last_message = chat  # 更新上一条发言

with open("outputall_art_qun.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=4)  # 将结果写入json文件

print("总数：")
print(len(output))