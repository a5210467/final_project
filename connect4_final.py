import numpy as np
import sys
import math
import random
import time

from MCTNode import Node
from collections import defaultdict

ROW_NUMBER = 6
COLUMN_NUMBER = 7

PLAYER = 1
AI =2

PLAYER_DICE = 1
AI_DICE = 2

DROP_PROBABILITY = 0.10

def create_new_board():
	board = np.zeros((ROW_NUMBER,COLUMN_NUMBER), dtype=int)
	return board

def get_next_open_row(board, col):
    #check if there still have valid position for next round
    #return np.where(board[:,col] == 0)[0][0]
    if np.array_equal(np.where(board[:,col] == 0)[0], []):
        #print('Col is already full')
        return None
    else:
        return np.where(board[:,col] == 0)[0][-1]

def get_player(board):
    if np.count_nonzero(board == PLAYER) < np.count_nonzero(board == AI_DICE):
        return PLAYER
    else:
        return AI

def get_player_dice(player):
    if player == PLAYER:
        return PLAYER_DICE
    else:
        return AI_DICE


def drop_dice(board_,col ,player = None):
    board = board_.copy()
    
    if player == None:
        player = get_player(board)
    
    player_dice = get_player_dice(player)
    #print(player_dice)
    
    row = get_next_open_row(board, col)
    if row == None:
        print('Col is already full')
    else:
        board[row][col] = player_dice
    
    return board, player if win_check(board, player_dice) else 0

def win_check(board, player_piece):
    # Check for col location for win
    for col in range(COLUMN_NUMBER-3):
        for row in range(ROW_NUMBER):
            if board[row][col] == board[row][col+1] == board[row][col+2] == board[row][col+3] == player_piece:
                return True

    # Check for row locations for win
    for col in range(COLUMN_NUMBER):
        for row in range(ROW_NUMBER-3):
            if board[row][col] == board[row+1][col] == board[row+2][col] == board[row+3][col] == player_piece:
                return True

	# Check diaganols location for win
    for col in range(COLUMN_NUMBER-3):
        for row in range(ROW_NUMBER-3):
            if board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3] == player_piece:
                return True

	# Check negatively diaganols location for win
    for col in range(COLUMN_NUMBER-3):
        for row in range(3, ROW_NUMBER):
            if board[row][col] == board[row-1][col+1] == board[row-2][col+2] == board[row-3][col+3] == player_piece:
                return True
    
    return False

def check_winning_move(board, choices, player):
    #player_dice = get_player_dice(player)
    better_choice = []
    for i in choices:
        if drop_dice(board, i ,player)[1]:
            better_choice.append(i)
    return better_choice
    #return None

def valid_col_list(board):
    some_list = [col for col in range(COLUMN_NUMBER) if get_next_open_row(board,col)!= None]
    return some_list

def roll_once(board, player):
    while True:
        possible_choice = valid_col_list(board)
        
        if possible_choice == []:
            return 0
        
        #win for current choose and loose for others
        win_choice = check_winning_move(board, possible_choice, player)
        loose_choice = check_winning_move(board, possible_choice, (player)%2+1)

        if len(win_choice) > 0:
            choice = win_choice[0]
        elif len(loose_choice) > 0:
            choice = loose_choice[0]
        else:
            choice = random.choice(possible_choice)
        
        board, win_person = drop_dice(board, choice)

        if win_person != 0:
            return player
        '''
        drop_possible = random.uniform(0,1)
        if drop_possible >= DROP_PROBABILITY:
            player = (player)%2 + 1
        else:
            player = player
        '''
        
        #player = (player)%2 + 1

        
def rollout(mcts_node = None, player = None):
    if mcts_node == None:
         mcts_node = Node(create_new_board(), 0, None,  None)
    
    #my tree node to calcute
    node = mcts_node

    while node.children is not None:
        uct_array = [child.uct() for child in node.children]

        if None in uct_array:
            node = random.choice(node.children)
        else:
            node = node.children[np.argmax(uct_array)]
        
    valid_move = valid_col_list(node.state)

    if len(valid_move) > 0:
        if node.is_winning == 0:
            states = [(drop_dice(node.state, move), move) for move in valid_move]
            #print(states)
            node.put_children([Node(state_winning[0], state_winning[1], move=move, parent=node) for state_winning, move in states])
            wining_node_list = [n_c for n_c in node.children if n_c.is_winning]
            if len(wining_node_list) > 0:
                node = wining_node_list[0]
                winner_persion = node.is_winning
            else:
                node = random.choice(node.children)
                if player == None:
                    player = get_player(node.state)
                winner_persion = roll_once(node.state, player)
                #winner_persion = roll_once(node.state, get_player(node.state))
        else:
            winner_persion = node.is_winning
        
        parent = node
        while parent is not None:
            parent.visit_count += 1
            if winner_persion != 0 and get_player(parent.state) != winner_persion:
                parent.score_total += 1
            parent = parent.parent
    else:
        print('no valid moves, expended all')

    return mcts_node


def rollout_times(current_node, training_time, player = None):
    start = int(round(time.time() * 1000))
    current = start
    while (current - start) < training_time:
        current_node = rollout(current_node, player)
        current = int(round(time.time() * 1000))
    return current_node


def print_board(board):
    board_new = board.copy() - 3
    addition_col = np.arange(ROW_NUMBER)
    board_new = np.c_[board_new, addition_col]
    print_board = board_new.astype(int)
    print_board = board_new.astype(str)
    print_board[print_board == '-2'] = 'X'
    print_board[print_board == '-1'] = 'O'
    print_board[print_board == '-3'] = '_'
    res = str(print_board).replace("'", "")
    res = res.replace('[[', ' ')
    res = res.replace(']]', ' ')
    res = res.replace('[', ' ')
    res = res.replace(']', ' ')
    print(' ' + res)
    print('  ' + ' '.join('0123456'))

def simeple_AI_choice(board):
    return None


if __name__ == '__main__':
    print("choose if you want to play or just want to see the analysis result. For play enter 1. For see analysis result eneter 2")
    play_decision = int(input())

    mcts = None

    for i in range(800):
        mcts = rollout(mcts)
        if i % (1000 // 10) == 0: print(i, mcts.score_total /mcts.visit_count)
    
    
    #print('training finished, total is: ',mcts.score_total, ' visit count is: ', mcts.visit_count, 'score_estimate :',mcts.score_total /mcts.visit_count)
    
    if play_decision == 1:
        while True:
            # test AI with real play
            board = create_new_board()
            count = 0
            training_time = 2000
            node = mcts
            #print(node.score_total)
            print_board(board)
            
            winner = 0
            
            while True:
                if count == 0:
                    #has some probability to drop the dice for requirement
                    drop_decision = random.uniform(0,1)
                    #print(drop_decision)
                    move = int(input())
                    if drop_decision < DROP_PROBABILITY:
                        print("Player drop")
                        count = (count + 1)%2
                    else:
                        new_node = node.get_child(move)
                        node = rollout_times(node, training_time, PLAYER).get_child(move)
                        board, winner = drop_dice(board, move, PLAYER)
                        count = (count + 1)%2
                else:
                    #has some probability to drop the dice for requirement
                    drop_decision = random.uniform(0,1)
                    #print(drop_decision)
                    if drop_decision < DROP_PROBABILITY:
                        print("AI drop")
                        count = (count + 1)%2
                    else:
                        new_node, move = node.select_child()
                        node = rollout_times(node, training_time, AI)
                        # print([(n.win, n.games) for n in node.children])
                        node, move = node.select_child()
                        board, winner = drop_dice(board, move, AI)
                        count = (count + 1)%2

            

                #print(board)
                print_board(board)


                if winner != 0:
                    print('Winner : ', 'PLAYER' if winner == PLAYER else 'AI')
                    break
                
        