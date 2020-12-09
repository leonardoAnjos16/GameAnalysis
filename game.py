class Game:
    def __init__(self, left_team_name, right_team_name):
        self.teams = {
            "l": Team(left_team_name, "l"),
            "r": Team(right_team_name, "r")
        }

        self.ball = Ball()

    def get_team(self, side):
        return self.teams[side]


class Team:
    def __init__(self, name, side):
        self.name = name
        self.side = side
        self.players = [Player(i + 1) for i in range(11)]
        self.goals = 0

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