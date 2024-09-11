import random

class NavalBattleGame:
    def __init__(self, board_size=10):
        self.board_size = board_size
        self.board = [['~' for _ in range(board_size)] for _ in range(board_size)]
        self.ships = []
        self.shots = []
        self.place_ships()

    def place_ships(self):
        ship_lengths = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        
        for length in ship_lengths:
            placed = False
            while not placed:
                x = random.randint(0, self.board_size - 1)
                y = random.randint(0, self.board_size - 1)
                direction = random.choice(['horizontal', 'vertical'])
                
                if self.can_place_ship(x, y, length, direction):
                    self.add_ship(x, y, length, direction)
                    placed = True

    def can_place_ship(self, x, y, length, direction):
        if direction == 'horizontal':
            if y + length > self.board_size:
                return False
            return all(self.board[x][y + i] == '~' for i in range(length)) and self.is_clear(x, y, length, direction)
        else:
            if x + length > self.board_size:
                return False
            return all(self.board[x + i][y] == '~' for i in range(length)) and self.is_clear(x, y, length, direction)

    def is_clear(self, x, y, length, direction):
        neighbors = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for i in range(length):
            cx, cy = (x, y + i) if direction == 'horizontal' else (x + i, y)
            for dx, dy in neighbors:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                    if self.board[nx][ny] == 'S':
                        return False
        return True

    def add_ship(self, x, y, length, direction):
        ship_coordinates = []
        if direction == 'horizontal':
            for i in range(length):
                self.board[x][y + i] = 'S'
                ship_coordinates.append((x, y + i))
        else:
            for i in range(length):
                self.board[x + i][y] = 'S'
                ship_coordinates.append((x + i, y))

        self.ships.append(ship_coordinates)

    def shoot(self, x, y):
        if (x, y) in self.shots:
            return "Вы уже стреляли сюда!"

        self.shots.append((x, y))

        if self.board[x][y] == 'S':
            self.board[x][y] = 'X'
            if self.is_ship_sunk(x, y):
                return "Корабль потоплен!"
            return "Попадание!"
        else:
            self.board[x][y] = 'O'
            return "Мимо!"

    def is_ship_sunk(self, x, y):
        for ship in self.ships:
            if (x, y) in ship:
                if all(self.board[coord[0]][coord[1]] == 'X' for coord in ship):
                    return True
        return False

    def is_game_over(self):
        return all(self.board[coord[0]][coord[1]] == 'X' for ship in self.ships for coord in ship)

    def display_board(self, reveal=False):
        return "\n".join([" ".join([self.board[x][y] if reveal or self.board[x][y] != 'S' else '~' for y in range(self.board_size)]) for x in range(self.board_size)])
