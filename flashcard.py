#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import random
import time
import datetime
import string
from typing import Any, Dict, List, Optional, Tuple

try:
    import yaml
except ImportError:
    print("Missing dependency: pyyaml\nInstall with: pip install pyyaml")
    sys.exit(1)

# -----------------------
# Config
# -----------------------

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
SUPPORTED_EXTS = (".yml", ".yaml")

# Quiz modes
MODE_Q_TO_TERM = 1      # use quiz_question -> expect term
MODE_TERM_TO_DEF = 2    # show term -> reveal full_def
MODE_MIXED = 3          # random mix


# -----------------------
# Obfuscated + plain logging
# -----------------------

def obfuscate_line(s: str) -> str:
    """
    Obfuscate a line by:
      1) inserting a random lowercase letter AFTER EVERY ORIGINAL CHARACTER
         Example: "ABCD" -> "AxByCzDq" (random letters after each original char)
      2) incrementing each char's codepoint by 7 (mod 255)
    Returns a readable obfuscated string.
    """
    letters = string.ascii_lowercase
    expanded = []
    for ch in s:
        expanded.append(ch)
        expanded.append(random.choice(letters))
    joined = "".join(expanded)

    obfus_chars = []
    for ch in joined:
        code = ord(ch)
        obfus_code = (code + 7) % 255
        obfus_chars.append(chr(obfus_code))
    return "".join(obfus_chars)


def log_answer(deck_title: str, mode: str, term: str, user_ans: str, correct: bool) -> None:
    """
    Append a plain log line to data/answers.log and an obfuscated line to data/stamp.log.
    Plain line format (tab-separated):
      YYYY-MM-DD HH:MM:SS    <deck_title>    <mode>    <term>    <user_ans>    <0|1>
    """
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{ts}\t{deck_title}\t{mode}\t{term}\t{user_ans}\t{int(correct)}"

    os.makedirs(DATA_DIR, exist_ok=True)
    plain_path = os.path.join(DATA_DIR, "answers.log")
    obfus_path = os.path.join(DATA_DIR, "stamp.log")

    # plain (UTF-8 text)
    with open(plain_path, "a", encoding="utf-8") as f:
        f.write(line + "\n")

    # obfuscated (readable text with per-line obfuscation)
    with open(obfus_path, "a", encoding="utf-8") as f:
        f.write(obfuscate_line(line) + "\n")


# -----------------------
# Deck loading
# -----------------------

def discover_deck_files(data_dir: str) -> List[str]:
    """Return a sorted list of YAML deck file paths from data/."""
    if not os.path.isdir(data_dir):
        return []
    files = [
        os.path.join(data_dir, fn)
        for fn in os.listdir(data_dir)
        if fn.lower().endswith(SUPPORTED_EXTS)
    ]
    files.sort(key=lambda p: os.path.basename(p).lower())
    return files


def _normalize_deck_from_data(data: Any, filename: str) -> Dict[str, Any]:
    """
    Normalize a loaded YAML structure into:
      {"title": str, "cards": [ {term, full_def, quiz_question?}, ... ], "source_file": str}
    Supports both:
      - new style: {title: "...", cards: [...]}
      - old style: [...] (list of cards only)
    """
    base_title = os.path.splitext(os.path.basename(filename))[0]
    if data is None:
        return {"title": base_title, "cards": [], "source_file": filename}

    if isinstance(data, dict) and "cards" in data and isinstance(data["cards"], list):
        title = data.get("title") or base_title
        cards = [coerce_card(c) for c in data["cards"]]
        return {"title": title, "cards": cards, "source_file": filename}

    if isinstance(data, list):
        cards = [coerce_card(c) for c in data]
        return {"title": base_title, "cards": cards, "source_file": filename}

    # Fallback
    return {"title": base_title, "cards": [], "source_file": filename}


def coerce_card(raw: Any) -> Dict[str, str]:
    """Ensure each card has term/full_def/quiz_question keys (graceful defaults)."""
    if not isinstance(raw, dict):
        return {"term": str(raw), "full_def": "", "quiz_question": ""}
    term = str(raw.get("term", "")).strip()
    full_def = str(raw.get("full_def", "")).strip()
    quiz_q = str(raw.get("quiz_question", "")).strip()
    return {"term": term, "full_def": full_def, "quiz_question": quiz_q}


def load_deck(filepath: str) -> Optional[Dict[str, Any]]:
    """Load one deck file safely."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return _normalize_deck_from_data(data, filepath)
    except FileNotFoundError:
        print(f"[!] File not found: {filepath}")
        return None
    except yaml.YAMLError as e:
        print(f"[!] YAML parse error in {filepath}:\n{e}")
        return None


# -----------------------
# UI helpers
# -----------------------

def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def wait_key(prompt="Press Enter to continue...") -> None:
    try:
        input(prompt)
    except EOFError:
        pass


def ask_int(prompt: str, lo: int, hi: int) -> int:
    while True:
        try:
            s = input(prompt).strip()
            val = int(s)
            if lo <= val <= hi:
                return val
        except ValueError:
            pass
        print(f"Please enter a number from {lo} to {hi}.")


def ask_yes_no(prompt: str) -> bool:
    """
    Ask a y/n question and re-prompt until a valid answer is given.
    Returns True for 'y', False for 'n'.
    """
    while True:
        s = input(prompt).strip().lower()
        if s in ("y", "yes"):
            return True
        if s in ("n", "no"):
            return False
        print("Please answer with 'y' or 'n'.")


# -----------------------
# Menus
# -----------------------

def choose_deck(decks: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    clear_screen()
    if not decks:
        print("No decks found in ./data")
        return None

    print("Select a subject:\n")
    for i, d in enumerate(decks, start=1):
        count = len(d["cards"])
        fn = os.path.basename(d["source_file"])
        print(f"  {i}. {d['title']}  ({count} cards)  [{fn}]")
    print()
    idx = ask_int("Enter choice: ", 1, len(decks))
    return decks[idx - 1]


def choose_mode() -> int:
    clear_screen()
    print("Choose quiz mode:\n")
    print(f"  {MODE_Q_TO_TERM}. Question -> Term   (uses 'quiz_question', expects the term)")
    print(f"  {MODE_TERM_TO_DEF}. Term -> Definition  (show term, reveal definition)")
    print(f"  {MODE_MIXED}. Mixed")
    print()
    return ask_int("Enter choice: ", MODE_Q_TO_TERM, MODE_MIXED)


def choose_count(max_n: int) -> int:
    clear_screen()
    print(f"How many cards? (1..{max_n})")
    print("Tip: press Enter for all.")
    s = input("Enter number: ").strip()
    if not s:
        return max_n
    try:
        n = int(s)
        n = max(1, min(max_n, n))
        return n
    except ValueError:
        return max_n


# -----------------------
# Quiz logic
# -----------------------

def normalize_answer(s: str) -> str:
    return " ".join(s.lower().split())


def mode_name(mode: int) -> str:
    return {
        MODE_Q_TO_TERM: "Question -> Term",
        MODE_TERM_TO_DEF: "Term -> Definition",
        MODE_MIXED: "Mixed",
    }.get(mode, "Unknown")


def run_quiz(deck: Dict[str, Any], mode: int) -> None:
    cards = [c for c in deck["cards"] if c.get("term")]
    if not cards:
        print("This deck has no cards.")
        return

    random.shuffle(cards)
    n = choose_count(len(cards))
    cards = cards[:n]

    correct = 0
    wrong: List[Tuple[Dict[str, str], str]] = []  # (card, user_answer)

    start = time.time()
    clear_screen()
    print(f"--- {deck['title']} ---")
    print(f"Mode: {mode_name(mode)} | Cards: {len(cards)}")
    print("Type 'q' to quit the quiz.\n")

    for idx, card in enumerate(cards, start=1):
        this_mode = mode
        if mode == MODE_MIXED:
            this_mode = random.choice([MODE_Q_TO_TERM, MODE_TERM_TO_DEF])

        print(f"[{idx}/{len(cards)}]")

        if this_mode == MODE_Q_TO_TERM:
            prompt = card.get("quiz_question") or f"Which term fits: {card.get('full_def', '').strip()}"
            if not prompt:
                prompt = f"Name the term for: {card.get('term', '')}"
            print(prompt)
            ans = input("> ").strip()
            if ans.lower() == "q":
                break
            is_correct = normalize_answer(ans) == normalize_answer(card["term"])
            if is_correct:
                print("✓ Correct!")
                correct += 1
            else:
                print(f"✗ Incorrect. Answer: {card['term']}")
                if card.get("full_def"):
                    print(f"   Def: {card['full_def']}")
                wrong.append((card, ans))
            # log answer (plain + obfuscated)
            log_answer(deck["title"], mode_name(this_mode), card["term"], ans, is_correct)
            print()

        elif this_mode == MODE_TERM_TO_DEF:
            term = card["term"]
            print(f"Term: {term}")
            _ = input("(Press Enter to reveal definition or type 'q' to quit) ")
            if _.strip().lower() == "q":
                break
            full_def = card.get("full_def", "").strip()
            if full_def:
                print(f"Definition: {full_def}")
            else:
                print("(No definition provided in this card.)")

            # self-assessment with validated y/n
            knew_it = ask_yes_no("Did you know it? (y/n): ")
            is_correct = knew_it
            if is_correct:
                correct += 1
                user_ans = "(knew)"
            else:
                wrong.append((card, ""))  # no explicit user answer here
                user_ans = "(unknown)"

            # log answer (plain + obfuscated)
            log_answer(deck["title"], mode_name(this_mode), card["term"], user_ans, is_correct)
            print()

        else:
            print("Internal error: unknown mode.")
            break

    elapsed = time.time() - start
    total = len(cards)
    print("\n--- Results ---")
    print(f"Score: {correct}/{total}  ({(100.0*correct/total if total else 0):.1f}%)")
    print(f"Time:  {elapsed:.1f}s")

    if wrong:
        print("\nYou missed these:")
        for card, user_ans in wrong:
            term = card["term"]
            qa = card.get("quiz_question", "")
            print(f"- Term: {term}")
            if qa:
                print(f"  Q : {qa}")
            if user_ans:
                print(f"  Your answer: {user_ans}")
            if card.get("full_def"):
                print(f"  Def: {card['full_def']}")
        print()

    wait_key()


# -----------------------
# Main
# -----------------------

def main() -> None:
    deck_files = discover_deck_files(DATA_DIR)
    decks: List[Dict[str, Any]] = []
    for path in deck_files:
        d = load_deck(path)
        if d:
            decks.append(d)

    if not decks:
        print(f"No YAML decks found in {DATA_DIR}")
        sys.exit(1)

    while True:
        deck = choose_deck(decks)
        if deck is None:
            return
        mode = choose_mode()
        run_quiz(deck, mode)

        print()
        again = ask_yes_no("Study another deck? (y/n): ")
        if not again:
            break

    print("Good luck! See you next time.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted. Bye!")
