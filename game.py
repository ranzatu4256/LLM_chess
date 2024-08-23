from soldier_type import *
from player import *
import random

class Game:
    def __init__(self, board_size=9):
        self.board_size = board_size
        self.board = [['.' for _ in range(board_size)] for _ in range(board_size)]
        self.pieces = []
        self.defeated_pieces = []
        self.current_turn = 0
        self.max_turns = 10
        self.player_a = None
        self.player_b = None

    def add_piece(self, piece):
        self.pieces.append(piece)
        self.board[piece.y][piece.x] = piece.symbol

    def remove_piece(self, piece):
        self.pieces.remove(piece)
        self.board[piece.y][piece.x] = '.'

    def move_piece(self, piece, new_x, new_y):
        if piece.is_valid_move(new_x, new_y, self.board):
            self.board[piece.y][piece.x] = '.'
            piece.x, piece.y = new_x, new_y
            self.board[new_y][new_x] = piece.symbol

    def play_turn(self):
        self.current_turn += 1
        print(f"\n--- Turn {self.current_turn} ---")

        # 1. 自軍の駒の移動
        self.move_team_pieces('ally')

        # 2. 敵軍の駒の移動
        self.move_team_pieces('enemy')

        self.print_board()
        # 3. 情報共有
        self.share_information()

        # 4. 自軍の攻撃対象選択
        ally_attacks = self.select_attack_targets('ally')

        # 5. 敵軍の攻撃対象選択
        enemy_attacks = self.select_attack_targets('enemy')

        # 6. ダメージ計算
        self.calculate_damage(ally_attacks + enemy_attacks)

        # 7. 蘇生フェーズ
        self.revive_phase()

        # 8. ターン終了処理
        self.end_turn()

    def set_pieces_policy(self, team):
        if team == 'ally':
            self.set_pieces_policy_cli(self.player_a, team)
        else:
            self.set_pieces_policy_cli(self.player_b, team)

    def set_pieces_policy_cli(self, player, team):
        for piece in self.pieces:
            if piece.team == team:
                piece.mobility_policy = input(f"Input the mobility polisy of {piece.symbol}.")
                if piece.mobility_policy == '0':
                    piece.mobility_policy = "You basically follow the policy of moving forward."
                piece.attack_policy = input(f"Input the attack polisy of {piece.symbol}.")
                if piece.attack_policy == '0':
                    piece.attack_policy = "You basically follow the policy of attacking enemies in the forward direction."


    def move_team_pieces(self, team):
        if team == 'ally':
            self.move_pieces_cli(self.player_a, team)
        else:
            self.move_pieces_cli(self.player_b, team)

    def move_pieces_cli(self, player, team):
        for piece in self.pieces:
            if piece.team == team:
                possible_moves = [
                    (dx, dy)
                    for dx in range(-piece.move_range, piece.move_range + 1)
                    for dy in range(-piece.move_range, piece.move_range + 1)
                    #if piece.is_valid_move(piece.x + dx, piece.y + dy, self.board)
                    if abs(dx) + abs(dy) <= piece.move_range and piece.is_valid_move(piece.x + dx, piece.y + dy, self.board)
                ]
                possible_moves.append((0, 0))  # 動かないオプションを追加
                dx, dy = player.select_move(piece, possible_moves)
                new_x, new_y = piece.x + dx, piece.y + dy
                self.move_piece(piece, new_x, new_y)
                print(f"{piece.symbol} moved to ({new_x}, {new_y})")

    def share_information(self):
        # まず、全ての駒が周囲をスカウトします
        for piece in self.pieces:
            piece.known_enemies = set()
            piece.scout(self.board, self.pieces)

        # 次に、情報共有を行います
        for sender in self.pieces:
            for receiver in self.pieces:
                if sender != receiver and sender.team == receiver.team:
                    receiver.receive_information(sender, sender.known_enemies)
        for sender in reversed(self.pieces):
            for receiver in self.pieces:
                if sender != receiver and sender.team == receiver.team:
                    receiver.receive_information(sender, sender.known_enemies)

    def select_attack_targets(self, team):
        if team == 'ally':
            return self.select_attack_targets_cli(self.player_a, team)
        else:
            return self.select_attack_targets_cli(self.player_b, team)

    def select_attack_targets_cli(self, player, team):
        attacks = []
        for attacker in self.pieces:
            if attacker.team == team:
                targets = []
                for target in self.pieces:
                    if target.team != attacker.team:
                        dx = abs(target.x - attacker.x)
                        dy = abs(target.y - attacker.y)
                        if dx+dy <= attacker.attack_range:
                            targets.append(target)
                targets = list(set(targets) & attacker.known_enemies)
                print(f"{attacker.symbol} knows the following targets:")
                for enemy in  attacker.known_enemies:
                    print(f"-{enemy.symbol} at ({enemy.x}, {enemy.y})")
                print(f"{attacker.symbol} can attack the following targets:")
                for target in targets:
                    print(f"-{target.symbol} at ({target.x}, {target.y})")
                if targets:
                    target = player.select_attack_target(attacker, targets)
                    attacks.append((attacker, target))
        return attacks

    def calculate_damage(self, attacks):
        self.defeated_pieces = []
        for attacker, target in attacks:
            damage = attacker.attack_power
            target.hp -= damage
            print(f"{attacker.symbol} attacks {target.symbol} for {damage} damage. {target.symbol}'s HP: {target.hp}")
            if target.hp <= 0 and target not in self.defeated_pieces:
                self.defeated_pieces.append(target)

    def revive_phase(self):
        for piece in self.pieces:
            if isinstance(piece, Medic):
                self.defeated_pieces = piece.revive(self.board, self.defeated_pieces)

        # すべての攻撃が終わってから defeated_pieces を処理する
        for piece in self.defeated_pieces:
            print(f"{piece.symbol} is defeated!")
            self.remove_piece(piece)

    def end_turn(self):
        self.print_board()

    def check_victory(self):
        ally_pieces = [p for p in self.pieces if p.team == 'ally']
        enemy_pieces = [p for p in self.pieces if p.team == 'enemy']

        # 条件1: 敵の全滅
        if not enemy_pieces:
            return 'A'
        if not ally_pieces:
            return 'B'

        # 条件2: 一番奥のマスに到達
        for piece in self.pieces:
            if piece.team == 'ally' and piece.y == self.board_size - 1:
                return 'A'
            if piece.team == 'enemy' and piece.y == 0:
                return 'B'

        # 条件3: 10ターン終了時にHPの合計が大きい方
        if self.current_turn >= self.max_turns:
            ally_hp = sum(p.hp for p in ally_pieces)
            enemy_hp = sum(p.hp for p in enemy_pieces)
            if ally_hp > enemy_hp:
                return 'A'
            elif enemy_hp > ally_hp:
                return 'B'
            else:
                return 'draw'

        return None

    def print_board(self):
        for row in self.board:
            print(' '.join(row))

    def run_game(self):
        # プレイヤーの選択
        player_type_a = input("Select player type for Player A (human/llm/bot): ").lower()
        player_type_b = input("Select player type for Player B (human/llm/bot): ").lower()

        if player_type_a == 'human':
           self.player_a = HumanPlayer('Player A')
        elif player_type_a == 'llm':
            self.player_a = LLM_Player('LLM Player A')
            print("""
            Set the policy for pieces. If you want to use the default policy,\n
            "mobility_policy : You basically follow the policy of moving forward."\n
            "attack_policy : You basically follow the policy of attacking enemies in the forward direction."\n
            enter 0.
            """)
            self.set_pieces_policy('ally')
        else:
            self.player_a = RandomBot('Bot A')

        if player_type_b == 'human':
            self.player_b = HumanPlayer('Player B')
        elif player_type_b == 'llm':
            self.player_b = LLM_Player('LLM Player B')
            print("""
            Set the policy for pieces. If you want to use the default policy,\n
            "mobility_policy : You basically follow the policy of moving forward."\n
            "attack_policy : You basically follow the policy of attacking enemies in the forward direction."\n
            enter 0.
            """)
            self.set_pieces_policy('enemy')
        else:
            self.player_b = RandomBot('Bot B')

        while True:
            self.play_turn()
            victor = self.check_victory()
            if victor:
                if victor == 'draw':
                    print("The game ends in a draw!")
                else:
                    print(f"{victor.capitalize()} team wins!")
                break