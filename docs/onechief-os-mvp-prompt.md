# 《OneChief OS 医疗创业驾驶舱 MVP 开发提示词》

请开发一个名为 **OneChief OS 医疗创业驾驶舱** 的Web应用。
目标：帮助医疗专家/医院管理者把日常想法转化为可开发、可销售、可复用的医疗 AI 产品。

## 一、产品定位

这是“一人公司平台”的 MVP 版本：优先实现从想法到机会判断、任务拆解、商业化输出、产品货架沉淀的闭环。

核心用户：医疗专家、医院管理者、医生创业者、医疗AI负责人、健康管理中心负责人。

## 二、核心模块

1. 创业灵感录入模块（ideas）
2. AI总管分析模块（analysis）
3. 产品机会评分模块（score）
4. Agent 拆解模块（sequential prompts）
5. 开发任务模块（dev tasks）
6. 产品货架模块（product shelf）
7. AI开发值班员模块 v0.1（prompt/error/fix/qa）
8. 体检报告解读闭环模块（预留变现入口）

## 三、页面结构（12页）

1. 首页仪表盘
2. 灵感列表
3. 新建灵感
4. 灵感详情
5. AI分析结果
6. 产品评分
7. Agent拆解
8. 开发任务列表
9. 开发值班员
10. 产品货架
11. 体检报告解读MVP
12. 系统设置

## 四、数据表设计

- users
- ideas
- ai_analysis
- opportunity_scores
- agent_outputs
- dev_tasks
- product_shelf
- dev_supervisor_logs
- health_report_cases
- health_report_items
- ai_prompt_templates
- system_settings

## 五、技术栈

- 前端：Next.js + Tailwind + shadcn/ui（或 Vue3 + Vite + Element Plus）
- 后端：FastAPI + PostgreSQL + Redis（可选）
- ORM：SQLAlchemy 或 Prisma
- API：REST
- AI层：OpenAI-compatible 抽象（base_url/api_key/model_name 可配置）
- 部署：Docker Compose + Nginx + 腾讯云轻量服务器

## 六、输出要求

必须提供：

- 可运行代码
- 数据库迁移文件
- docker-compose
- `.env.example`
- README
- 示例数据
- 示例提示词
- 本地启动方法
- 腾讯云部署说明

## 七、交付优先级（非常重要）

第一目标：

> 用户输入一个医疗创业想法，系统可自动分析、评分、拆解开发任务、生成开发提示词，并沉淀到产品货架。

不要过度设计，先保证 MVP 跑通。
