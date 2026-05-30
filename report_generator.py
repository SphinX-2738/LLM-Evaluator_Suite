"""
report_generator.py - Human-Readable Evaluation Reports
Project: LLM Evaluation Tester (Project 1)
Author: Ankur Sharma
Week: 1, Day 2

What this does:
    - Loads evaluation JSON produced by evaluator.py
    - Generates a clean, human-readable report
    - Shows per-test scores with visual indicators
    - Calculates cost analysis
    - Flags issues and gives recommendations
    - Saves report as .txt file (portfolio-ready)

Why this matters:
    Raw JSON is for machines. Reports are for humans.
    In production, your team lead / client / stakeholder
    will never read a JSON file. They need a clear summary:
    "What passed? What failed? What do we fix?"
    This is that summary.
"""

import json
import os
from datetime import datetime


# ─────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────

# OpenAI GPT-4o-mini pricing (for cost estimation reference)
# Even though Groq is free, we calculate real-world cost
# so you can speak to cost optimization in interviews
COST_PER_1M_INPUT_TOKENS  = 0.150   # USD
COST_PER_1M_OUTPUT_TOKENS = 0.600   # USD

REPORT_DIR = "reports"


# ─────────────────────────────────────────────
# HELPER: Score to visual bar
# ─────────────────────────────────────────────

def score_to_bar(score, max_score=10, bar_length=20):
    """
    Convert a numeric score into a visual progress bar.

    Example:
        score_to_bar(8.5) --> "[#################---]  8.5/10"

    Args:
        score (float): The score value
        max_score (int): Maximum possible score
        bar_length (int): Width of the bar in characters

    Returns:
        str: Visual bar string
    """
    filled = int((score / max_score) * bar_length)
    empty  = bar_length - filled
    bar    = "#" * filled + "-" * empty
    return f"[{bar}]  {score:>4.1f}/{max_score}"


def score_to_grade(score):
    """
    Convert numeric score to letter grade with label.

    Args:
        score (float): Score out of 10

    Returns:
        str: Grade label
    """
    if score >= 9.5:  return "A+  (Exceptional)"
    if score >= 9.0:  return "A   (Excellent)"
    if score >= 8.0:  return "B+  (Good)"
    if score >= 7.0:  return "B   (Acceptable)"
    if score >= 6.0:  return "C   (Needs Improvement)"
    if score >= 5.0:  return "D   (Poor)"
    return                    "F   (Failing)"


def verdict_icon(passed):
    """Return visual pass/fail indicator."""
    return "PASS [OK]" if passed else "FAIL [!!]"


# ─────────────────────────────────────────────
# HELPER: Cost calculation
# ─────────────────────────────────────────────

def calculate_cost(prompt_tokens, completion_tokens):
    """
    Calculate estimated cost using OpenAI GPT-4o-mini pricing.

    Why we calculate this even though Groq is free:
        In production you'll use paid APIs. Knowing your cost
        per evaluation run lets you budget and optimize.
        "This evaluation suite costs $0.002 per run, or $2
        for 1000 runs" is a real business metric.

    Args:
        prompt_tokens (int): Input token count
        completion_tokens (int): Output token count

    Returns:
        float: Estimated cost in USD
    """
    input_cost  = (prompt_tokens  / 1_000_000) * COST_PER_1M_INPUT_TOKENS
    output_cost = (completion_tokens / 1_000_000) * COST_PER_1M_OUTPUT_TOKENS
    return round(input_cost + output_cost, 6)


# ─────────────────────────────────────────────
# HELPER: Generate recommendations
# ─────────────────────────────────────────────

def generate_recommendations(evaluated_results):
    """
    Analyze results and generate actionable recommendations.

    This is the intelligence layer of the report.
    Rather than just showing scores, we tell the engineer
    exactly what to fix and why.

    Args:
        evaluated_results (list): List of evaluated test results

    Returns:
        list: List of recommendation strings
    """
    recommendations = []

    for result in evaluated_results:
        ev       = result.get("evaluation", {})
        name     = result.get("test_name", "Unknown")
        category = result.get("category", "")

        if ev.get("status") != "success":
            continue

        score              = ev.get("overall_score", 0)
        format_score       = ev.get("format_compliance", 10)
        hallucination      = ev.get("hallucination_score", 10)
        issues             = ev.get("issues_found", [])
        tokens_used        = result.get("token_usage", {}).get("total_tokens", 0)
        completion_tokens  = result.get("token_usage", {}).get("completion_tokens", 0)
        max_tokens_setting = result.get("max_tokens", 300)

        # Truncation detection
        if completion_tokens >= max_tokens_setting * 0.95:
            recommendations.append(
                f"[WARN] [{name}] Response likely truncated "
                f"({completion_tokens} tokens hit {max_tokens_setting} limit). "
                f"Increase max_tokens for '{category}' category to 500+."
            )

        # Format issues
        if format_score < 9 and "backtick" in " ".join(issues).lower():
            recommendations.append(
                f"[FIX]  [{name}] JSON wrapped in backticks. "
                f"Add to system prompt: 'Return ONLY raw JSON. "
                f"No markdown. No code fences. No backticks.' "
                f"Also use extract_json() utility before json.loads()."
            )

        # Low hallucination score
        if hallucination < 8:
            recommendations.append(
                f"[CRIT] [{name}] Low hallucination score ({hallucination}/10). "
                f"Add to system prompt: 'If you are unsure, say "
                f"I don't know rather than guessing.'"
            )

        # General low score
        if score < 7:
            recommendations.append(
                f"[FAIL] [{name}] Failed with {score}/10. "
                f"Review prompt design and expected_behavior definition. "
                f"Consider adding few-shot examples for this test category."
            )

        # High token usage warning
        if tokens_used > 500:
            recommendations.append(
                f"[COST] [{name}] High token usage ({tokens_used} tokens). "
                f"Consider shortening system prompt or reducing max_tokens "
                f"to optimize cost at scale."
            )

    # If everything passed with high scores
    if not recommendations:
        recommendations.append(
            "[OK] All tests passed with high scores. "
            "Consider adding more edge case tests to stress-test the model. "
            "Try adversarial prompts, multilingual inputs, or very long contexts."
        )

    return recommendations


# ─────────────────────────────────────────────
# MAIN: Generate the report
# ─────────────────────────────────────────────

def generate_report(evaluation_file):
    """
    Load evaluation results and generate full human-readable report.

    Report sections:
        1. Header (run metadata)
        2. Executive Summary (the TL;DR)
        3. Per-Test Detailed Results
        4. Score Comparison Table
        5. Cost Analysis
        6. Recommendations
        7. Footer

    Args:
        evaluation_file (str): Path to evaluation JSON from evaluator.py

    Returns:
        str: The complete report as a string
    """

    # ── Load evaluation data ─────────────────────────────────────────
    if not os.path.exists(evaluation_file):
        print(f"[ERROR] File not found: {evaluation_file}")
        print("   Run evaluator.py first.")
        return None

    with open(evaluation_file, "r") as f:
        data = json.load(f)

    summary           = data.get("summary", {})
    evaluated_results = data.get("evaluated_results", [])

    # ── Build report lines ───────────────────────────────────────────
    lines = []
    sep   = "=" * 65
    thin  = "-" * 65

    # ── SECTION 1: Header ────────────────────────────────────────────
    lines += [
        sep,
        "  LLM EVALUATION REPORT",
        "  Project: LLM Evaluation Tester (Project 1)",
        "  Author:  Ankur Sharma",
        sep,
        f"  Generated     : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"  Source file   : {evaluation_file}",
        f"  Model tested  : {summary.get('evaluator_model', 'N/A')}",
        f"  Pass threshold: {summary.get('pass_threshold', 7.0)}/10",
        sep,
        ""
    ]

    # ── SECTION 2: Executive Summary ─────────────────────────────────
    passed     = summary.get("passed", 0)
    failed     = summary.get("failed", 0)
    total      = summary.get("total_evaluated", 0)
    pass_rate  = summary.get("pass_rate_pct", 0)
    avg_score  = summary.get("avg_overall_score", 0)
    grade      = score_to_grade(avg_score)

    # Overall status banner
    if pass_rate == 100:
        status_banner = "*** ALL TESTS PASSED - PRODUCTION READY ***"
    elif pass_rate >= 80:
        status_banner = ">>> MOSTLY PASSING - MINOR ISSUES TO ADDRESS"
    elif pass_rate >= 60:
        status_banner = "!!! PARTIAL PASS - SIGNIFICANT ISSUES FOUND"
    else:
        status_banner = "XXX FAILING - DO NOT SHIP - REVIEW REQUIRED"

    lines += [
        "EXECUTIVE SUMMARY",
        thin,
        f"  Status    : {status_banner}",
        f"  Pass Rate : {pass_rate}%  ({passed}/{total} tests passed)",
        f"  Avg Score : {score_to_bar(avg_score)}",
        f"  Grade     : {grade}",
        ""
    ]

    # ── SECTION 3: Per-Test Detailed Results ─────────────────────────
    lines += [
        sep,
        "DETAILED TEST RESULTS",
        sep,
        ""
    ]

    total_prompt_tokens     = 0
    total_completion_tokens = 0

    for i, result in enumerate(evaluated_results, 1):
        ev       = result.get("evaluation", {})
        name     = result.get("test_name", "Unknown")
        test_id  = result.get("test_id", "N/A")
        category = result.get("category", "N/A").upper()
        passed_t = ev.get("pass", False)

        # Token tracking
        token_usage    = result.get("token_usage", {})
        prompt_tok     = token_usage.get("prompt_tokens", 0)
        completion_tok = token_usage.get("completion_tokens", 0)
        total_prompt_tokens     += prompt_tok
        total_completion_tokens += completion_tok

        lines += [
            f"TEST {i}: {name}",
            thin,
            f"  ID       : {test_id}",
            f"  Category : {category}",
            f"  Verdict  : {verdict_icon(passed_t)}",
            ""
        ]

        if ev.get("status") == "success":
            o_score   = ev.get("overall_score", 0)
            acc       = ev.get("accuracy", 0)
            fmt       = ev.get("format_compliance", 0)
            rel       = ev.get("relevance", 0)
            hal       = ev.get("hallucination_score", 0)
            reasoning = ev.get("reasoning", "N/A")
            issues    = ev.get("issues_found", [])

            lines += [
                f"  SCORES:",
                f"",
                f"    Overall           {score_to_bar(o_score)}",
                f"",
                f"    Accuracy          {score_to_bar(acc)}",
                f"",
                f"    Format Compliance {score_to_bar(fmt)}",
                f"",
                f"    Relevance         {score_to_bar(rel)}",
                f"",
                f"    Hallucination     {score_to_bar(hal)}",
                f"",
                f"  Reasoning : {reasoning}",
            ]

            if issues:
                lines.append(f"  Issues    : {' | '.join(issues)}")

            lines += [
                f"  Tokens    : {token_usage.get('total_tokens', 0)} "
                f"(prompt: {prompt_tok}, completion: {completion_tok})",
                ""
            ]

            lines += [
                f"  PROMPT PREVIEW:",
                f"    {result.get('user_prompt', '')[:100]}...",
                "",
                f"  RESPONSE PREVIEW:",
                f"    {result.get('ai_response', '')[:150]}...",
                ""
            ]

        else:
            lines += [
                f"  ERROR: {ev.get('error', ev.get('reasoning', 'Unknown error'))}",
                ""
            ]

        lines.append(sep)
        lines.append("")

    # ── SECTION 4: Score Comparison Table ────────────────────────────
    lines += [
        "SCORE COMPARISON TABLE",
        thin,
        f"  {'Test':<42} {'Score':>7}  {'Grade':<22} {'Result':>10}",
        f"  {'-'*42} {'-'*7}  {'-'*22} {'-'*10}",
    ]

    for result in evaluated_results:
        ev    = result.get("evaluation", {})
        name  = result.get("test_name", "Unknown")[:41]
        score = ev.get("overall_score", 0)
        grade = score_to_grade(score)[:21]
        verd  = verdict_icon(ev.get("pass", False))
        lines.append(f"  {name:<42} {score:>6.1f}  {grade:<22} {verd:>10}")

    lines += ["", sep, ""]

    # ── SECTION 5: Cost Analysis ──────────────────────────────────────
    test_cost   = calculate_cost(total_prompt_tokens, total_completion_tokens)
    eval_tokens = summary.get("eval_tokens_used", 0)
    eval_cost   = calculate_cost(
        int(eval_tokens * 0.6),
        int(eval_tokens * 0.4)
    )
    total_cost  = round(test_cost + eval_cost, 6)

    cost_100   = round(total_cost * 100, 4)
    cost_1000  = round(total_cost * 1000, 4)
    cost_10000 = round(total_cost * 10000, 2)

    lines += [
        "COST ANALYSIS  (GPT-4o-mini pricing reference)",
        thin,
        f"  Test run tokens       : {total_prompt_tokens + total_completion_tokens:,}",
        f"  Evaluation tokens     : {eval_tokens:,}",
        f"  Total tokens          : {total_prompt_tokens + total_completion_tokens + eval_tokens:,}",
        "",
        f"  Cost this run         : ${total_cost:.6f}",
        f"  Cost per 100 runs     : ${cost_100:.4f}",
        f"  Cost per 1,000 runs   : ${cost_1000:.4f}",
        f"  Cost per 10,000 runs  : ${cost_10000:.2f}",
        "",
        f"  NOTE: Actual cost on Groq = $0.00 (free tier)",
        f"        Above figures show production cost if using OpenAI.",
        f"        Use this for ROI discussions with stakeholders.",
        "",
        sep,
        ""
    ]

    # ── SECTION 6: Recommendations ───────────────────────────────────
    recommendations = generate_recommendations(evaluated_results)

    lines += [
        "RECOMMENDATIONS",
        thin,
        ""
    ]

    for rec in recommendations:
        words        = rec.split()
        current_line = "  "
        for word in words:
            if len(current_line) + len(word) + 1 > 63:
                lines.append(current_line)
                current_line = "  " + word + " "
            else:
                current_line += word + " "
        if current_line.strip():
            lines.append(current_line)
        lines.append("")

    lines += [sep, ""]

    # ── SECTION 7: Footer ────────────────────────────────────────────
    lines += [
        "NEXT STEPS",
        thin,
        "  1. Fix flagged issues (see Recommendations above)",
        "  2. Add more test cases (aim for 20+ covering edge cases)",
        "  3. Run evaluation again to measure improvement",
        "  4. Compare scores across different models",
        "  5. Add this report to your GitHub README as proof of quality",
        "",
        sep,
        "  End of Report",
        f"  Generated by LLM Evaluation Tester | Ankur Sharma | {datetime.now().year}",
        sep
    ]

    report = "\n".join(lines)
    return report


# ─────────────────────────────────────────────
# SAVE AND DISPLAY
# ─────────────────────────────────────────────

def save_and_display_report(evaluation_file):
    """
    Generate, display, and save the report.

    Args:
        evaluation_file (str): Path to evaluation JSON

    Returns:
        str: Path to saved report file
    """
    report = generate_report(evaluation_file)

    if not report:
        return None

    print(report)

    os.makedirs(REPORT_DIR, exist_ok=True)
    report_file = os.path.join(
        REPORT_DIR,
        f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    )

    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\n>> Report saved to: {report_file}")
    print("   -> Add this to your GitHub README as a screenshot!")
    print("   -> This is your portfolio proof of quality.")

    return report_file


# ─────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────

if __name__ == "__main__":

    results_dir = "test_results"

    if not os.path.exists(results_dir):
        print("[ERROR] No test_results folder found.")
        print("        Run test_runner.py then evaluator.py first.")
    else:
        eval_files = sorted([
            f for f in os.listdir(results_dir)
            if f.startswith("evaluation_") and f.endswith(".json")
        ])

        if not eval_files:
            print("[ERROR] No evaluation files found.")
            print("        Run evaluator.py first.")
        else:
            latest = os.path.join(results_dir, eval_files[-1])
            print(f">> Using latest evaluation: {latest}\n")
            save_and_display_report(latest)
