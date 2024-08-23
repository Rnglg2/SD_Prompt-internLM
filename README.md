## 项目规划：Stable Diffusion提示词助手

### 项目简介
本项目旨在为用户生成高质量的Stable Diffusion提示词。用户输入自然语言描述，通过大模型转换为适合Stable Diffusion的提示词，并使用XTuner对模型进行微调，以提升生成效果。主要功能包括：
## SD提示词助手模型地址-https://huggingface.co/Rnglg2/internLM2-SD_PROMPT
1. **自然语言到提示词转换**：利用书生大模型将用户输入的自然语言转换为Stable Diffusion的提示词。
2. **模型微调**：使用XTuner工具对模型进行QLoRA或全量参数微调，提升生成效果。
# 使用LMDeploy
首先 下载推理所用的模型 https://huggingface.co/Rnglg2/internLM2-SD_PROMPT
将模型文件夹重命名为internlm2-xxxxxx
## 安装依赖
```bash
#安装LMDepoly  
pip install lmdeploy
#安装其他依赖
pip install streamlit openai requests
```
## 运行
```bash
CUDA_VISIBLE_DEVICES=0 lmdeploy serve api_server ($model-path) --server-port 23333 --api-keys internlm2
streamlit run chat_ui.py
```
### 随后在webui上进行参数的调整即可
**你需要部署一个Stable diffusion Webui 否则将无法使用生图功能**

# 仅使用推理ui
## 安装依赖
```bash
pip install transformers huggingface_hub streamlit torch
```
## 运行步骤
1. 将脚本中`model_name_or_path`修改为下载完成的模型路径
2. 运行以下命令启动应用
   ```bash
   streamlit run streamlit.py
   ```
3. 打开浏览器，进入`localhost:8501`即可开始对话[1]

Citations:
[1] https://huggingface.co/Rnglg2/internLM2-SD_PROMPT


### 项目功能
![SD提示词助手](https://github.com/user-attachments/assets/9364d154-8582-4b80-934a-b4fcde9adfa4)


#### 任务输入
- 用户输入自然语言描述。
- 系统生成提示词。

#### 自然语言处理
- 使用书生大模型将自然语言转换为Stable Diffusion提示词。

#### 模型微调
- 使用XTuner工具进行QLoRA或全量参数微调，让模型学习更多的提示词示例，以便更好地生成提示词。

### 后续更新方向
1. **生成图片**：将生成的提示词结合Stable Diffusion WebUI API，实现自然语言直接生成符合要求的图片。
2. **个性化优化建议**：根据用户的使用习惯和历史数据，提供个性化的提示词优化建议。
基于 InternLM 的 SD提示词助手 项目，欢迎大家也来参加书生大模型实战营项目(http://github.com/internLM/tutorial)
***个人学习python做的第一个项目，用于学习,目前项目属于是看看乐乐的情况，并不具备实际的能力***
