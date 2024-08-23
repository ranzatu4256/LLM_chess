class Scout:
    def __init__(self, x, y, team):
        self.x = x
        self.y = y
        self.team = team
        self.hp = 5
        self.attack_power = 1
        self.move_range = 3
        self.scout_range = 4
        self.attack_range = 3
        self.inform_range = 2
        self.known_enemies = set()
        self.mobility_policy = ""
        self.attack_policy = ""
        self.symbol = 'S' if self.team == 'ally' else 's'

    def move(self, new_x, new_y, board):
        if self.is_valid_move(new_x, new_y, board):
            board[self.y][self.x] = '.'
            self.x, self.y = new_x, new_y
            board[self.y][self.x] = 'S' if self.team == 'ally' else 's'

    def is_valid_move(self, new_x, new_y, board):
        return (0 <= new_x < len(board) and 0 <= new_y < len(board) and
                abs(new_x - self.x) + abs(new_y - self.y) <= self.move_range and
                board[new_y][new_x] == '.')

    def scout(self, board, pieces):
        for dy in range(-self.scout_range, self.scout_range + 1):
            for dx in range(-self.scout_range, self.scout_range + 1):
                new_x, new_y = self.x + dx, self.y + dy
                if 0 <= new_x < 9 and 0 <= new_y < 9 and abs(new_x - self.x) + abs(new_y - self.y) <= self.scout_range:
                    if (self.team == 'ally' and board[new_y][new_x].islower()) or \
                       (self.team == 'enemy' and board[new_y][new_x].isupper()):
                        for piece in pieces:
                            if piece.x == new_x and piece.y == new_y:
                                self.known_enemies.add(piece)

    def inform_allies(self, board, enemy_positions):
        for dy in range(-self.inform_range, self.inform_range + 1):
            for dx in range(-self.inform_range, self.inform_range + 1):
                new_x, new_y = self.x + dx, self.y + dy
                if 0 <= new_x < 9 and 0 <= new_y < 9 and abs(new_x - self.x) + abs(new_y - self.y) <= self.inform_range:
                    if (self.team == 'ally' and board[new_y][new_x].isupper()) or \
                       (self.team == 'enemy' and board[new_y][new_x].islower()):
                        print(f"Informing ally at ({new_x}, {new_y}) about enemy positions: {enemy_positions}")

    def receive_information(self, sender, enemy_positions):
        if abs(sender.x - self.x) + abs(sender.y - self.y) <= sender.inform_range:
            self.known_enemies.update(enemy_positions)

    def attack(self, target_x, target_y, board):
        if self.is_valid_attack(target_x, target_y, board):
            print(f"Scout attacks position ({target_x}, {target_y})")
            # ここで攻撃対象の駒のHPを減らすなどの処理を行う

    def is_valid_attack(self, target_x, target_y, board):
        dx = abs(target_x - self.x)
        dy = abs(target_y - self.y)
        return (0 <= target_x < len(board) and 0 <= target_y < len(board) and
                #max(dx, dy) <= self.attack_range and
                abs(target_x - self.x) + abs(target_y - self.y) <= self.attack_range and
                ((self.team == 'ally' and board[target_y][target_x].islower()) or
                 (self.team == 'enemy' and board[target_y][target_x].isupper())))

class Medic:
    def __init__(self, x, y, team):
        self.x = x
        self.y = y
        self.team = team
        self.hp = 5
        self.attack_power = 1
        self.move_range = 2
        self.scout_range = 3
        self.attack_range = 3
        self.inform_range = 3
        self.revive_range = 3
        self.known_enemies = set()
        self.mobility_policy = ""
        self.attack_policy = ""
        self.symbol = 'M' if self.team == 'ally' else 'm'

    def move(self, new_x, new_y, board):
        if self.is_valid_move(new_x, new_y, board):
            board[self.y][self.x] = '.'
            self.x, self.y = new_x, new_y
            board[self.y][self.x] = 'S' if self.team == 'ally' else 's'

    def is_valid_move(self, new_x, new_y, board):
        return (0 <= new_x < len(board) and 0 <= new_y < len(board) and
                abs(new_x - self.x) + abs(new_y - self.y) <= self.move_range and
                board[new_y][new_x] == '.')

    def scout(self, board, pieces):
        for dy in range(-self.scout_range, self.scout_range + 1):
            for dx in range(-self.scout_range, self.scout_range + 1):
                new_x, new_y = self.x + dx, self.y + dy
                if 0 <= new_x < 9 and 0 <= new_y < 9 and abs(new_x - self.x) + abs(new_y - self.y) <= self.scout_range:
                    if (self.team == 'ally' and board[new_y][new_x].islower()) or \
                       (self.team == 'enemy' and board[new_y][new_x].isupper()):
                        for piece in pieces:
                            if piece.x == new_x and piece.y == new_y:
                                self.known_enemies.add(piece)

    def inform_allies(self, board, enemy_positions):
        for dy in range(-self.inform_range, self.inform_range + 1):
            for dx in range(-self.inform_range, self.inform_range + 1):
                new_x, new_y = self.x + dx, self.y + dy
                if 0 <= new_x < 9 and 0 <= new_y < 9 and abs(new_x - self.x) + abs(new_y - self.y) <= self.inform_range:
                    if (self.team == 'ally' and board[new_y][new_x].isupper()) or \
                       (self.team == 'enemy' and board[new_y][new_x].islower()):
                        print(f"Informing ally at ({new_x}, {new_y}) about enemy positions: {enemy_positions}")

    def receive_information(self, sender, enemy_positions):
        if abs(sender.x - self.x) + abs(sender.y - self.y) <= sender.inform_range:
            self.known_enemies.update(enemy_positions)

    def revive(self, board, defeated_pieces):
        for piece in defeated_pieces:
            if piece.team == self.team and (piece.symbol != "m" or piece.symbol != "M"):
                if abs(piece.x - self.x) + abs(piece.y - self.y) <= self.revive_range:
                    piece.hp = 1  # 蘇生時のHP
                    defeated_pieces.remove(piece)
                    print(f"{self.symbol} at ({self.x}, {self.y}) revived {piece.symbol} at ({piece.x}, {piece.y})")
        return defeated_pieces

    def attack(self, target_x, target_y, board):
        if self.is_valid_attack(target_x, target_y, board):
            print(f"Medic attacks position ({target_x}, {target_y})")
            # ここで攻撃対象の駒のHPを減らすなどの処理を行う

    def is_valid_attack(self, target_x, target_y, board):
        dx = abs(target_x - self.x)
        dy = abs(target_y - self.y)
        return (0 <= target_x < len(board) and 0 <= target_y < len(board) and
                #max(dx, dy) <= self.attack_range and
                abs(target_x - self.x) + abs(target_y - self.y) <= self.attack_range and
                ((self.team == 'ally' and board[target_y][target_x].islower()) or
                 (self.team == 'enemy' and board[target_y][target_x].isupper())))

class HeavyInfantry:
    def __init__(self, x, y, team):
        self.x = x
        self.y = y
        self.team = team
        self.hp = 5
        self.attack_power = 3
        self.move_range = 1
        self.scout_range = 3
        self.attack_range = 4
        self.inform_range = 3
        self.attack_area = 1
        self.known_enemies = set()
        self.mobility_policy = ""
        self.attack_policy = ""
        self.symbol = 'H' if self.team == 'ally' else 'h'

    def move(self, new_x, new_y, board):
        if self.is_valid_move(new_x, new_y, board):
            board[self.y][self.x] = '.'
            self.x, self.y = new_x, new_y
            board[self.y][self.x] = 'S' if self.team == 'ally' else 's'

    def is_valid_move(self, new_x, new_y, board):
        return (0 <= new_x < len(board) and 0 <= new_y < len(board) and
                abs(new_x - self.x) + abs(new_y - self.y) <= self.move_range and
                board[new_y][new_x] == '.')

    def scout(self, board, pieces):
        for dy in range(-self.scout_range, self.scout_range + 1):
            for dx in range(-self.scout_range, self.scout_range + 1):
                new_x, new_y = self.x + dx, self.y + dy
                if 0 <= new_x < 9 and 0 <= new_y < 9 and abs(new_x - self.x) + abs(new_y - self.y) <= self.scout_range:
                    if (self.team == 'ally' and board[new_y][new_x].islower()) or \
                       (self.team == 'enemy' and board[new_y][new_x].isupper()):
                        for piece in pieces:
                            if piece.x == new_x and piece.y == new_y:
                                self.known_enemies.add(piece)

    def inform_allies(self, board, enemy_positions):
        for dy in range(-self.inform_range, self.inform_range + 1):
            for dx in range(-self.inform_range, self.inform_range + 1):
                new_x, new_y = self.x + dx, self.y + dy
                if 0 <= new_x < 9 and 0 <= new_y < 9 and abs(new_x - self.x) + abs(new_y - self.y) <= self.inform_range:
                    if (self.team == 'ally' and board[new_y][new_x].isupper()) or \
                       (self.team == 'enemy' and board[new_y][new_x].islower()):
                        print(f"Informing ally at ({new_x}, {new_y}) about enemy positions: {enemy_positions}")

    def receive_information(self, sender, enemy_positions):
        if abs(sender.x - self.x) + abs(sender.y - self.y) <= sender.inform_range:
            self.known_enemies.update(enemy_positions)

    def attack(self, target_x, target_y, board):
        if self.is_valid_attack(target_x, target_y):
            print(f"Heavy Infantry attacks position ({target_x}, {target_y}) and surrounding area")
            affected_positions = self.get_attack_area(target_x, target_y)
            for pos_x, pos_y in affected_positions:
                if 0 <= pos_x < 9 and 0 <= pos_y < 9:
                    if (self.team == 'ally' and board[pos_y][pos_x].islower()) or \
                       (self.team == 'enemy' and board[pos_y][pos_x].isupper()):
                        print(f"Attacking enemy at ({pos_x}, {pos_y})")
                        # ここで攻撃対象の駒のHPを減らすなどの処理を行う

    def is_valid_attack(self, target_x, target_y, board):
        dx = abs(target_x - self.x)
        dy = abs(target_y - self.y)
        return (0 <= target_x < len(board) and 0 <= target_y < len(board) and
                #max(dx, dy) <= self.attack_range and
                abs(target_x - self.x) + abs(target_y - self.y) <= self.attack_range and
                ((self.team == 'ally' and board[target_y][target_x].islower()) or
                 (self.team == 'enemy' and board[target_y][target_x].isupper())))

    def get_attack_area(self, center_x, center_y):
        area = []
        for dy in range(-self.attack_area, self.attack_area + 1):
            for dx in range(-self.attack_area, self.attack_area + 1):
                area.append((center_x + dx, center_y + dy))
        return area

class Communicator:
    def __init__(self, x, y, team):
        self.x = x
        self.y = y
        self.team = team
        self.hp = 5
        self.attack_power = 1
        self.move_range = 2
        self.scout_range = 3
        self.attack_range = 3
        self.inform_range = 4
        self.known_enemies = set()
        self.mobility_policy = ""
        self.attack_policy = ""
        self.symbol = 'C' if self.team == 'ally' else 'c'

    def move(self, new_x, new_y, board):
        if self.is_valid_move(new_x, new_y, board):
            board[self.y][self.x] = '.'
            self.x, self.y = new_x, new_y
            board[self.y][self.x] = 'S' if self.team == 'ally' else 's'

    def is_valid_move(self, new_x, new_y, board):
        return (0 <= new_x < len(board) and 0 <= new_y < len(board) and
                abs(new_x - self.x) + abs(new_y - self.y) <= self.move_range and
                board[new_y][new_x] == '.')

    def scout(self, board, pieces):
        for dy in range(-self.scout_range, self.scout_range + 1):
            for dx in range(-self.scout_range, self.scout_range + 1):
                new_x, new_y = self.x + dx, self.y + dy
                if 0 <= new_x < 9 and 0 <= new_y < 9 and abs(new_x - self.x) + abs(new_y - self.y) <= self.scout_range:
                    if (self.team == 'ally' and board[new_y][new_x].islower()) or \
                       (self.team == 'enemy' and board[new_y][new_x].isupper()):
                        for piece in pieces:
                            if piece.x == new_x and piece.y == new_y:
                                self.known_enemies.add(piece)

    def inform_allies(self, board, enemy_positions):
        for dy in range(-self.inform_range, self.inform_range + 1):
            for dx in range(-self.inform_range, self.inform_range + 1):
                new_x, new_y = self.x + dx, self.y + dy
                if 0 <= new_x < 9 and 0 <= new_y < 9 and abs(new_x - self.x) + abs(new_y - self.y) <= self.inform_range:
                    if (self.team == 'ally' and board[new_y][new_x].isupper()) or \
                       (self.team == 'enemy' and board[new_y][new_x].islower()):
                        print(f"Informing ally at ({new_x}, {new_y}) about enemy positions: {enemy_positions}")

    def receive_information(self, sender, enemy_positions):
        if abs(sender.x - self.x) + abs(sender.y - self.y) <= sender.inform_range:
            self.known_enemies.update(enemy_positions)

    def attack(self, target_x, target_y, board):
        if self.is_valid_attack(target_x, target_y, board):
            print(f"Communicator attacks position ({target_x}, {target_y})")
            # ここで攻撃対象の駒のHPを減らすなどの処理を行う

    def is_valid_attack(self, target_x, target_y, board):
        dx = abs(target_x - self.x)
        dy = abs(target_y - self.y)
        return (0 <= target_x < len(board) and 0 <= target_y < len(board) and
                #max(dx, dy) <= self.attack_range and
                abs(target_x - self.x) + abs(target_y - self.y) <= self.attack_range and
                ((self.team == 'ally' and board[target_y][target_x].islower()) or
                 (self.team == 'enemy' and board[target_y][target_x].isupper())))