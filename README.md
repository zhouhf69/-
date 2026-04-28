# 病历事实触发与临床建议系统（MVP）

本项目实现一个可运行的后端基础系统，用于：

- 接收多来源病历结构化事实（可由 HIS、复制粘贴解析、OCR 解析后的结果汇入）。
- 以**知识库**为基础触发规则与建议。
- 自动进行基础计算/评分并输出临床参考建议。

> 当前阶段：提示与参考建议。
> 下一阶段：可对接医嘱草案，医生确认后回写 HIS。

## 快速启动

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m app.main
```

## API

### 1) 健康检查

`GET /health`

### 2) 查看知识库

`GET /knowledge-base`

返回规则版本和已加载的临床触发规则。

### 3) 病例评估

`POST /evaluate`

示例请求：

```json
{
  "patient_id": "p001",
  "encounter_id": "enc-001",
  "facts": [
    {"key": "eGFR", "value": 25, "source": "his"},
    {"key": "glucose", "value": 3.2, "source": "ocr"},
    {"key": "age", "value": 70, "source": "his"},
    {"key": "systolic_bp", "value": 150, "source": "his"}
  ]
}
```

示例输出：
- 触发肾功能用药审查。
- 触发低血糖高风险提醒。
- 计算基础心血管风险指数（演示评分）。

## 架构说明（简化）

- `app/knowledge_base.py`: 知识库与规则定义（触发与建议基础）。
- `app/engine.py`: 规则执行引擎与评分计算。
- `app/models.py`: 输入输出数据模型。
- `app/main.py`: 轻量 HTTP 接口层（健康检查/知识库/评估）。

## 测试

```bash
pytest -q
```

## 下一步建议

1. 引入指南条文版本化（按病种/年份/证据级别）。
2. 接入向量检索（RAG）支持条款可解释追溯。
3. 增加药物相互作用与禁忌数据库。
4. 增加医院版对接层（HIS/EMR/医嘱）。
