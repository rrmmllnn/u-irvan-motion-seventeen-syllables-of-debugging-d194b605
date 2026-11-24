"""Seventeen Syllables of Debugging.

Writes a 5-7-5 haiku about a debugging session to
$MAKEFUN_OUTPUT_DIR/entry.txt, terminated by a newline.
"""

import os
import sys

FIRST_LINE = "Cursor blinks at three"
SECOND_LINE = "the log line stops mid-sentence"
THIRD_LINE = "and I am the bug"

SYLLABLES_PER_LINE = (5, 7, 5)


def count_syllables(line):
    """Estimate syllables from vowel clusters in each word."""
    running = 0
    vowel_set = set("aeiou")
    for token in line.casefold().split():
        clusters = 0
        inside = False
        for letter in token:
            hit = letter in vowel_set
            if hit and not inside:
                clusters += 1
            inside = hit
        if token.endswith("e") and clusters > 1:
            clusters -= 1
        running += clusters if clusters > 0 else 1
    return running


def build_haiku():
    verses = (FIRST_LINE, SECOND_LINE, THIRD_LINE)
    for verse, wanted in zip(verses, SYLLABLES_PER_LINE):
        found = count_syllables(verse)
        if found != wanted:
            sys.exit("syllable mismatch in %r: found %d, expected %d" % (verse, found, wanted))
    joined = "\n".join(verses)
    if not 1 <= len(joined) <= 200:
        sys.exit("haiku length out of range: %d chars" % len(joined))
    return joined


def main():
    destination = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(destination, exist_ok=True)
    poem = build_haiku()
    target = os.path.join(destination, "entry.txt")
    with open(target, "w", encoding="utf-8", newline="") as sink:
        sink.write(poem + "\n")


if __name__ == "__main__":
    main()
