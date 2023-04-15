# 将文本模型部署成 Web API
# by: sean@6pen
# Date: 2023-04-15


from flask import Flask, jsonify, request
from transformers import AutoTokenizer
from thuglm.modeling_chatglm import ChatGLMForConditionalGeneration
import torch
from peft import get_peft_model, LoraConfig, TaskType
import threading

model_id = 'chatglm-6b'
model = ChatGLMForConditionalGeneration.from_pretrained(model_id).half().cuda()

lock = threading.Lock()

peft_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    inference_mode=False, r=8, lora_alpha=32, lora_dropout=0.1,
    target_modules=['query_key_value',],
)
model = get_peft_model(model, peft_config)



# 在这里加载lora模型，注意修改chekpoint
peft_path = "test_merge_lora_chat_chat_new_8-2.pt"
model.load_state_dict(torch.load(peft_path), strict=False)
model.eval()




tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)



app = Flask(__name__)

@app.route("/status", methods=['GET'])
def status_endpoint():
    result = {
        "info": "ok",
        "memory": "123"
    }
    return jsonify(result)



@app.route("/chat", methods=['POST'])
def chat_endpoint():
    # 获取请求中的参数
    global history
    data = request.get_json()
    text = data.get("text")
    history_send = data.get("history")
    if history_send is not None:
        history = history_send
    # 进行聊天
    with lock:
        with torch.autocast("cuda"):
            res, history = model.chat(tokenizer=tokenizer, query=text, history=history ,max_length=256, temperature=data.get("temperature"), do_sample=data.get("do_sample"), top_p = data.get("top_p"), num_beams = data.get("num_beams"))
            # app.logger.info(data)
            # app.logger.info(res)
            print(data,flush=True)
            print(res,flush=True)
        # 返回结果
        result = {
            "response": res,
            "history": history
        }
    return jsonify(result)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9527)