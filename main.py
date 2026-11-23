"""One-line pitch entry for make.fun's "A Day of One-Line Pitches".

Reads the pitch from entry.txt shipped in this repository, checks it
against the competition gate (UTF-8 text, 1 to 240 characters, not
only whitespace), and writes it to $MAKEFUN_OUTPUT_DIR/entry.txt
(falling back to /output/entry.txt) for the sealed scorer and judge.
Pure standard library: no third-party packages, no network access.
"""

import os
import sys

MAX_CHARS = 240


def load_pitch():
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "entry.txt")
    with open(path, "r", encoding="utf-8") as handle:
        return handle.read().strip()


def check_pitch(text):
    if not text:
        raise ValueError("pitch is empty")
    if len(text) > MAX_CHARS:
        raise ValueError(
            "pitch is %d characters, over the %d limit" % (len(text), MAX_CHARS)
        )
    if not text.strip():
        raise ValueError("pitch is only whitespace")
    if "\n" in text:
        raise ValueError("pitch must be a single line")
    return text


def main():
    pitch = check_pitch(load_pitch())
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")
    tmp = "%s.tmp%d" % (target, os.getpid())
    with open(tmp, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(pitch + "\n")
    os.replace(tmp, target)
    with open(target, "r", encoding="utf-8") as handle:
        written = handle.read().strip()
    if written != pitch:
        raise ValueError("read-back mismatch after writing entry.txt")
    check_pitch(written)
    print("Wrote %d-character pitch to %s" % (len(pitch), target))
    print(pitch)
    return 0


if __name__ == "__main__":
    sys.exit(main())
