---
slug: interview-coach
displayName: AI模拟面试官
category: career
summary: >-
  AI驱动的岗位模拟面试训练工具。支持50+道行为/技术/情景面试题，
  5维评分体系（清晰度/相关性/深度/结构/自信），
  自动生成含雷达图的HTML面试报告。覆盖互联网、金融、咨询等行业。
version: 1.0.0
license: MIT
tags:
  - interview
  - career
  - coaching
  - ai
  - job-search
  - mock-interview
---

# AI模拟面试官 (Interview Coach)

## 概述

AI模拟面试官是一个命令行驱动的智能面试训练工具，帮助你：

- 针对目标岗位进行模拟面试训练
- 覆盖行为面试（STAR法则）、技术架构、情景应变三大类50+题目
- 获得5维量化评分和详细反馈
- 生成专业的HTML可视化面试报告

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 查看支持的岗位
python coach.py list-roles

# 预览面试题目
python coach.py preview --role 产品经理 --difficulty hard --rounds 5

# 开始模拟面试
python coach.py start --role 产品经理 --difficulty hard --rounds 5

# 指定报告输出目录
python coach.py start --role 后端开发 --difficulty medium --rounds 3 -o ./reports
```

## 支持岗位

产品经理、后端开发、前端开发、算法工程师、数据分析师、项目经理、技术Leader、解决方案架构师、咨询顾问、金融分析师

## 难度等级

- **easy**: 侧重基础能力和常见场景
- **medium**: 均衡分布行为/技术/情景题
- **hard**: 侧重系统设计、复杂决策和高压力场景

## 5维评分体系

| 维度 | 满分 | 评估重点 |
|------|------|----------|
| 表达清晰度 | 20 | 语言流畅度、逻辑清晰度、简洁有力 |
| 内容相关性 | 20 | 紧扣问题、案例支撑、数据佐证 |
| 思考深度 | 20 | 深入分析、独立思考、洞察本质 |
| 结构完整性 | 20 | STAR/PREP框架、层次分明 |
| 自信与气场 | 20 | 语气自信、态度积极、感染力 |

## HTML报告

每次面试结束后自动生成HTML报告，包含：

- 综合评分圆环
- 5维雷达图（Chart.js）
- 逐题回放与评分
- 亮点优势和待改进方向
- 面试官综合评价

## 项目结构

```
interview-coach/
├── coach.py                 # CLI入口
├── interview_coach/
│   ├── __init__.py          # 包定义
│   ├── engine.py            # 面试编排引擎
│   ├── questions.py         # 题库（50+题）
│   ├── scorer.py            # 5维评分引擎
│   └── report.py            # HTML报告生成
├── SKILL.md                 # Skill元数据
├── README.md                # 项目文档
└── requirements.txt         # 依赖清单
```

## 编程使用

```python
from interview_coach.engine import InterviewEngine

engine = InterviewEngine(role="产品经理", difficulty="hard", rounds=5)
engine.start()

while not engine.is_finished:
    print(engine.current_question.text)
    engine.submit_answer(input(">> "))

session_score, report_path = engine.finish()
print(engine.summary())
```

## License

MIT
