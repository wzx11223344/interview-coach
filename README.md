# AI模拟面试官 (Interview Coach)

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)

AI驱动的岗位模拟面试训练工具。支持50+道行为/技术/情景面试题，5维评分体系，自动生成含雷达图的专业HTML面试报告。

## 特性

- **丰富题库**: 50+道面试题覆盖行为面试（STAR法则）、技术架构设计、情景应变三大类
- **5维评分**: 清晰度、相关性、深度、结构、自信，每题0-100分
- **智能反馈**: 自动识别亮点和待改进方向，给出面试官风格的综合评价
- **HTML报告**: 含Chart.js雷达图、逐题回放、维度分解的可视化报告
- **多岗位支持**: 产品经理、后端开发、前端开发、算法工程师等10+岗位
- **三级难度**: easy/medium/hard，按比例分配不同难度题目
- **CLI驱动**: 简洁的命令行接口，支持交互式面试和题目预览

## 安装

```bash
git clone <repo-url>
cd interview-coach
pip install -r requirements.txt
```

## 使用

### 命令行

```bash
# 查看支持的岗位
python coach.py list-roles

# 按分类浏览题库
python coach.py list-questions --category behavioral

# 预览面试题目
python coach.py preview --role 产品经理 --difficulty hard --rounds 5

# 开始模拟面试
python coach.py start --role 产品经理 --difficulty hard --rounds 5

# 指定报告输出目录
python coach.py start --role 后端开发 --difficulty medium --rounds 3 -o ./reports
```

### Python API

```python
from interview_coach.engine import InterviewEngine
from interview_coach.questions import build_question_pool

# 构建题库
pool = build_question_pool(role="产品经理", difficulty="hard", rounds=5)

# 运行面试
engine = InterviewEngine(role="产品经理", difficulty="hard", rounds=5)
engine.start()

while not engine.is_finished:
    print(engine.current_question.text)
    engine.submit_answer(input(">> "))

session_score, report_path = engine.finish()
print(engine.summary())
```

## 题库覆盖

| 分类 | 数量 | 子类目 |
|------|------|--------|
| 行为面试 (Behavioral) | 16题 | STAR法则、领导力、冲突处理、压力应对、失败反思 |
| 技术面试 (Technical) | 18题 | 系统设计、API设计、数据库优化、架构权衡、性能调优 |
| 情景面试 (Situational) | 18题 | 危机管理、资源取舍、跨部门协作、利益相关者管理 |

## 评分维度

| 维度 | 满分 | 评估标准 |
|------|------|----------|
| 表达清晰度 (Clarity) | 20 | 语言流畅、逻辑清晰、简洁有力 |
| 内容相关性 (Relevance) | 20 | 紧扣问题、具体案例、数据支撑 |
| 思考深度 (Depth) | 20 | 深入分析、独立思考、洞察本质 |
| 结构完整性 (Structure) | 20 | STAR/PREP框架、层次分明 |
| 自信与气场 (Confidence) | 20 | 语气自信、态度积极、感染力 |

## 依赖

- Python 3.9+
- rich (终端美化)
- Chart.js (HTML报告，CDN引入)

## License

MIT License
