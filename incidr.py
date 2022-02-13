#!/usr/bin/env python

import sys
import re
from cidr import CidrBlock, CidrTree

COMMENT_REGEX = re.compile(r"^\s*#")

def get_input():
    lines = []

    for line in sys.stdin:
        # ignore empty lines or comments
        if not line.strip() or COMMENT_REGEX.match(line):
            continue
        lines.append(line.strip())

    return lines

def main():
    cidr_strings = get_input()
    cidr_blocks = map(CidrBlock.from_string, cidr_strings)

    tree = CidrTree()

    for cidr in cidr_blocks:
        tree.add(cidr)

    if len(sys.argv) >= 2 and sys.argv[1] == "join":
        if len(tree.children) == 0:
            return
        result = tree.children[0].root
        for child in tree.children:
            result |= child.root
        print(result)
    else:
        print(tree)

if __name__ == "__main__":
    main()
