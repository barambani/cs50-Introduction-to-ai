from minesweeper import Minesweeper, MinesweeperAI

import random

from multiprocessing import Pool
from datetime import datetime


MIN_HEIGHT = 8
MAX_HEIGHT = 50

MIN_WIDTH_HEIGHT_RATIO = 1
MAX_WIDTH_HEIGHT_RATIO = 3

WON = 'Won'
LOST = 'Lost'

class Simulation():
    def __init__(self) -> None:
        system_random = random.SystemRandom()
        self.height = system_random.randrange(
            start = MIN_HEIGHT,
            stop = MAX_HEIGHT
        ) if MIN_HEIGHT < MAX_HEIGHT else MIN_HEIGHT

        width_height_ratio = system_random.uniform(
            MIN_WIDTH_HEIGHT_RATIO,
            MAX_WIDTH_HEIGHT_RATIO
        ) if MIN_WIDTH_HEIGHT_RATIO < MAX_WIDTH_HEIGHT_RATIO else MIN_WIDTH_HEIGHT_RATIO

        self.width = int(self.height * width_height_ratio)
        self.mines = int((self.height * self.width) / 6)

        self.game = Minesweeper(self.height, self.width, self.mines)
        self.ai = MinesweeperAI(self.height, self.width)

        self.outcome = 'Unknown'
        self.lost_after_moves = 0

    def game_moves(self) -> int:
        return len(self.ai.moves_made)

    def remaining_moves(self) -> int:
        return len(self.ai.moves_remaining)


def run(simulation: Simulation) -> str:
    while True:
        next_move = simulation.ai.make_safe_move()
        if next_move is None:
            next_move = simulation.ai.make_random_move()

        if next_move is None:
            simulation.outcome = WON
            break

        if simulation.game.is_mine(next_move):
            simulation.outcome = LOST
            simulation.lost_after_moves = len(simulation.ai.moves_made) + 1
            break

        nearby = simulation.game.nearby_mines(next_move)
        simulation.ai.add_knowledge(next_move, nearby)
    
    return simulation


def run_simulator():
    print(f'{datetime.now():%Y-%m-%d %H:%M:%S}')
    total_simulation = 50 * 1000

    results = []
    simulations = list(map(lambda x: Simulation(), range(total_simulation)))
    # [print(f'H: {x.height}, W: {x.width}, Mines: {x.mines}') for x in simulations]

    print(f'{datetime.now():%Y-%m-%d %H:%M:%S}')
    with Pool(processes = 7) as pool:
        results = pool.map(run, simulations)

    won_games = []
    lost_games = []

    for simulation in results:
        if simulation.outcome == WON:
            won_games.append(simulation)
        if simulation.outcome == LOST:
            lost_games.append(simulation)
    print(f'{datetime.now():%Y-%m-%d %H:%M:%S}')
    print()

    lost_after_1_move = [lost_game for lost_game in lost_games if lost_game.lost_after_moves == 1]
    lost_after_2_move = [lost_game for lost_game in lost_games if lost_game.lost_after_moves == 2]
    lost_after_3_move = [lost_game for lost_game in lost_games if lost_game.lost_after_moves == 3]
    lost_after_4_move = [lost_game for lost_game in lost_games if lost_game.lost_after_moves == 4]
    lost_after_5_move = [lost_game for lost_game in lost_games if lost_game.lost_after_moves == 5]
    lost_in_less_than_6 = [lost_game for lost_game in lost_games if lost_game.lost_after_moves < 6]
    lost_in_6_to_10 = [lost_game for lost_game in lost_games if 6 < lost_game.lost_after_moves < 10]
    lost_in_10_to_100 = [lost_game for lost_game in lost_games if 10 < lost_game.lost_after_moves < 100]
    lost_in_100_to_500 = [lost_game for lost_game in lost_games if 100 < lost_game.lost_after_moves < 500]
    lost_in_500_to_1000 = [lost_game for lost_game in lost_games if 500 < lost_game.lost_after_moves < 1000]
    lost_in_1000_to_total_minus_10 = [lost_game for lost_game in lost_games if 1000 < lost_game.lost_after_moves and lost_game.remaining_moves() > 10]
    lost_in_total_minus_10 = [lost_game for lost_game in lost_games if lost_game.remaining_moves() <= 10]

    print(f'Won: {len(won_games)/len(results):.0%}')
    print(f'Lost: {len(lost_games)/len(results):.0%}')
    print()
    print(f'Lost in 1 move: {len(lost_after_1_move)/len(lost_games):.1%}')
    print(f'Lost in 2 move: {len(lost_after_2_move)/len(lost_games):.1%}')
    print(f'Lost in 3 move: {len(lost_after_3_move)/len(lost_games):.1%}')
    print(f'Lost in 4 move: {len(lost_after_4_move)/len(lost_games):.1%}')
    print(f'Lost in 5 move: {len(lost_after_5_move)/len(lost_games):.1%}')
    print(f'Lost in less than 6 moves: {len(lost_in_less_than_6)/len(lost_games):.1%}')
    print(f'Lost in 5 to 10 moves: {len(lost_in_6_to_10)/len(lost_games):.1%}')
    print(f'Lost in 10 to 100 moves: {len(lost_in_10_to_100)/len(lost_games):.1%}')
    print(f'Lost in 100 to 500 moves: {len(lost_in_100_to_500)/len(lost_games):.1%}')
    print(f'Lost in 500 to 1000 moves: {len(lost_in_500_to_1000)/len(lost_games):.1%}')
    print(f'Lost in 1000 to 10 moves from the end: {len(lost_in_1000_to_total_minus_10)/len(lost_games):.1%}')
    print(f'Lost in less than 10 moves from the end: {len(lost_in_total_minus_10)/len(lost_games):.1%}')
    return


if __name__ == '__main__':
    run_simulator()