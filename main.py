"""Entry program for the make.fun bounty
"Two Lines of Morning Light" (u-gudril-cool-two-lines-of-morning-light-ade94fc5).

Writes a two-line micro poem about light and morning to entry.txt in the
output directory given by MAKEFUN_OUTPUT_DIR (default "/output"), then reads
it back to verify it was written exactly.
"""

import os
import re
import sys

ENTRY = "Light climbs the stairwell in bare feet,\nand the whole house learns to breathe again."

MAX_CHARS = 120

# Worn language the judge penalises (criterion 3): no stock phrase about
# dawn, gold or waking may appear in the entry.
WORN_WORDS = ("dawn", "gold", "waking")


def main():
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

    if not ENTRY.strip():
        print("error: entry text is blank", file=sys.stderr)
        return 1
    if len(ENTRY) > MAX_CHARS:
        print(
            "error: entry is %d characters, over the %d limit"
            % (len(ENTRY), MAX_CHARS),
            file=sys.stderr,
        )
        return 1
    lines = ENTRY.split("\n")
    if len(lines) != 2:
        print(
            "error: entry must have exactly 2 lines, found %d" % len(lines),
            file=sys.stderr,
        )
        return 1
    for word in WORN_WORDS:
        if re.search(r"\b" + re.escape(word) + r"\b", ENTRY, re.IGNORECASE):
            print(
                "error: entry uses worn language: %r" % word,
                file=sys.stderr,
            )
            return 1

    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(ENTRY)

    # Read back and compare byte-for-byte: the file must contain exactly the
    # poem, with no trailing newline added or stripped.
    with open(path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != ENTRY:
        print("error: read-back mismatch", file=sys.stderr)
        return 1

    print("Wrote entry.txt (%d characters, 2 lines) to %s" % (len(ENTRY), path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
