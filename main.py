#!/usr/bin/env python3

import sys
import winona.bot.bot
import winona.cli.cli

def main(argv):
    if len(argv) < 2:
        print("usage: {} bot|cli [tool specific args]", argv[0])
        sys.exit(1)
    elif argv[1] == "bot":
        winona.bot.bot.main(argv[2:])
    elif argv[1] == "cli":
        # remove main.py cli from argv
        winona.cli.cli.main(argv[2:])
    else:
        print("usage: {} bot|cli")
        sys.exit(1)
    return

if __name__ == "__main__":
    main(sys.argv)
