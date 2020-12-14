import sys

from game import Game

def main():
    # Makes sure user input CSV file
    if len(sys.argv) < 2 or not sys.argv[1].endswith(".csv"):
        print("Usage: python3 main.py <CSVLogFilePath>")
        return

    game = Game(sys.argv[1])


if __name__ == "__main__":
    main()