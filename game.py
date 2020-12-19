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
                self.states.append({
                    "show_time": int(row[header("show_time")]),
                    "playmode": row[header("playmode")]
                })

                # Gets ball current position
                ball_header = header("ball")
                self.ball.new_position(row[ball_header("x")], row[ball_header("y")])

                # Updates each team score
                team_header = header("team")
                for index, side in zip([0, 1], [left, right]):
                    self.teams[index].goals = row[team_header("score", side)]

                # Updates each player information
                for side in (left, right):
                    team = self.get_team(side)
                    for number in range(1, 12):
                        player = team.get_player(number)
                        player_header = header("player")

                        player.new_position(row[player_header("x", side, number)], row[player_header("y", side, number)])
                        player.tackles = int(row[player_header("counting_tackle", side, number)])

    # Returns team given side
    def get_team(self, side):
        return self.teams[0] if side == left else self.teams[1]

    # Gets important stats from game
    def get_stats(self):
        # Gets defense/offense ball possession for each team
        def ball_possession():
            # Checks if player has the ball at given frame
            def player_has_ball(frame, player):
                player_x, player_y = player.positions[frame]
                ball_x, ball_y = self.ball.positions[frame]

                distance = sqrt((player_x - ball_x) ** 2 + (player_y - ball_y) ** 2)
                return distance <= 4.0

            # Checks if ball is on the defense or offense side at given frame
            def ball_side(frame, team_side):
                sides = {
                    left: "defense",
                    right: "offense"
                }

                if team_side == right:
                    sides[left], sides[right] = sides[right], sides[left]

                return sides[left] if self.ball.positions[frame][0] <= 0 else sides[right]

            # Initializes counters for how many frames each team had the ball on each side of the field
            possession_count = {
                team: {
                    "defense": 0,
                    "offense": 0
                }
                for team in self.teams
            }

            # Updates counters considering which team has the ball on each frame of time
            num_frames = 0
            for frame in range(len(self.states)):
                # Makes sure game clock is running
                if self.states[frame]["playmode"].startswith("foul_charge"):
                    continue

                # Finds which team has the ball on current frame
                has_ball = False
                for team in self.teams:
                    for player in team.players:
                        if player_has_ball(frame, player):
                            current_team = team
                            has_ball = True
                            break
                    
                    if has_ball:
                        break

                # Updates counter
                possession_count[current_team][ball_side(frame, current_team.side)] += 1
                num_frames += 1

            return {
                team: {
                    side: count / num_frames * 100
                    for side, count in counters.items()
                }
                for team, counters in possession_count.items()
            }

        # Gets number of fouls commited by each team
        def calculate_fouls():
            fouls = { side: 0 for side in (left, right) }
            last_show_time, last_playmode = 0, ""

            for state in self.states:
                show_time, playmode = state["show_time"], state["playmode"]
                if playmode.startswith("foul_charge") and (show_time > last_show_time or playmode != last_playmode):
                    fouls[playmode[-1]] += 1

                last_show_time, last_playmode = show_time, playmode

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
            "fouls": calculate_fouls(),
            "tackles": {
                team: team.get_tackles()
                for team in self.teams
            }
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

    def get_tackles(self):
        return sum([player.tackles for player in self.players])


class Ball:
    def __init__(self):
        self.positions = []

    def new_position(self, x, y):
        self.positions.append((float(x), float(y)))


class Player:
    def __init__(self, number):
        self.number = number
        self.positions = []
        self.tackles = 0

    def new_position(self, x, y):
        self.positions.append((float(x), float(y)))
