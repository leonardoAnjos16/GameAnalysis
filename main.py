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

# Creates game object with all the important information about the game
def create_game(path):
    with open(path, 'r') as log_file:
        # Parses CSV into a list of dictionaries
        reader = csv.DictReader(log_file)

        # Extracts team names from first row of CSV
        row = next(reader)
        team_names = []

        for side in "lr":
            team_names.append(row[header("team", "name")(side)])

        # Initializes game object
        game = Game(team_names[0], team_names[1])

        # Restarts reader to first row of CSV
        log_file.seek(0)
        reader = csv.DictReader(log_file)

        # Goes through each row in CSV and gather information about teams, ball and players
        for row in reader:
            # Gets ball current position and velocity
            game.ball.new_position(row[header("ball", "x")], row[header("ball", "y")])
            game.ball.new_velocity(row[header("ball", "vx")], row[header("ball", "vy")])

            # Gets each player current position and velocity
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