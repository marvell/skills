#!/usr/bin/env python3
"""Show every edited paragraph of a Markdown text in context.

Usage: changed_context.py before.ru.md after.ru.md > changes.md

Paragraphs are blocks separated by blank lines. For each edit the output
gives the neighbouring paragraph before it, the paragraph as it was and as
it became, and the neighbouring paragraph after it. Neighbours come from
the new text.

Under each edit, «Повторы» lists repeats that the edit introduced: found by
check_repeats.py in the new paragraphs and their neighbours, but not in the
old ones. The list is a hint, not a verdict.
"""
import difflib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_repeats import paragraphs, repeated_keys  # noqa: E402


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__.strip().splitlines()[2])
    old, new = paragraphs(sys.argv[1]), paragraphs(sys.argv[2])
    ops = [op for op in difflib.SequenceMatcher(None, old, new, autojunk=False)
           .get_opcodes() if op[0] != "equal"]
    if not ops:
        print("Изменений нет.")
        return
    out = []
    for n, (_, i1, i2, j1, j2) in enumerate(ops, 1):
        prev_p = new[j1 - 1] if j1 > 0 else None
        next_p = new[j2] if j2 < len(new) else None
        where = (f"абзац {j1 + 1}" if j2 - j1 <= 1
                 else f"абзацы {j1 + 1}–{j2}")
        out.append(f"## Правка {n} ({where} нового текста)\n")
        if prev_p:
            out.append(f"**Перед:**\n\n{prev_p}\n")
        out.append("**Было:**\n\n" + ("\n\n".join(old[i1:i2]) or "(нет)") + "\n")
        out.append("**Стало:**\n\n" + ("\n\n".join(new[j1:j2]) or "(удалено)") + "\n")
        if next_p:
            out.append(f"**После:**\n\n{next_p}\n")
        head = [prev_p] if prev_p else []
        tail = [next_p] if next_p else []
        fresh = sorted(repeated_keys(head + new[j1:j2] + tail)
                       - repeated_keys(head + old[i1:i2] + tail))
        if fresh:
            out.append("**Повторы:** " + ", ".join(fresh) + "\n")
        out.append("---\n")
    print("\n".join(out))


if __name__ == "__main__":
    main()
