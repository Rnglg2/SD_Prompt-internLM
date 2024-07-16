## 项目规划：Stable Diffusion提示词助手

### 项目简介
本项目旨在为用户生成高质量的Stable Diffusion提示词。用户输入自然语言描述，通过大模型转换为适合Stable Diffusion的提示词，并使用XTuner对模型进行微调，以提升生成效果。主要功能包括：

1. **自然语言到提示词转换**：利用书生大模型将用户输入的自然语言转换为Stable Diffusion的提示词。
2. **模型微调**：使用XTuner工具对模型进行LoRA、QLoRA或全量参数微调，提升生成效果。

### 项目功能
![SD提示词助手](https://github.com/user-attachments/assets/9ab08cdf-eaea-439e-be4e-10c8cbb95756)

#### 任务输入
- 用户输入自然语言描述。
- 系统生成提示词。

#### 自然语言处理
- 使用书生大模型将自然语言转换为Stable Diffusion提示词。

#### 模型微调
- 使用XTuner工具进行LoRA、QLoRA或全量参数微调，让模型学习更多的提示词示例，以便更好地生成提示词。

### 后续更新方向
1. **生成图片**：将生成的提示词结合Stable Diffusion WebUI API，实现自然语言直接生成符合要求的图片。
2. **个性化优化建议**：根据用户的使用习惯和历史数据，提供个性化的提示词优化建议。
