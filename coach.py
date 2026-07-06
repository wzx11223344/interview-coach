#!/usr/bin/env python3
"""AI-Powered Job Interview Simulator -- CLI Entry Point.

Usage:
    python coach.py start --role 产品经理 --difficulty hard --rounds 5
    python coach.py start --role 后端开发 --difficulty medium --rounds 3 --output ./reports
    python coach.py list-roles
    python coach.py list-questions --category behavioral
"""

from __future__ import annotations

import argparse
import sys
import os

# Ensure the parent directory is on the path for direct execution
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from interview_coach.engine import InterviewEngine, run_interactive
from interview_coach.questions import (
    BEHAVIORAL_QUESTIONS,
    TECHNICAL_QUESTIONS,
    SITUATIONAL_QUESTIONS,
    ROLE_KEYWORDS,
    build_question_pool,
    get_question_count,
    Question,
)


def cmd_start(args: argparse.Namespace) -> None:
    """Start an interactive interview session."""
    engine = InterviewEngine(
        role=args.role,
        difficulty=args.difficulty,
        rounds=args.rounds,
        output_dir=args.output,
    )
    run_interactive(engine)


def cmd_list_roles(args: argparse.Namespace) -> None:
    """List supported roles with their keyword mappings."""
    print(f"\n支持的岗位角色 ({len(ROLE_KEYWORDS)}):\n")
    for role, keywords in sorted(ROLE_KEYWORDS.items()):
        print(f"  {role}")
        print(f"    关联能力: {', '.join(keywords)}")
    print()


def cmd_list_questions(args: argparse.Namespace) -> None:
    """List questions from the bank, optionally filtered by category."""
    category = args.category
    if category == "behavioral":
        pool = BEHAVIORAL_QUESTIONS
    elif category == "technical":
        pool = TECHNICAL_QUESTIONS
    elif category == "situational":
        pool = SITUATIONAL_QUESTIONS
    else:
        pool = BEHAVIORAL_QUESTIONS + TECHNICAL_QUESTIONS + SITUATIONAL_QUESTIONS

    cat_map = {"behavioral": "行为面试", "technical": "技术面试", "situational": "情景面试"}
    print(f"\n题库 (共 {len(pool)} 题):\n")
    for i, q in enumerate(pool, 1):
        print(f"  [{i:02d}] [{cat_map.get(q.category, q.category)}] [{q.difficulty.upper()}]")
        print(f"       {q.text}")
        print()


def cmd_preview(args: argparse.Namespace) -> None:
    """Preview the questions that would be selected for a given configuration."""
    pool = build_question_pool(
        role=args.role, difficulty=args.difficulty, rounds=args.rounds
    )
    cat_map = {"behavioral": "行为面试", "technical": "技术面试", "situational": "情景面试"}
    print(f"\n题目预览 (岗位: {args.role}, 难度: {args.difficulty}, 轮次: {args.rounds}):\n")
    for i, q in enumerate(pool, 1):
        print(f"  [{i}/{len(pool)}] [{cat_map.get(q.category, q.category)}] [{q.difficulty.upper()}]")
        print(f"       {q.text}")
    print()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="AI 模拟面试官 -- 智能模拟面试训练工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python coach.py start --role 产品经理 --difficulty hard --rounds 5
  python coach.py start --role 后端开发 --difficulty medium --rounds 3
  python coach.py preview --role 数据分析师 --difficulty medium
  python coach.py list-roles
  python coach.py list-questions --category behavioral
        """,
    )

    sub = parser.add_subparsers(dest="command", help="子命令")

    # start
    p_start = sub.add_parser("start", help="开始模拟面试")
    p_start.add_argument("--role", default="产品经理", help="目标岗位 (默认: 产品经理)")
    p_start.add_argument("--difficulty", default="medium",
                         choices=["easy", "medium", "hard"], help="难度 (默认: medium)")
    p_start.add_argument("--rounds", type=int, default=5, help="面试轮次 (默认: 5)")
    p_start.add_argument("--output", "-o", default=None, help="报告输出目录")
    p_start.set_defaults(func=cmd_start)

    # preview
    p_preview = sub.add_parser("preview", help="预览题目")
    p_preview.add_argument("--role", default="产品经理", help="目标岗位")
    p_preview.add_argument("--difficulty", default="medium",
                           choices=["easy", "medium", "hard"], help="难度")
    p_preview.add_argument("--rounds", type=int, default=5, help="面试轮次")
    p_preview.set_defaults(func=cmd_preview)

    # list-roles
    p_roles = sub.add_parser("list-roles", help="列出支持的岗位角色")
    p_roles.set_defaults(func=cmd_list_roles)

    # list-questions
    p_q = sub.add_parser("list-questions", help="列出题库")
    p_q.add_argument("--category", "-c", default="all",
                     choices=["all", "behavioral", "technical", "situational"],
                     help="题目分类")
    p_q.set_defaults(func=cmd_list_questions)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    args.func(args)


if __name__ == "__main__":
    main()
