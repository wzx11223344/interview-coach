"""Question bank: 50+ questions across behavioral, technical, and situational categories.

Covers Chinese interview scenarios for 互联网, 金融, 咨询 industries.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Question:
    text: str
    category: str        # behavioral / technical / situational
    sub_category: str     # e.g. leadership, coding, conflict
    difficulty: str       # easy / medium / hard
    expected_duration: int = 120  # seconds


# ---------------------------------------------------------------------------
# Behavioral Questions (STAR method) -- 行为面试
# ---------------------------------------------------------------------------
BEHAVIORAL_QUESTIONS: list[Question] = [
    Question("请用STAR法则描述一个你主导过的、最具挑战性的项目。", "behavioral", "project_management", "hard"),
    Question("你遇到过最困难的技术决策是什么？你是如何做出选择的？", "behavioral", "decision_making", "hard"),
    Question("请分享一次你与同事产生严重分歧的经历，你是如何处理的？", "behavioral", "conflict_resolution", "medium"),
    Question("描述一次你在紧迫截止日期下完成任务的经历。", "behavioral", "pressure_handling", "medium"),
    Question("有没有一个项目失败的经历？你从中学到了什么？", "behavioral", "failure_reflection", "hard"),
    Question("请举例说明你是如何在团队中推动一项变革的。", "behavioral", "leadership", "hard"),
    Question("描述一次你主动承担额外责任的经历。", "behavioral", "initiative", "medium"),
    Question("你是如何平衡多个优先级的任务？请用具体例子说明。", "behavioral", "time_management", "medium"),
    Question("请分享一个你通过数据驱动决策解决问题的例子。", "behavioral", "data_driven", "medium"),
    Question("你曾经指导过初级同事吗？你采用了什么方法？", "behavioral", "mentorship", "easy"),
    Question("描述一次你在信息不完整的情况下做出决策的经历。", "behavioral", "decision_making", "hard"),
    Question("你是如何获得跨部门团队的支持来完成项目的？", "behavioral", "cross_functional", "medium"),
    Question("举例说明你如何从用户反馈中发现问题并推动解决的。", "behavioral", "user_centric", "medium"),
    Question("请描述一次你自己学习新技术并应用到工作中的经历。", "behavioral", "self_learning", "easy"),
    Question("你曾经说服过领导改变决策吗？你是怎么做的？", "behavioral", "influence", "hard"),
    Question("分享一个你通过创新方法来提升效率的案例。", "behavioral", "innovation", "medium"),
]

# ---------------------------------------------------------------------------
# Technical Questions -- 技术面试
# ---------------------------------------------------------------------------
TECHNICAL_QUESTIONS: list[Question] = [
    Question("请设计一个支持千万级DAU的推送系统架构。", "technical", "system_design", "hard"),
    Question("如何设计一个高可用的分布式缓存系统？考虑一致性、分区容错。", "technical", "system_design", "hard"),
    Question("请解释CAP定理，并举例说明在实际系统中如何权衡。", "technical", "fundamentals", "medium"),
    Question("设计一个类似微博的Feed流系统，核心关注点是什么？", "technical", "system_design", "hard"),
    Question("你是如何进行代码审查的？请分享你的审查清单。", "technical", "engineering_practice", "medium"),
    Question("请设计一个RESTful API的最佳实践方案，包括版本管理、错误处理等。", "technical", "api_design", "medium"),
    Question("假设系统出现性能瓶颈，你将从哪些维度进行排查和优化？", "technical", "performance", "medium"),
    Question("请解释微服务架构的优缺点，什么场景下适合使用？", "technical", "architecture", "medium"),
    Question("如何确保一个金融交易系统的数据一致性？", "technical", "system_design", "hard"),
    Question("请讲解数据库索引的原理，以及如何针对慢查询进行优化。", "technical", "database", "medium"),
    Question("设计一个秒杀系统的核心方案，如何应对高并发？", "technical", "system_design", "hard"),
    Question("你如何保证自己编写的代码质量？谈谈你的测试策略。", "technical", "engineering_practice", "medium"),
    Question("请描述一个你引入并落地的最佳工程实践。", "technical", "engineering_practice", "hard"),
    Question("如何进行技术选型？请分享你的评估框架。", "technical", "decision_making", "medium"),
    Question("设计一个API网关，需要支持限流、鉴权、路由转发。", "technical", "system_design", "hard"),
    Question("你有使用过哪些方式提升系统可观测性（监控、日志、追踪）？", "technical", "observability", "medium"),
    Question("请对比关系型数据库和NoSQL数据库的适用场景。", "technical", "database", "easy"),
    Question("设计一个电商平台的订单系统，需要处理订单状态流转和库存扣减。", "technical", "system_design", "hard"),
]

# ---------------------------------------------------------------------------
# Situational Questions -- 情景面试
# ---------------------------------------------------------------------------
SITUATIONAL_QUESTIONS: list[Question] = [
    Question("假如你加入公司一个月后发现项目方向有严重问题，你会怎么做？", "situational", "leadership", "hard"),
    Question("你的产品上线前一天发现了一个可能导致用户数据丢失的Bug，你如何处理？", "situational", "crisis_management", "hard"),
    Question("如果上级给你安排了一个你认为不可行的任务，你会如何应对？", "situational", "communication", "medium"),
    Question("团队中有一位资深同事拒绝配合你的方案，你怎么办？", "situational", "conflict_resolution", "medium"),
    Question("你发现竞品推出了一个对标功能，你作为产品经理如何应对？", "situational", "product_strategy", "medium"),
    Question("产品的核心指标连续两周下滑，你会如何分析和应对？", "situational", "data_analysis", "hard"),
    Question("如果需要在技术债务和新功能开发之间做取舍，你会怎么决策？", "situational", "trade_off", "medium"),
    Question("作为新人，你如何在入职90天内证明自己的价值？", "situational", "onboarding", "easy"),
    Question("客户提出的需求与技术可行性有冲突，作为解决方案架构师你如何处理？", "situational", "client_management", "hard"),
    Question("项目资源被削减了30%，你如何重新规划以保证核心交付？", "situational", "resource_management", "hard"),
    Question("团队远程协作效率持续下降，你会采取哪些措施？", "situational", "team_management", "medium"),
    Question("你发现团队中有人存在严重的职业倦怠，作为Leader你如何帮助他？", "situational", "people_management", "medium"),
    Question("CEO突然要求你在两周内交付一个原定三个月的功能，你如何回应？", "situational", "stakeholder_management", "hard"),
    Question("需求方不断变更需求导致项目延期，你如何建立有效的需求管理机制？", "situational", "process_improvement", "medium"),
    Question("你接手了一个代码质量极差的遗留系统，你的改善策略是什么？", "situational", "technical_debt", "hard"),
    Question("两个核心业务方的需求相互冲突，资源只能支持一个，如何决策？", "situational", "prioritization", "hard"),
    Question("有用户在社交媒体上公开投诉你的产品，作为负责人你如何处理？", "situational", "crisis_pr", "medium"),
    Question("面试官问：'你还有什么问题想问我们吗？' 你会问哪三个问题？", "situational", "reverse_interview", "easy"),
]

# ---------------------------------------------------------------------------
# Role-specific question filters
# ---------------------------------------------------------------------------
ROLE_KEYWORDS: dict[str, list[str]] = {
    "产品经理":     ["product_strategy", "user_centric", "data_driven", "prioritization",
                     "stakeholder_management", "cross_functional"],
    "后端开发":     ["system_design", "database", "api_design", "performance",
                     "engineering_practice", "observability"],
    "前端开发":     ["system_design", "engineering_practice", "performance", "innovation"],
    "算法工程师":   ["fundamentals", "performance", "innovation", "data_driven"],
    "数据分析师":   ["data_driven", "data_analysis", "user_centric", "decision_making"],
    "项目经理":     ["project_management", "time_management", "stakeholder_management",
                     "resource_management", "process_improvement"],
    "技术Leader":   ["leadership", "people_management", "architecture", "decision_making",
                     "mentorship", "trade_off"],
    "解决方案架构师": ["system_design", "client_management", "architecture", "trade_off"],
    "咨询顾问":     ["data_driven", "decision_making", "influence", "communication",
                     "client_management", "prioritization"],
    "金融分析师":   ["data_driven", "data_analysis", "decision_making", "pressure_handling"],
}

DIFFICULTY_WEIGHTS = {
    "easy":   [0.50, 0.35, 0.15],  # easy / medium / hard
    "medium": [0.25, 0.50, 0.25],
    "hard":   [0.10, 0.30, 0.60],
}


def _filter_by_role(questions: list[Question], role: Optional[str]) -> list[Question]:
    """Boost questions matching the role's sub-categories."""
    if not role or role not in ROLE_KEYWORDS:
        return list(questions)
    keywords = ROLE_KEYWORDS[role]
    matched, rest = [], []
    for q in questions:
        (matched if q.sub_category in keywords else rest).append(q)
    # put matched questions first, then fill with rest
    return matched + rest


def _filter_by_difficulty(questions: list[Question], difficulty: str) -> list[Question]:
    """Proportionally include questions by difficulty tier."""
    weights = DIFFICULTY_WEIGHTS.get(difficulty, DIFFICULTY_WEIGHTS["medium"])
    by_diff: dict[str, list[Question]] = {"easy": [], "medium": [], "hard": []}
    for q in questions:
        by_diff[q.difficulty].append(q)
    result: list[Question] = []
    rng = random.Random()
    for tier in ("easy", "medium", "hard"):
        pool = by_diff[tier]
        if not pool:
            continue
        take = max(1, int(len(questions) * weights[{"easy": 0, "medium": 1, "hard": 2}[tier]]))
        result.extend(rng.sample(pool, min(take, len(pool))))
    rng.shuffle(result)
    return result


def build_question_pool(
    role: Optional[str] = None,
    difficulty: str = "medium",
    rounds: int = 5,
) -> list[Question]:
    """Build a curated question pool for the interview session.

    Parameters
    ----------
    role: target role (e.g. 产品经理, 后端开发).
    difficulty: easy / medium / hard.
    rounds: number of questions to select.
    """
    all_questions = BEHAVIORAL_QUESTIONS + TECHNICAL_QUESTIONS + SITUATIONAL_QUESTIONS
    filtered = _filter_by_role(all_questions, role)
    filtered = _filter_by_difficulty(filtered, difficulty)

    if len(filtered) < rounds:
        # Padding: duplicate with shuffle if not enough
        filtered = (filtered * (rounds // len(filtered) + 1))[:rounds]
        random.shuffle(filtered)
        return filtered

    return filtered[:rounds]


def all_questions() -> list[Question]:
    """Return the full question bank."""
    return BEHAVIORAL_QUESTIONS + TECHNICAL_QUESTIONS + SITUATIONAL_QUESTIONS


def get_question_count() -> int:
    return len(all_questions())
