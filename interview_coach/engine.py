"""Interview orchestration: manages the full interview lifecycle.

Coordinates question selection, answer collection, scoring, and report generation.
"""

from __future__ import annotations

import os
import sys
import time
from typing import Optional, Callable
from enum import Enum

from interview_coach.questions import (
    Question,
    build_question_pool,
    get_question_count,
    ROLE_KEYWORDS,
)
from interview_coach.scorer import (
    score_answer,
    aggregate_session,
    ScoredAnswer,
    SessionScore,
)
from interview_coach.report import generate_html_report, save_report


class InterviewState(Enum):
    IDLE = "idle"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class InterviewEngine:
    """Core interview orchestrator.

    Usage::

        engine = InterviewEngine(role="产品经理", difficulty="hard", rounds=5)
        engine.start()
        while not engine.is_finished:
            print(engine.current_question)
            engine.submit_answer(input(">> "))
        engine.finish()
    """

    def __init__(
        self,
        role: str = "产品经理",
        difficulty: str = "medium",
        rounds: int = 5,
        output_dir: Optional[str] = None,
        on_question: Optional[Callable[[Question, int, int], None]] = None,
        on_score: Optional[Callable[[ScoredAnswer], None]] = None,
    ):
        if difficulty not in ("easy", "medium", "hard"):
            raise ValueError(f"Invalid difficulty: {difficulty}")
        if rounds < 1 or rounds > 20:
            raise ValueError("rounds must be between 1 and 20")

        self.role = role
        self.difficulty = difficulty
        self.rounds = rounds
        self.output_dir = output_dir or os.getcwd()
        self.on_question = on_question
        self.on_score = on_score

        self.state = InterviewState.IDLE
        self.questions: list[Question] = []
        self.answers: list[ScoredAnswer] = []
        self.current_index = 0
        self.session_score: Optional[SessionScore] = None
        self.report_path: Optional[str] = None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def start(self) -> str:
        """Initialize the interview session. Returns a welcome message."""
        self.questions = build_question_pool(
            role=self.role, difficulty=self.difficulty, rounds=self.rounds
        )
        self.answers = []
        self.current_index = 0
        self.state = InterviewState.IN_PROGRESS
        self.session_score = None
        self.report_path = None

        return (
            f"\n{'=' * 60}\n"
            f"  AI 模拟面试官 v1.0\n"
            f"  目标岗位: {self.role}"
            f"  |  难度: {self.difficulty}"
            f"  |  轮次: {self.rounds}\n"
            f"  题库总量: {get_question_count()} 题\n"
            f"{'=' * 60}\n"
            f"\n  面试即将开始，请做好准备！\n"
        )

    @property
    def is_finished(self) -> bool:
        return self.state == InterviewState.COMPLETED

    @property
    def current_question(self) -> Optional[Question]:
        if self.current_index < len(self.questions):
            return self.questions[self.current_index]
        return None

    @property
    def progress(self) -> tuple[int, int]:
        """Returns (current, total)."""
        return (self.current_index + 1, len(self.questions))

    def submit_answer(self, answer: str) -> Optional[ScoredAnswer]:
        """Submit an answer for the current question.

        Returns the scored result, or None if the interview is finished.
        """
        if self.state != InterviewState.IN_PROGRESS:
            return None

        q = self.current_question
        if q is None:
            self.state = InterviewState.COMPLETED
            return None

        scored = score_answer(
            question_text=q.text,
            question_category=q.category,
            answer=answer,
        )
        self.answers.append(scored)
        self.current_index += 1

        if self.on_score:
            self.on_score(scored)

        if self.current_index >= len(self.questions):
            self.state = InterviewState.COMPLETED

        return scored

    def finish(self) -> tuple[SessionScore, str]:
        """Complete the interview, aggregate scores, and generate the HTML report.

        Returns (SessionScore, report_path).
        """
        self.session_score = aggregate_session(self.answers)
        html = generate_html_report(
            session=self.session_score,
            role=self.role,
            difficulty=self.difficulty,
            rounds=self.rounds,
        )
        self.report_path = save_report(html, self.output_dir, role=self.role)
        return self.session_score, self.report_path

    def summary(self) -> str:
        """Return a text summary of the session."""
        if self.session_score is None:
            return "面试尚未结束，请先完成所有回答。"

        lines = [
            f"\n{'=' * 60}",
            f"  面试结束！综合评分: {self.session_score.total_score}/100",
            f"{'=' * 60}",
            "",
            "  [维度得分]",
        ]
        for d_name, d_cn, d_max, _desc in [
            ("clarity", "表达清晰度", 20, ""),
            ("relevance", "内容相关性", 20, ""),
            ("depth", "思考深度", 20, ""),
            ("structure", "结构完整性", 20, ""),
            ("confidence", "自信与气场", 20, ""),
        ]:
            val = self.session_score.dim_averages.get(d_name, 0)
            bar = "#" * int(val) + "-" * (d_max - int(val))
            lines.append(f"  {d_cn}:  [{bar}] {val:.1f}/{d_max}")

        lines.append("")
        if self.session_score.overall_strengths:
            lines.append("  [亮点]")
            for s in self.session_score.overall_strengths[:3]:
                lines.append(f"    + {s}")
        if self.session_score.overall_weaknesses:
            lines.append("  [待改进]")
            for w in self.session_score.overall_weaknesses[:3]:
                lines.append(f"    - {w}")
        lines.append(f"\n  详细报告: {self.report_path}")
        lines.append(f"{'=' * 60}\n")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Interactive CLI mode
# ---------------------------------------------------------------------------
def run_interactive(engine: InterviewEngine) -> None:
    """Run the interview engine in interactive terminal mode."""
    try:
        from rich.console import Console
        from rich.panel import Panel
        from rich.progress import Progress, SpinnerColumn, TextColumn
        from rich.table import Table
        from rich import box
        HAS_RICH = True
    except ImportError:
        HAS_RICH = False

    if HAS_RICH:
        console = Console()

        welcome = engine.start()
        console.print(Panel(welcome.strip(), title="Interview Coach", border_style="blue"))

        while not engine.is_finished:
            q = engine.current_question
            if q is None:
                break
            idx, total = engine.progress

            # Show question
            diff_color = {"easy": "green", "medium": "yellow", "hard": "red"}.get(
                q.difficulty, "white"
            )
            cat_map = {"behavioral": "行为面试", "technical": "技术面试", "situational": "情景面试"}
            console.print(
                Panel(
                    q.text,
                    title=f"[bold]第 {idx}/{total} 题[/bold]",
                    subtitle=f"{cat_map.get(q.category, q.category)} | 难度: [{diff_color}]{q.difficulty.upper()}[/{diff_color}]",
                    border_style="cyan",
                )
            )
            console.print("[dim]请输入你的回答（输入完成后按 Enter）:[/dim]")
            answer = console.input("[bold green]>> [/bold green]")
            console.print()

            scored = engine.submit_answer(answer)
            if scored:
                # Show instant score
                table = Table(box=box.SIMPLE, show_header=True, header_style="bold magenta")
                table.add_column("维度", style="dim")
                table.add_column("得分", justify="center")
                table.add_column("满分", justify="center")
                for d in _get_dimensions():
                    table.add_row(
                        d["cn"],
                        str(scored.dim_scores.get(d["name"], 0)),
                        str(d["max"]),
                    )
                console.print(
                    Panel(
                        table,
                        title=f"[bold]本题得分: {scored.total_score}/100[/bold]",
                        border_style="green",
                    )
                )
                if scored.general_feedback:
                    console.print(f"[yellow]反馈:[/yellow] {scored.general_feedback}")
                console.print()

        # Finish & summary
        session_score, report_path = engine.finish()
        console.print("[bold green]面试完成![/bold green]")

        # Summary table
        table = Table(box=box.SIMPLE, show_header=True, header_style="bold blue")
        table.add_column("维度")
        table.add_column("得分")
        table.add_column("可视化")
        for d in _get_dimensions():
            val = session_score.dim_averages.get(d["name"], 0)
            bar = "#" * int(val) + "-" * (d["max"] - int(val))
            table.add_row(d["cn"], f"{val:.1f}/{d['max']}", f"[cyan]{bar}[/cyan]")
        table.add_row("[bold]综合评分", f"[bold green]{session_score.total_score}/100[/bold green]", "")
        console.print(Panel(table, title="面试结果总览", border_style="blue"))

        console.print(f"\n[bold]详细报告已生成:[/bold] [underline]{report_path}[/underline]\n")

    else:
        # Plain text fallback
        welcome = engine.start()
        print(welcome)

        while not engine.is_finished:
            q = engine.current_question
            if q is None:
                break
            idx, total = engine.progress
            print(f"\n--- 第 {idx}/{total} 题 [{q.category}/{q.difficulty}] ---")
            print(q.text)
            answer = input(">> ")
            scored = engine.submit_answer(answer)
            if scored:
                print(f"\n本题得分: {scored.total_score}/100")
                print(f"反馈: {scored.general_feedback}")

        session_score, report_path = engine.finish()
        print(engine.summary())


def _get_dimensions() -> list[dict]:
    return [
        {"name": "clarity", "cn": "表达清晰度", "max": 20},
        {"name": "relevance", "cn": "内容相关性", "max": 20},
        {"name": "depth", "cn": "思考深度", "max": 20},
        {"name": "structure", "cn": "结构完整性", "max": 20},
        {"name": "confidence", "cn": "自信与气场", "max": 20},
    ]
