#!/usr/bin/env python3
"""Generate MAGiE encode-puzzle candidates (clue + winMessage) for answer words.

Usage:
  python generate.py --word MALLOWANCE
  python generate.py --word "MALL AFTER SCHOOL?" -n 5 --context "Scene: Mall Jail."
  python generate.py --from-bank AnswerBank1.md --limit 10 --out batch1.json

Requires: pip install anthropic
          export ANTHROPIC_API_KEY=...
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

MAX_LINE_LEN = 24
DEFAULT_MODEL = "claude-sonnet-4-6"

USER_TEMPLATE = """ANSWER: {win_text}

Write {n} candidate puzzles for this answer.

The clue must make ANSWER the single obvious completion. Assume the player
knows the mall world but is not looking at any other puzzle.
{context_block}"""


# ---------- validation ----------

def validate_candidate(cand: dict, win_text: str) -> list[str]:
    """Return a list of problems. Empty list == valid."""
    problems = []
    if not isinstance(cand, dict):
        return ["candidate is not an object"]

    for field in ("puzzleName", "clue", "winMessage"):
        if field not in cand:
            problems.append(f"missing field: {field}")
    if problems:
        return problems

    if not isinstance(cand["puzzleName"], str) or not cand["puzzleName"].strip():
        problems.append("puzzleName empty or not a string")

    for field in ("clue", "winMessage"):
        lines = cand[field]
        if not isinstance(lines, list) or not lines:
            problems.append(f"{field} empty or not a list")
            continue
        for i, line in enumerate(lines):
            if not isinstance(line, str):
                problems.append(f"{field}[{i}] not a string")
            elif len(line) > MAX_LINE_LEN:
                problems.append(f"{field}[{i}] too long ({len(line)} > {MAX_LINE_LEN}): {line!r}")

    # Answer must not leak into the clue text.
    if isinstance(cand.get("clue"), list):
        clue_blob = " ".join(str(l) for l in cand["clue"]).upper()
        core = win_text.upper().strip(" ?!.")
        if core and core in clue_blob:
            problems.append(f"answer {core!r} appears in clue")

    return problems


# ---------- generation ----------

def parse_response_json(text: str):
    """Model is told 'no fences', but strip them defensively."""
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("```")[1]
        if cleaned.startswith("json"):
            cleaned = cleaned[4:]
    return json.loads(cleaned)


def generate_for_word(client, model: str, system_prompt: str,
                      win_text: str, n: int, context: str) -> dict:
    context_block = f"\n{context}\n" if context else ""
    user_msg = USER_TEMPLATE.format(win_text=win_text.upper(), n=n,
                                    context_block=context_block)

    message = client.messages.create(
        model=model,
        max_tokens=2000,
        system=system_prompt,
        messages=[{"role": "user", "content": user_msg}],
    )
    raw = "".join(block.text for block in message.content
                  if getattr(block, "type", None) == "text")

    result = {
        "winText": win_text.upper(),
        "type": "Encode",
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "model": model,
        "candidates": [],
        "rejected": [],
    }

    try:
        candidates = parse_response_json(raw)
    except (json.JSONDecodeError, IndexError) as e:
        result["rejected"].append({"reason": f"response not valid JSON: {e}",
                                   "raw": raw})
        return result

    if not isinstance(candidates, list):
        candidates = [candidates]

    for cand in candidates:
        problems = validate_candidate(cand, win_text)
        if problems:
            result["rejected"].append({"candidate": cand, "problems": problems})
        else:
            result["candidates"].append(cand)

    return result


# ---------- answer bank ----------

def load_answer_bank(path: Path) -> list[str]:
    words = []
    for line in path.read_text().splitlines():
        word = line.strip()
        if word and not word.startswith("#"):
            words.append(word)
    return words


# ---------- main ----------

def main():
    ap = argparse.ArgumentParser(description="Generate MAGiE encode-puzzle candidates.")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--word", help="single answer word/phrase")
    src.add_argument("--from-bank", type=Path, metavar="FILE",
                     help="answer bank file, one word per line")
    ap.add_argument("--limit", type=int, default=None,
                    help="max words to process from the bank")
    ap.add_argument("--skip", type=int, default=0,
                    help="skip the first N bank words (resume a batch)")
    ap.add_argument("-n", "--candidates", type=int, default=3,
                    help="candidates per word (default 3)")
    ap.add_argument("--context", default="",
                    help="optional scene context sentence(s)")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--prompt", type=Path,
                    default=Path(__file__).parent / "prompt_system.md")
    ap.add_argument("--out", type=Path, default=Path("candidates.json"))
    args = ap.parse_args()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("ANTHROPIC_API_KEY is not set.")

    try:
        from anthropic import Anthropic
    except ImportError:
        sys.exit("anthropic package not installed: pip install anthropic")

    system_prompt = args.prompt.read_text()
    client = Anthropic()

    if args.word:
        words = [args.word]
    else:
        words = load_answer_bank(args.from_bank)[args.skip:]
        if args.limit:
            words = words[: args.limit]

    results = []
    for i, word in enumerate(words, 1):
        print(f"[{i}/{len(words)}] {word} ... ", end="", flush=True)
        try:
            r = generate_for_word(client, args.model, system_prompt,
                                  word, args.candidates, args.context)
        except Exception as e:  # API errors: report and keep going
            print(f"ERROR: {e}")
            results.append({"winText": word.upper(), "error": str(e)})
            continue
        print(f"{len(r['candidates'])} ok, {len(r['rejected'])} rejected")
        results.append(r)

    args.out.write_text(json.dumps(results, indent=2) + "\n")
    total_ok = sum(len(r.get("candidates", [])) for r in results)
    total_rej = sum(len(r.get("rejected", [])) for r in results)
    print(f"\nWrote {args.out}: {total_ok} candidates, {total_rej} rejected, "
          f"{len(results)} words.")


if __name__ == "__main__":
    main()
