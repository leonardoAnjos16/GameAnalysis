from math import sqrt

class Game:
    def __init__(self, left_team_name, right_team_name):
        self.teams = {
            "l": Team(left_team_name),
            "r": Team(right_team_name)
        }

        self.ball = Ball()

    def get_team(self, side):
        return self.teams[side]

    # Gets important stats from game
    def get_stats(self):
        # Get defense/offense ball possession for each team
        def ball_possession():
            # Checks if player has the ball at show_time
            def player_has_ball(show_time, player):
                player_x, player_y = player.positions[show_time]
                ball_x, ball_y = self.ball.positions[show_time]

                distance = sqrt((player_x - ball_x) ** 2 + (player_y - ball_y) ** 2)
                return distance <= 4.0

            # Checks if ball is on the defense or offense side ate show_time
            def ball_side(show_time, team_side):
                sides = {
                    "l": "defense",
                    "r": "offense"
                }

                if team_side == "r":
                    sides["l"], sides["r"] = sides["r"], sides["l"]

                return sides["l"] if self.ball.positions[show_time][0] <= 0 else sides["r"]

            # Initializes counters for how many frames each team had the ball on each side of the field
            possession_count = {
                team: {
                    "defense": 0,
                    "offense": 0
                }
                for team in self.teams.values()
            }

            # Updates counters considering which team has the ball on each frame of time
            show_time = 0
            while show_time < len(self.ball.positions):
                # Finds which team has the ball on current frame of time
                has_ball = False
                for side, team in self.teams.items():
                    for player in team.players:
                        if (player_has_ball(show_time, player)):
                            current_team = team
                            has_ball = True
                            break

                    if has_ball:
                        break

                # Updates counters
                possession_count[current_team][ball_side(show_time, side)] += 1
                show_time += 1

            return {
                team: {
                    side: count / show_time * 100
                    for side, count in counters.items()
                }
                for team, counters in possession_count.items()
            }

        # Returns dictionary with all important game stats
        return {
            "ball_possession": ball_possession()
        }


class Team:
    def __init__(self, name):
        self.name = name
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