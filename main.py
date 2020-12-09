import csv
import sys

from game import Game

# Defines header formatters for specific types of headers (team, ball and player)
def header(type, header):
    if type == "team":
       return lambda side: f"team_{header}_{side}"
    elif type == "ball":
        return f"ball_{header}"
    elif type == "player":
        return lambda side, number: f"player_{side}{number}_{header}"
    else:
        return header


def create_game(path):
    with open(path, 'r') as log_file:
        # Parses CSV into a list of dictionaries
        reader = csv.DictReader(log_file)

        row = next(reader)
        team_names = []

        for side in "lr":
            team_names.append(row[header("team", "name")(side)])

        game = Game(team_names[0], team_names[1])

        log_file.seek(0)
        reader = csv.DictReader(log_file)

        for row in reader:
            game.ball.new_position(row[header("ball", "x")], row[header("ball", "y")])
            game.ball.new_velocity(row[header("ball", "vx")], row[header("ball", "vy")])

            for side in "lr":
                team = game.get_team(side)
                for number in range(1, 12):
                    player = team.get_player(number)
                    player.new_position(row[header("player", "x")(side, number)], row[header("player", "y")(side, number)])
                    player.new_velocity(row[header("player", "vx")(side, number)], row[header("player", "vy")(side, number)])

    return game


def main():
    # Makes sure user input CSV file
    if len(sys.argv) < 2 or not sys.argv[1].endswith(".csv"):
        print("Usage: python3 main.py <CSVLogFilePath>")
        return

    game = create_game(sys.argv[1])


if __name__ == "__main__":
    main()