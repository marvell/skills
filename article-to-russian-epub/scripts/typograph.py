#!/usr/bin/env python3
"""Insert non-breaking spaces into Russian Markdown.

Usage: typograph.py < input.md > output.md

- after short prepositions, conjunctions and particles: «в доме», «и вот»;
- before an em dash: «слово —»;
- between a number and the following word: «15 минут».
Fenced code, inline code, link targets and URLs are left untouched.
The transformation is idempotent.
"""
import re
import sys

NBSP = " "
SHORT = (
    "а без в во да для до же за и из к ко ли на над не ни но о об обо "
    "от по под при про с со у"
).split()
SHORT_RE = re.compile(
    r"(?<![\w-])(" + "|".join(SHORT) + r") (?=\S)", re.IGNORECASE
)
DASH_RE = re.compile(r"(?<=\S) (?=—)")
NUM_RE = re.compile(r"(?<=\d) (?=[а-яёА-ЯЁ])")
# Inline code, link/image targets, bare URLs.
PROTECT_RE = re.compile(r"`[^`]*`|\]\([^)]*\)|<?https?://\S+>?")


def fix_text(text: str) -> str:
    text = SHORT_RE.sub(lambda m: m.group(1) + NBSP, text)
    text = DASH_RE.sub(NBSP, text)
    return NUM_RE.sub(NBSP, text)


def fix_line(line: str) -> str:
    out, pos = [], 0
    for m in PROTECT_RE.finditer(line):
        out.append(fix_text(line[pos:m.start()]))
        out.append(m.group(0))
        pos = m.end()
    out.append(fix_text(line[pos:]))
    return "".join(out)


def main() -> None:
    in_code = False
    for line in sys.stdin:
        if line.lstrip().startswith("```"):
            in_code = not in_code
            sys.stdout.write(line)
            continue
        sys.stdout.write(line if in_code else fix_line(line))


if __name__ == "__main__":
    main()
