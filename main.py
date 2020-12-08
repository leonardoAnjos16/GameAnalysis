import csv
import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <CSVLogFilePath>")
        return

    with open(sys.argv[1], 'r') as log_file:
        reader = csv.DictReader(log_file)

        headers = {
            "team": [
                header.replace("team_", "")[:-2]
                for header in reader.fieldnames
                if header.startswith("team_") and header.endswith("_l")
            ],
            "ball": [
                header.replace("ball_", "")
                for header in reader.fieldnames
                if header.startswith("ball_")
            ],
            "player": [
                header.replace("player_l1_", "")
                for header in reader.fieldnames
                if header.startswith("player_l1_")
            ]  
        }


if __name__ == "__main__":
    main()