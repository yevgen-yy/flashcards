#!/usr/bin/env python3
"""
bio_practice.py — CLI drill app for Biology Unit 1 (self‑validation style).

Usage:
  Run this script from the same folder as `bio_practice.yml`.
  The app will ask if you want questions in random order.
  For multi‑part questions, you'll be prompted 1., 2., ... sequentially.
  After you see the model answers, confirm if you were correct (y/n).

Dependencies:
  pip install pyyaml
"""

from __future__ import annotations
import sys
import random
from pathlib import Path
from typing import Any, Dict, List

try:
    import yaml  # PyYAML
except ImportError as e:
    sys.stderr.write("ERROR: PyYAML is not installed. Try: pip install pyyaml\n")
    sys.exit(1)


DATA_FILENAME = "bio_practice.yml"


def yn_prompt(prompt: str) -> bool:
    """Ask a yes/no question; loop until a valid answer is given.
    Returns True for yes, False for no.
    """
    while True:
        ans = input(prompt).strip().lower()
        if ans in ("y", "yes"):
            return True
        if ans in ("n", "no"):
            return False
        print("Please answer 'y' or 'n'.")


def press_enter(msg: str = "Press Enter to reveal the model answer...") -> None:
    try:
        input(msg)
    except EOFError:
        pass


def load_questions(path: Path) -> Dict[str, Any]:
    if not path.exists():
        sys.stderr.write(f"ERROR: Could not find data file: {path}\n")
        sys.stderr.write("Make sure bio_practice.yml is in the same folder as this script.\n")
        sys.exit(1)
    try:
        with path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            if not isinstance(data, dict) or "questions" not in data:
                raise ValueError("YAML must contain a top-level 'questions' list")
            if not isinstance(data["questions"], list):
                raise ValueError("'questions' must be a list")
            return data
    except Exception as e:
        sys.stderr.write(f"ERROR: Failed to read/parse YAML: {e}\n")
        sys.exit(1)


def ask_question(q: Dict[str, Any]) -> bool:
    qid = q.get("id", "<no-id>")
    prompt = q.get("prompt", "<no-prompt>")
    qtype = q.get("type", "short").lower()
    answers: List[str] = q.get("answers", [])
    parts = q.get("parts")

    print("=" * 72)
    print(f"Q: {prompt}")
    print("-" * 72)

    # Collect user input (not auto-graded; purely for pacing)
    if qtype == "short":
        _ = input("> ")
    elif qtype in ("list", "sequence"):
        if parts is None:
            # If not provided, default to number of model answers (if available)
            parts = len(answers) if answers else 3
        for i in range(1, int(parts) + 1):
            _ = input(f"{i}. ")
    else:
        # Fallback as short
        _ = input("> ")

    press_enter()

    # Show model answers
    if answers:
        print("Model answer(s):")
        for i, ans in enumerate(answers, 1):
            print(f"  {i}. {ans}")
    else:
        print("Model answer(s): (none provided)")

    # Self-validation
    correct = yn_prompt("Did you answer correctly (y/n)? ")
    return correct


def main() -> None:
    script_dir = Path(__file__).resolve().parent
    data_path = script_dir / DATA_FILENAME

    data = load_questions(data_path)
    questions: List[Dict[str, Any]] = data["questions"]

    # Order choice
    print("Biology Unit 1 Practice — self-validation")
    random_choice = yn_prompt("Practice in random order? (y/n): ")
    indices = list(range(len(questions)))
    if random_choice:
        random.shuffle(indices)

    total = len(indices)
    correct_count = 0
    missed: List[Dict[str, Any]] = []

    for idx, qi in enumerate(indices, 1):
        q = questions[qi]
        print(f"\n[ {idx} / {total} ]  id={q.get('id','<no-id>')}")
        is_correct = ask_question(q)
        if is_correct:
            correct_count += 1
        else:
            missed.append(q)

    print("\n" + "=" * 72)
    print("SESSION SUMMARY")
    print("-" * 72)
    print(f"Score: {correct_count} / {total}  ({(100.0*correct_count/total):.1f}%)")
    if missed:
        print("\nMissed questions:")
        for q in missed:
            print(f" - {q.get('id', '<no-id>')}: {q.get('prompt', '<no-prompt>')}")
    print("=" * 72)
    print("Done. Good work!")

if __name__ == "__main__":
    main()
