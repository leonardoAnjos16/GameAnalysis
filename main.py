import sys

from game import Game

def pretty_print(input, level=0):
    if isinstance(input, dict):
        if level > 0:
            print()

        for key, value in input.items():
            print("\t" * level, key, ": ", end="", sep="")
            pretty_print(value, level + 1)
    else:
        print(input)


def main():
    # Makes sure user input CSV file
    if len(sys.argv) < 2 or not sys.argv[1].endswith(".csv"):
        print("Usage: python3 main.py <CSVLogFilePath>")
        return

    game = Game(sys.argv[1])
    pretty_print(game.get_stats())


if __name__ == "__main__":
    main()