#!/usr/bin/env python3
"""List words that repeat within a sentence or in two adjacent sentences.

Usage: check_repeats.py text.ru.md

Two kinds of repeats are reported:
- a stem: the first 5 letters of a word of 5+ letters, skipping frequent
  function words: «вопрос… вопросом», «часто… слишком часто»;
- a word pair of 7+ letters, function words included: «для этого… Для этого».

The stem is a crude prefix, not a dictionary lemma, so the output is a list
of places to look at, not a list of errors. The exit code is always 0.
"""
import re
import sys

STEM = 5
PAIR = 7
WORD_RE = re.compile(r"[а-яёА-ЯЁa-zA-Z]+")
SENT_RE = re.compile(r"(?<=[.!?…»])\s+|\n+")
# Link and image targets, bare URLs.
LINK_RE = re.compile(r"\]\([^)]*\)|<?https?://\S+>?")
# Frequent long function words that repeat harmlessly.
SKIP = set(
    "потому чтобы когда который которая которое которые которых которым "
    "которой этого этому этими своей своего своих своим может можно "
    "только тоже также более очень между после перед через всего всегда "
    "сейчас здесь потом теперь будет будут нужно".split()
)


def paragraphs(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    return [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]


def keys(sentence):
    """Stems and word pairs of a sentence, with their counts."""
    words = [w.lower() for w in WORD_RE.findall(LINK_RE.sub("]", sentence))]
    found = [w[:STEM] + "…" for w in words if len(w) >= STEM and w not in SKIP]
    found += [f"{a} {b}" for a, b in zip(words, words[1:])
              if len(a) + len(b) >= PAIR]
    return found


def repeats(paras):
    """Yield (paragraph index, repeated keys, sentences) for each hit."""
    sentences = [(i, s) for i, p in enumerate(paras)
                 for s in SENT_RE.split(p) if s.strip()]
    for n, (i, s) in enumerate(sentences):
        own = keys(s)
        inside = {k for k in own if own.count(k) > 1}
        if inside:
            yield i, inside, [s]
        if n + 1 < len(sentences):
            j, t = sentences[n + 1]
            across = set(own) & set(keys(t))
            if across:
                yield j, across, [s, t]


def repeated_keys(paras):
    return {k for _, found, _ in repeats(paras) for k in found}


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__.strip().splitlines()[2])
    for i, found, sents in repeats(paragraphs(sys.argv[1])):
        print(f"абзац {i + 1}: {', '.join(sorted(found))}")
        for s in sents:
            print(f"  — {s.strip()}")


if __name__ == "__main__":
    main()
