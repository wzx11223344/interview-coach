"""5-dimension scoring engine with detailed feedback generation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Dimension definitions
# ---------------------------------------------------------------------------
@dataclass
class Dimension:
    name: str
    name_cn: str
    max_score: int
    description: str
    keywords: list[str] = field(default_factory=list)


DIMENSIONS: list[Dimension] = [
    Dimension("clarity",    "表达清晰度",  20, "语言是否流畅、逻辑是否清晰、表达是否简洁有力"),
    Dimension("relevance",  "内容相关性",  20, "回答是否紧扣问题、是否有具体的案例和数据支撑"),
    Dimension("depth",      "思考深度",    20, "分析是否深入、是否有独立思考、是否能洞察本质"),
    Dimension("structure",  "结构完整性",  20, "回答是否有清晰的结构框架（STAR/PREP等）、层次是否分明"),
    Dimension("confidence", "自信与气场",   20, "语气是否自信、态度是否积极、是否有感染力"),
]


# ---------------------------------------------------------------------------
# Scoring engine
# ---------------------------------------------------------------------------
@dataclass
class ScoredAnswer:
    question_text: str
    category: str
    answer: str
    dim_scores: dict[str, int]    # dimension_name -> 0..20
    total_score: int              # 0..100
    strengths: list[str]
    weaknesses: list[str]
    general_feedback: str


def score_answer(
    question_text: str,
    question_category: str,
    answer: str,
) -> ScoredAnswer:
    """Score a single answer across 5 dimensions with rule-based heuristics.

    The scoring is based on the answer length, keyword matching, structural
    indicators, and content quality markers.  In production this would be
    replaced by an LLM-based evaluator.
    """
    dim_scores: dict[str, int] = {}
    strengths: list[str] = []
    weaknesses: list[str] = []

    # -- Clarity: length sanity + sentence variety ------------------------
    clarity = _score_clarity(answer, strengths, weaknesses)
    dim_scores["clarity"] = clarity

    # -- Relevance: keyword overlap with question ------------------------
    relevance = _score_relevance(answer, question_category, strengths, weaknesses)
    dim_scores["relevance"] = relevance

    # -- Depth: analytical signals ---------------------------------------
    depth = _score_depth(answer, strengths, weaknesses)
    dim_scores["depth"] = depth

    # -- Structure: structural markers -----------------------------------
    structure = _score_structure(answer, strengths, weaknesses)
    dim_scores["structure"] = structure

    # -- Confidence: tone / positivity / initiative ----------------------
    confidence = _score_confidence(answer, strengths, weaknesses)
    dim_scores["confidence"] = confidence

    total = sum(dim_scores.values())

    general_feedback = _build_general_feedback(total, strengths, weaknesses)

    return ScoredAnswer(
        question_text=question_text,
        category=question_category,
        answer=answer,
        dim_scores=dim_scores,
        total_score=total,
        strengths=strengths,
        weaknesses=weaknesses,
        general_feedback=general_feedback,
    )


# ---------------------------------------------------------------------------
# Per-dimension scoring heuristics
# ---------------------------------------------------------------------------
def _score_clarity(text: str, strengths: list[str], weaknesses: list[str]) -> int:
    text_clean = text.strip()
    length = len(text_clean)
    sentences = [s for s in text_clean.replace("!", ".").replace("？", ".").split("。") if s.strip()]
    score = 8  # baseline

    if length < 50:
        weaknesses.append("回答过于简短，缺乏充分展开")
        return max(4, score - 4)
    if length < 120:
        score -= 1
    if length >= 300:
        score += 2
        strengths.append("回答内容充实，充分展开论述")
    if length >= 500:
        score += 2

    if len(sentences) >= 5:
        score += 2
    if len(sentences) >= 8:
        score += 1

    # fluency markers
    fluency = sum(text_clean.count(w) for w in ["首先", "其次", "最后", "因为", "所以", "因此", "总结"])
    if fluency >= 2:
        score += 1
    if fluency >= 4:
        score += 1
        strengths.append("表达流畅，逻辑衔接自然")

    return min(20, max(4, score))


def _score_relevance(text: str, category: str, strengths: list[str], weaknesses: list[str]) -> int:
    score = 8

    # Numeric data signals
    import re
    numbers = len(re.findall(r"\d+", text))
    if numbers >= 3:
        score += 2
        strengths.append("使用了具体数据进行支撑")
    if numbers >= 6:
        score += 1

    # Case / example signals
    case_signals = ["案例", "比如", "例如", "项目", "经历", "团队", "数据", "指标",
                    "案例", "实际", "当时", "结果", "我们", "我负责"]
    hits = sum(1 for s in case_signals if s in text)
    if hits >= 3:
        score += 2
    if hits >= 6:
        score += 2
        strengths.append("有具体的案例或项目经验支撑")
    if hits < 2 and len(text) > 50:
        weaknesses.append("缺少具体案例或数据支撑，建议使用STAR法则展开")

    # did user directly answer the question?
    generic_words = ["我认为", "一般", "通常", "大概", "可能"]
    gen_count = sum(1 for w in generic_words if w in text)
    if gen_count >= 3:
        score -= 1
        weaknesses.append("回答过于笼统，建议更加具体和有针对性")

    return min(20, max(4, score))


def _score_depth(text: str, strengths: list[str], weaknesses: list[str]) -> int:
    score = 8

    deep_signals = {
        "本质": 2, "根因": 2, "底层": 2, "权衡": 2, "tradeoff": 2,
        "反思": 2, "复盘": 2, "方法论": 2, "框架": 2, "framework": 2,
        "长期": 1, "短期": 1, "ROI": 1, "投入产出": 1, "优先级": 1,
        "假设": 1, "验证": 1, "关键": 1, "核心": 1, "策略": 1,
        "抽象": 1, "模式": 1, "pattern": 1, "系统性地": 2,
    }
    for word, bonus in deep_signals.items():
        if word in text:
            score += bonus

    if score >= 14:
        strengths.append("展现了深入的独立思考和分析能力")
    if score <= 9 and len(text) > 80:
        weaknesses.append("回答偏向表层描述，建议增加深度分析和反思")

    return min(20, max(4, score))


def _score_structure(text: str, strengths: list[str], weaknesses: list[str]) -> int:
    score = 8

    # STAR structure detection
    star_signals = ["背景", "情境", "任务", "行动", "结果", "Situation",
                    "Task", "Action", "Result"]
    star_hits = sum(1 for s in star_signals if s in text)
    if star_hits >= 3:
        score += 3
        strengths.append("使用了STAR结构化表达")
    if star_hits >= 5:
        score += 1

    # General structure markers
    struct_signals = ["第一", "第二", "第三", "首先", "其次", "最后", "总结", "综上"]
    struct_hits = sum(1 for s in struct_signals if s in text)
    if struct_hits >= 2:
        score += 2
    if struct_hits >= 4:
        score += 1
        strengths.append("回答层次分明，结构清晰")

    if star_hits < 2 and struct_hits < 2 and len(text) > 100:
        weaknesses.append("建议使用STAR法则或总分总结构来组织回答")

    return min(20, max(4, score))


def _score_confidence(text: str, strengths: list[str], weaknesses: list[str]) -> int:
    score = 8

    conf_signals = {
        "我认为": 1, "我坚信": 2, "我能够": 2, "我擅长": 2,
        "主动": 2, "推动": 2, "主导": 2, "负责": 1, "带领": 2,
        "成果": 1, "达成": 1, "超额": 2, "突破": 2, "创新": 1,
    }
    for word, bonus in conf_signals.items():
        if word in text:
            score += bonus

    weak_signals = ["可能", "大概", "也许", "不确定", "不太清楚"]
    weak_count = sum(1 for w in weak_signals if w in text)
    if weak_count >= 3:
        score -= 2
        weaknesses.append("表达中带有较多不确定词汇，建议更加自信和坚定")
    if weak_count >= 5:
        score -= 2

    return min(20, max(4, score))


def _build_general_feedback(total: int, strengths: list[str], weaknesses: list[str]) -> str:
    if total >= 85:
        tier = "优秀——你的回答展现了出色的综合素质，继续保持！"
    elif total >= 70:
        tier = "良好——整体表现不错，部分维度还有提升空间。"
    elif total >= 55:
        tier = "一般——基本能够回答问题，但深度和结构感需要加强。"
    else:
        tier = "需要提升——建议系统性地准备面试，多练习STAR结构化表达。"

    parts = [tier]
    if strengths:
        parts.append("亮点：" + "；".join(strengths[:3]))
    if weaknesses:
        parts.append("改进方向：" + "；".join(weaknesses[:3]))
    return "  ".join(parts)


# ---------------------------------------------------------------------------
# Session-level aggregation
# ---------------------------------------------------------------------------
@dataclass
class SessionScore:
    total_score: int          # average across all answers
    scores: list[ScoredAnswer]
    dim_averages: dict[str, float]
    overall_strengths: list[str]
    overall_weaknesses: list[str]


def aggregate_session(scores: list[ScoredAnswer]) -> SessionScore:
    """Aggregate per-answer scores into a session-level result."""
    if not scores:
        return SessionScore(
            total_score=0, scores=[], dim_averages={},
            overall_strengths=[], overall_weaknesses=[],
        )

    avg_total = round(sum(s.total_score for s in scores) / len(scores))

    dim_totals: dict[str, float] = {d.name: 0.0 for d in DIMENSIONS}
    for s in scores:
        for d in DIMENSIONS:
            dim_totals[d.name] += s.dim_scores.get(d.name, 0)
    dim_averages = {k: round(v / len(scores), 1) for k, v in dim_totals.items()}

    # Collect top strengths & weaknesses across all answers
    from collections import Counter
    str_counter: Counter[str] = Counter()
    weak_counter: Counter[str] = Counter()
    for s in scores:
        for item in s.strengths:
            str_counter[item] += 1
        for item in s.weaknesses:
            weak_counter[item] += 1

    overall_strengths = [k for k, _ in str_counter.most_common(5)]
    overall_weaknesses = [k for k, _ in weak_counter.most_common(5)]

    return SessionScore(
        total_score=avg_total,
        scores=scores,
        dim_averages=dim_averages,
        overall_strengths=overall_strengths,
        overall_weaknesses=overall_weaknesses,
    )
