from collections import deque
from copy import deepcopy
from itertools import islice


class sliceable_deque(deque):
    def __getitem__(self, index):
        if isinstance(index, slice):
            return type(self)(islice(self, index.start,
                                               index.stop, index.step))
        return deque.__getitem__(self, index)

def simulate_game(player_1: deque, player_2: deque):
    round = 0
    while True:
        round += 1
        print(f"Round {round}:")
        print(player_1, player_2)

        player_1_card = player_1.popleft()
        player_2_card = player_2.popleft()
        print(f"player 1: {player_1_card}")
        print(f"player 2: {player_2_card}")
        winner = player_1 if player_1_card > player_2_card else player_2
        winner.extend(sorted((player_1_card, player_2_card), reverse=True))
        print(player_1, player_2)
        print()
        if len(player_1) == 0:
            return player_2
        if len(player_2) == 0:
            return player_1

def simulate_recursive_game(player_1: sliceable_deque, player_2: sliceable_deque):
    game_tracker = set()
    while True:
        game_state = (tuple(player_1), tuple(player_2))
        if game_state in game_tracker:
            return 1, player_1
        game_tracker.add(game_state)
        player_1_card = player_1.popleft()
        player_2_card = player_2.popleft()
        if len(player_1) < player_1_card or len(player_2) < player_2_card:
            winner = player_1 if player_1_card > player_2_card else player_2
            winner.extend(sorted((player_1_card, player_2_card), reverse=True))
        else:
            winning_player, _ = simulate_recursive_game(player_1[0:player_1_card], player_2[0:player_2_card])
            winner = player_1 if winning_player == 1 else player_2
            winner.extend((player_1_card, player_2_card) if winning_player == 1 else (player_2_card, player_1_card))
        if len(player_1) == 0:
            return (2, player_2)
        if len(player_2) == 0:
            return (1, player_1)

with open("input") as f:
    text = f.read().split("\n\n")
    player_1 = sliceable_deque((int(c) for c in text[0].split("\n")[1:]))
    player_2 = sliceable_deque((int(c) for c in text[1].split("\n")[1:]))

winner = simulate_game(player_1.copy(), player_2.copy())
score = sum((position+1) * card for position, card in enumerate(reversed(winner)))
print("Task 1:", score)

winner, winning_deck = simulate_recursive_game(player_1.copy(), player_2.copy())
score = sum((position+1) * card for position, card in enumerate(reversed(winning_deck)))
print("Task 2:", score)