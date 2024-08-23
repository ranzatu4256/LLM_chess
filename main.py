from game import *
from player import *
from soldier_type import *
# 既存の駒クラス（Scout, Medic, HeavyInfantry, Communicator）をここに配置

# ゲームの初期化と実行
game = Game()

# 駒の配置（例）
game.add_piece(Scout(3, 0, 'ally'))
game.add_piece(Medic(2, 0, 'ally'))
game.add_piece(HeavyInfantry(1, 0, 'ally'))
game.add_piece(Communicator(0, 0, 'ally'))

game.add_piece(Scout(5, 8, 'enemy'))
game.add_piece(Medic(6, 8, 'enemy'))
game.add_piece(HeavyInfantry(7, 8, 'enemy'))
game.add_piece(Communicator(8, 8, 'enemy'))

game.run_game()