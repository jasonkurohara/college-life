from majors import majors, test_majors
from board import game_board, days_off
import random

board_len = len(game_board)

def game_over(players):
    for p in players:
        if players[p]['finished'] == False:
            return False
    return True


def simulate_turn(players):
    for major in players:
        p = players[major]
        roll = random.randint(1, 6) + random.randint(1, 6)
        p['current_tile'] += roll
        if p['current_tile'] >= board_len:
            p['finished'] = True
        else :
            tile = game_board[p['current_tile']]
            if isinstance(tile, int):
                effect = tile * p['stress_factor']
                p['energy_balance'] += effect
            else:
                p[tile] += 1
        if p['days_off'] < len(days_off) and days_off[p['days_off']] <= p['current_tile']:
            p['energy_balance'] += p['reward']
            p['days_off'] += 1
        players[major] = p
            

def simulate_game():
    players = {}
    m = majors
    for x in m.keys():
        players[x] = {
            'reward': m[x]['reward'],
            'stress_factor': m[x]['stress_factor'],
            'energy_balance': 0,
            'shake': 0,
            'decision': 0,
            'recovery': 0,
            'current_tile': 0,
            'finished': False,
            'days_off': 0
        }
    while True:
        if game_over(players):
            return players
        simulate_turn(players)

if __name__ == '__main__':
    player_results = simulate_game()
    for i in range(0, 100):
        new_results = simulate_game()
        for major in player_results:
            for metric in new_results[major]:
                if isinstance(new_results[major][metric], int):
                    player_results[major][metric] += new_results[major][metric]
    
    for major in player_results:
            for metric in player_results[major]:
                if isinstance(player_results[major][metric], int):
                    player_results[major][metric] /= 100
        

    for x in player_results:
        player = player_results[x]
        print('*************************************************')
        print('major: ' + x)
        for metric in player:
            print(metric + ': ' + str(player[metric]))
        print('*************************************************')