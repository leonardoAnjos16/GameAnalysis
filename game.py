# TODO: calculate how much time the ball was on the defense/offense side
from math import sqrt

class Game:
    def __init__(self, left_team_name, right_team_name):
        self.teams = {
            "l": Team(left_team_name, "l"),
            "r": Team(right_team_name, "r")
        }

        self.ball = Ball()

    def get_team(self, side):
        return self.teams[side]

    def ball_possession(self):
        def player_has_ball(show_time, player):
            player_x, player_y = map(float, player.positions[show_time])
            ball_x, ball_y = map(float, self.ball.positions[show_time])

            distance = sqrt((player_x - ball_x) ** 2 + (player_y - ball_y) ** 2)
            return distance <= 4.0

        possession_count = { team: 0 for team in self.teams.values() }

        show_time = 0
        current_team = self.teams["l"]

        while show_time < len(self.ball.positions):
            has_ball = False
            for team in self.teams.values():
                for player in team.players:
                    if (player_has_ball(show_time, player)):
                        current_team = team
                        has_ball = True
                        break

                if has_ball:
                    break

            possession_count[current_team] += 1
            show_time += 1

        return {
            team: count / show_time * 100
            for team, count in possession_count.items()
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
        self.positions.append((x, y))

    def new_velocity(self, vx, vy):
        self.velocities.append((vx, vy))


class Player:
    def __init__(self, number):
        self.number = number
        self.positions = []
        self.velocities = []

    def new_position(self, x, y):
        self.positions.append((x, y))

    def new_velocity(self, vx, vy):
        self.velocities.append((vx, vy))