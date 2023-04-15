# lora模型融合
# by: sean@6pen
# Date: 2023-04-15

import torch
import json


model_chat = 'chatglm-lora.pt' #融合模型1
model_chat_new = 'checkpoint-29000/chatglm-lora.pt' #融合模型2

l1 = torch.load(model_chat)
l2 = torch.load(model_chat_new)

alpha_1 = 0.7 #权重1
alpha_2 = 0.3 #权重2
print(l1.keys())
out_list = {}
for (k1, v1), (k2, v2) in zip(l1.items(), l2.items()):
    v1.data = alpha_1 * v1.data + alpha_2 * v2.data

    out_list[k1] =  v1

output_path = 'test_merge_lora_merge_blog_more_7-3.pt' #保存
torch.save(out_list, output_path)
