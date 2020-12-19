import csv
from math import sqrt

left, right = "l", "r"

# Defines header formatters for specific types of headers (team, ball and player)
def header(type):
    if type == "team":
       return lambda header, side: f"team_{header}_{side}"
    elif type == "ball":
        return lambda header: f"ball_{header}"
    elif type == "player":
        return lambda header, side, number: f"player_{side}{number}_{header}"
    else:
        return type


class Game:
    def __init__(self, filepath):
        self.states = []
        self.ball = Ball()

        with open(filepath, 'r') as log_file:
            # Parses CSV into a list of dictionaries
            reader = csv.DictReader(log_file)

            # Extracts team names from first row of CSV
            row = next(reader)
            self.teams = tuple(
                Team(row[header("team")("name", side)], side)
                for side in (left, right)
            )

            # Restarts reader to first row of CSV
            log_file.seek(0)
            reader = csv.DictReader(log_file)

            # Goes through each row in CSV and gather information about teams, ball and players
            for row in reader:
                # Adds current game state to array of states
                show_time = int(row[header("show_time")])
                playmode = row[header("playmode")]

                if show_time > len(self.states) or self.states[-1] != playmode:
                    self.states.append(playmode)

                # Gets ball current position and velocity
                ball_header = header("ball")
                self.ball.new_position(row[ball_header("x")], row[ball_header("y")])
                self.ball.new_velocity(row[ball_header("vx")], row[ball_header("vy")])

                # Updates each team score
                team_header = header("team")
                for index, side in zip([0, 1], [left, right]):
                    self.teams[index].goals = row[team_header("score", side)]

                # Gets each player current position and velocity
                for side in (left, right):
                    team = self.get_team(side)
                    for number in range(1, 12):
                        player = team.get_player(number)
                        player_header = header("player")
                        player.new_position(row[player_header("x", side, number)], row[player_header("y", side, number)])
                        player.new_velocity(row[player_header("vx", side, number)], row[player_header("vy", side, number)])

    # Returns team given side
    def get_team(self, side):
        return self.teams[0] if side == left else self.teams[1]

    # Gets important stats from game
    def get_stats(self):
        # Gets defense/offense ball possession for each team
        def ball_possession():
            # Checks if player has the ball at show_time
            def player_has_ball(show_time, player):
                player_x, player_y = player.positions[show_time]
                ball_x, ball_y = self.ball.positions[show_time]

                distance = sqrt((player_x - ball_x) ** 2 + (player_y - ball_y) ** 2)
                return distance <= 4.0

            # Checks if ball is on the defense or offense side at show_time
            def ball_side(show_time, team_side):
                sides = {
                    left: "defense",
                    right: "offense"
                }

                if team_side == right:
                    sides[left], sides[right] = sides[right], sides[left]

                return sides[left] if self.ball.positions[show_time][0] <= 0 else sides[right]

            # Initializes counters for how many frames each team had the ball on each side of the field
            possession_count = {
                team: {
                    "defense": 0,
                    "offense": 0
                }
                for team in self.teams
            }

            # Updates counters considering which team has the ball on each frame of time
            show_time = 0
            while show_time < len(self.ball.positions):
                # Finds which team has the ball on current frame of time
                has_ball = False
                for team in self.teams:
                    for player in team.players:
                        if player_has_ball(show_time, player):
                            current_team = team
                            has_ball = True
                            break

                    if has_ball:
                        break

                # Updates counter
                possession_count[current_team][ball_side(show_time, current_team.side)] += 1
                show_time += 1

            return {
                team: {
                    side: count / show_time * 100
                    for side, count in counters.items()
                }
                for team, counters in possession_count.items()
            }

        # Gets number of fouls commited by each team
        def calculate_fouls():
            fouls = { side: 0 for side in (left, right) }
            for state in self.states:
                if state.startswith("foul_charge"):
                    fouls[state[-1]] += 1

            return {
                self.teams[0]: fouls[left],
                self.teams[1]: fouls[right]
            }

        # Returns dictionary with all important game stats
        return {
            "ball_possession": ball_possession(),
            "goals": {
                team: team.goals
                for team in self.teams
            },
            "fouls": calculate_fouls()
        }


class Team:
    def __init__(self, name, side):
        self.name = name
        self.side = side
        self.players = [Player(i + 1) for i in range(11)]
        self.goals = 0

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return self.name

    def get_player(self, number):
        return self.players[number - 1]


class Ball:
    def __init__(self):
        self.positions = []
        self.velocities = []

    def new_position(self, x, y):
        self.positions.append((float(x), float(y)))

    def new_velocity(self, vx, vy):
        self.velocities.append((float(vx), float(vy)))


class Player:
    def __init__(self, number):
        self.number = number
        self.positions = []
        self.velocities = []

    def new_position(self, x, y):
        self.positions.append((float(x), float(y)))

    def new_velocity(self, vx, vy):
        self.velocities.append((float(vx), float(vy)))