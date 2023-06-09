# CLONE_DK


📃 相关文章：[我用我的微信聊天记录和 280 篇博客文章，做了我自己的数字克隆AI](https://greatdk.com/1908.html)

💬 在线和我的克隆聊天：[AI DK](https://ai.greatdk.com)


在这个仓库中，我将提供更为详细的技术细节和代码，包括：

* chatglm-6b finetune 脚本
* 微信聊天记录文本转换脚本
* 文章转换成可用于训练的数据集脚本
* 模型权重融合脚本
* 通过 chatGPT 将文章数据转换成```json```问答对的 prompt
* 前端部署方案
* 封装 chatglm 为 web api 的脚本


## web 部署

demo 参考：https://ai.greatdk.com/

如果你已经完成了模型的部署(web.py)，可以直接参考使用 https://github.com/wdkwdkwdk/MoeChat 这个项目部署成一个线上聊天的 demo

推荐使用 vercel 直接部署，贼方便：


### 需要注意的是：

完整的训练过程十分繁琐，需要具备一定的代码能力，我并没有对训练方式做任何创新，如果你对训练过程有问题或感兴趣，推荐先了解这些微调训练的项目：
* [https://github.com/yuanzhoulvpi2017/zero_nlp](https://github.com/yuanzhoulvpi2017/zero_nlp)
* [https://github.com/ssbuild/chatglm_finetuning](https://github.com/ssbuild/chatglm_finetuning)


因为数据集和训练方式，训练时间，以及运气原因，无法保证训练结果会令人满意，我个人的经验是：
* chatGLM-6B 中文的效果很好，但是似乎被训练的比较过，如果想让训练完的模型明显区别于原始版本，可能需要 5 万条以上的数据
* 数据更多的话，调低学习率，增加 epoch 


同时在文章下有很多疑惑，我做一些说明：
基于我的微信聊天记录训练模型，并不会泄露隐私，有很多人问到了我的身份证号或者住址，此外还有几千人问我女朋友的名字，我可以负责任的说，得到的回答都是瞎编的。数据集中并不会有很多类似于：
```
你的身份证号是多少？
XXXXXX
```
这样的对话，即便有极少量，在 10万条的总数里占比也非常低，这不足以让模型将其当作```知识```记忆，更多的，模型只是通过这些聊天问答，学习某些规律，可以理解为学习说话的方式，语气和某些思维(谁知道呢)
