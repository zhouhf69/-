# 医疗大数据体检报告工作流

该项目提供一个可在 Windows PC 上运行的体检报告批量解析与 HTML 输出工具，支持 doc/docx/PDF 等格式，并可嵌入国内免费的大语言模型（如通义千问 DashScope 免费额度）生成高质量的健康分析内容。

## 功能概述

- 自动遍历 `data/` 目录下的体检报告文件，支持 `.doc`、`.docx`、`.pdf`。
- 解析报告中的关键指标，并计算多份报告之间的趋势变化。
- 调用大模型生成风险评估、健康解读、干预建议、随访计划等叙事内容。
- 使用 Jinja2 模板渲染出视觉效果良好的 HTML 健康分析报告。
- 自带规则引擎兜底，即使没有配置大模型 API 也能生成基础版本的报告。

## 环境准备

1. **安装 Python**（3.10 及以上）并将其加入 PATH。
2. 推荐使用虚拟环境隔离依赖：
   ```bash
   python -m venv .venv
   .venv\\Scripts\\activate  # Windows
   # 或 source .venv/bin/activate  # macOS/Linux
   ```
3. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

## 大模型配置

项目默认集成了 **通义千问 DashScope** 的兼容模式 API：

1. 注册并登录 [DashScope 控制台](https://dashscope.aliyun.com/)，领取免费额度。
2. 在控制台生成 API Key，并在运行前设置环境变量：
   ```powershell
   setx DASHSCOPE_API_KEY "your_api_key"
   ```
3. 运行程序时通过 `--ai-provider dashscope` 指定使用通义千问；如未设置该参数，则自动启用规则兜底模式。

未来可以在 `health_report/llm.py` 中扩展更多国内免费模型（如智谱 GLM、百度文心千帆等）。

## 使用说明

1. 将原始体检报告文件放入 `data/` 目录，文件命名建议采用 `用户ID_日期.xxx` 形式，例如 `user123_2023-08-01.pdf`。
2. 运行主程序：
   ```bash
   python main.py data \
       --template templates/report_template.html \
       --output output \
       --hotline 400-123-4567 \
       --consult 400-765-4321 \
       --ai-provider dashscope \
       --ai-model qwen-plus
   ```
3. 程序运行结束后，可在 `output/` 目录找到生成的 HTML 报告。

若没有大模型 API Key，可省略 `--ai-provider` 参数，系统将使用内置模板生成基础文案。

## 目录结构

```
├── data/                     # 原始体检报告目录（需手动放置文件）
├── output/                   # 输出的 HTML 报告
├── templates/
│   └── report_template.html  # 报告模板，可根据需要自行美化
├── health_report/
│   ├── aggregator.py         # 指标趋势分析
│   ├── config.py             # 配置管理
│   ├── ingestion.py          # 文件读取与格式转换
│   ├── llm.py                # 大模型调用封装
│   ├── parser.py             # 文本解析
│   ├── renderer.py           # HTML 渲染
│   └── workflow.py           # 工作流调度
├── main.py                   # 程序入口
└── requirements.txt          # Python 依赖
```

## 注意事项

- `.doc` 文件需要本地安装 LibreOffice 并确保 `soffice` 命令可用。
- 自动解析体检数据可能存在误差，生成的报告仅供参考，不能替代专业医生的诊断。
- 在处理个人健康信息时请务必遵守数据隐私及合规要求。
