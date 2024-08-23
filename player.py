import random
import re
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

class HumanPlayer:
    def __init__(self, name):
        self.name = name

    def select_move(self, piece, possible_moves):
        while True:
            print(f"{self.name}'s {piece.symbol} at ({piece.x}, {piece.y}) can move to the following relative positions:")
            for dx, dy in possible_moves:
                print(f"({dx}, {dy})")
            dx = int(input(f"Where do you want to move {piece.symbol}? (dx) "))
            dy = int(input(f"Where do you want to move {piece.symbol}? (dy) "))
            if (dx, dy) in possible_moves:
                return dx, dy
            else:
                print("Invalid move. Please try again.")

    def receive_information(self, piece, enemy_positions):
        print(f"{self.name}'s {piece.symbol} has discovered the following enemy positions:")
        for pos_x, pos_y in enemy_positions:
            print(f"({pos_x}, {pos_y})")

    def select_attack_target(self, attacker, targets):
        print(f"{self.name}'s {attacker.symbol} can attack the following targets:")
        for target in targets:
            print(f"{target.symbol} at ({target.x}, {target.y})")
        target_x = int(input(f"Which target does {attacker.symbol} attack? (x) "))
        target_y = int(input(f"Which target does {attacker.symbol} attack? (y) "))
        for target in targets:
            if target.x == target_x and target.y == target_y:
                return target
        return None
    
class RandomBot:
    def __init__(self, name):
        self.name = name

    def select_move(self, piece, possible_moves):
        # 動かないことも含めてランダムに選択
        return random.choice(possible_moves)

    def receive_information(self, piece, enemy_positions):
        # 情報を受け取るだけで特に何もしない
        pass

    def select_attack_target(self, attacker, targets):
        # ランダムに攻撃対象を選択
        return random.choice(targets) if targets else None

class LLM_Player:
    def __init__(self, name):
        self.name = name
        torch.random.manual_seed(0)

    def generate_text(self, messages):
        torch.cuda.empty_cache()
        tokenizer = AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-4k-instruct")
        model = AutoModelForCausalLM.from_pretrained(
            "microsoft/Phi-3-mini-4k-instruct",
            device_map="cuda",
            torch_dtype="auto",
            trust_remote_code=True,
        )
        pipe = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
        )
        generation_args = {"max_new_tokens": 500, "return_full_text": False, "temperature": 0.0, "do_sample": False, }

        output = pipe(messages,**generation_args)
        assistant_response = output[0]['generated_text']
        print(assistant_response)
        return assistant_response

    def select_move(self, piece, possible_moves):
        selected = []
        context = ""
        num = 1
        team_flag = 1
        if piece.team == 'enemy':
            team_flag = -1
        
        # 知っている敵の情報を追加
        for enemy in piece.known_enemies:
            dx = enemy.x - piece.x
            dy = enemy.y - piece.y
            if dy*team_flag >= 0:
                vertical_dir = "forward"
            else:
                vertical_dir = "backward"
            if dx*team_flag >= 0:
                horizontal_dir = "left"
            else:
                horizontal_dir = "right"
            context += f"The enemy's {enemy.symbol} positon is {abs(dy)} spaces {vertical_dir} and {abs(dx)} spaces to the {horizontal_dir}.\n"

        # 移動可能マスの選択肢を追加
        context += f"{piece.symbol} at ({piece.x}, {piece.y}) can move to the following relative positions:"
        num = 1
        for dx, dy in possible_moves:
            selected.append([dx,dy])
            if dy*team_flag >= 0:
                vertical_dir = "forward"
            else:
                vertical_dir = "backward"
            if dx*team_flag >= 0:
                horizontal_dir = "left"
            else:
                horizontal_dir = "right"

            context += f"\n[{num}]{abs(dy)} spaces {vertical_dir} and {abs(dx)} spaces to the {horizontal_dir}."
            num += 1

        messages = [
            {"role": "system", "content": "You are a helpful AI assistant that provides a clear answer. You basically follow the policy of moving forward. You must only answer using a number."},
            {"role": "user", "content": f"[1]1 spaces forward and 0 spaces to the left.\n[2]2 spaces forward and 0 spaces to the left.\n Which option should I choose?"},
            {"role": "assistant", "content": "If I must follow the policy I should choose the option that is moving more forward. Therefore, I choose [2]"},
            {"role": "user", "content": f"{context} Which option should I choose?"},
        ]
        print(f"{context=}")
        while True:
            answer = self.generate_text(messages)

            # 正規表現パターン
            pattern = r'\[(\d+)\]'
            answer = int(re.findall(pattern, answer)[0])

            dx = selected[answer-1][0]
            dy = selected[answer-1][1]

            if (dx, dy) in possible_moves:
                return dx, dy
            else:
                print("Invalid move. Please try again.")

    def select_attack_target(self, attacker, targets):
        selected = []
        print(f"--{attacker.symbol} can attack the following targets:")
        context = ""
        num = 1
        team_flag = 1
        if attacker.team == 'enemy':
            team_flag = -1
        for target in targets:
            selected.append([target.x, target.y])
            if (target.x-attacker.x)*team_flag >= 0:
                vertical_dir = "forward"
            else:
                vertical_dir = "backward"
            if (target.y-attacker.y)*team_flag >= 0:
                horizontal_dir = "left"
            else:
                horizontal_dir = "right"

            if target.symbol == 'S' or target.symbol == 's':
                target_type = 'Scout'
            elif target.symbol == 'M' or target.symbol == 'm':
                target_type = 'Medic'
            elif target.symbol == 'H' or target.symbol == 'h':
                target_type = 'HeavyInfantry'
            elif target.symbol == 'C' or target.symbol == 'c':
                target_type = 'Communicator'

            context += f"\n[{num}]{abs(target.x-attacker.x)} spaces {vertical_dir} and {abs(target.y-attacker.y)} spaces to the {horizontal_dir}. The type of enemy is {target_type}."
            num += 1
        message = [
            {"role": "system", "content": "You are a helpful AI assistant that provides a clear answer. You basically follow the policy of attacking enemies in the forward direction. You must only answer using a number."},
            {"role": "user", "content": f"[1]0 spaces formard and 1 spaces to the left.\n[2]:2 spaces formard and 0 spaces to the left.\n.\n Which option should I choose?"},
            {"role": "assistant", "content": "I must follow the policy. Therefore, I choose [2]"},
            {"role": "user", "content": f"{context} Which option should I choose?"},
        ]
        print(context)
        while True:
            if len(selected) > 1:
                answer = self.generate_text(message)

                # 正規表現パターン
                pattern = r'\[(\d+)\]'
                answer = int(re.findall(pattern, answer)[0])
            else:
                answer = 1

            target_x = selected[answer-1][0]
            target_y = selected[answer-1][1]

            for target in targets:
                if target.x == target_x and target.y == target_y:
                    return target
            return None