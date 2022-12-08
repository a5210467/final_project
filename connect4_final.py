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

EMPTY = 0
ARRAY_LENGTH = 4

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
    col_string = ''
    for i in range(COLUMN_NUMBER):
        col_string += str(i)
    print('  ' + ' '.join(col_string))

def simeple_AI_choice(board):
    #random choice a place to drop the dice
    possible_list = valid_col_list(board)
    choose = -1
    if len(possible_list) > 0:
        choose = random.choice(possible_list)
    return choose
    return None

def test_hundred_times(mcts):
    SIMPLE_AI_winning_time = 0
    AI_winning_time = 0
    tie_game_time = 0
    visit_count_list = []
    score_total_list = []
    score_count_list = []

    
    for i in range(100):
        board = create_new_board()
        count = 0
        training_time = 2000
        node = mcts
        #print_board(board)
        winner = 0
        while True:
            if count == 0:
                #has some probability to drop the dice for requirement
                drop_decision = random.uniform(0,1)
                #print(drop_decision)

                #random choice one to put
                move = int(simeple_AI_choice(board))
                if drop_decision < DROP_PROBABILITY:
                    #print("SIMPLE_AI drop")
                    count = (count + 1)%2
                else:
                    try:
                        new_node = node.get_child(move)
                    except:
                        tie_game_time += 1
                        score_count_list.append(0)
                        break
                    node = rollout_times(node, training_time, PLAYER).get_child(move)
                    board, winner = drop_dice(board, move, PLAYER)
                    count = (count + 1)%2
            else:
                #has some probability to drop the dice for requirement
                drop_decision = random.uniform(0,1)
                #print(drop_decision)
                if drop_decision < DROP_PROBABILITY:
                    #print("AI drop")
                    count = (count + 1)%2
                else:
                    try:
                        new_node, move = node.select_child()
                    except:
                        tie_game_time += 1
                        score_count_list.append(0)
                        break
                    node = rollout_times(node, training_time, AI)
                    # print([(n.win, n.games) for n in node.children])
                    try:
                        node, move = node.select_child()
                    except:
                        tie_game_time += 1
                        score_count_list.append(0)
                        break
                    board, winner = drop_dice(board, move, AI)
                    count = (count + 1)%2

            

            #print_board(board)

            if winner != 0:
                print('Winner : ', 'SIMPLE_AI' if winner == PLAYER else 'AI')
                if winner == PLAYER:
                    SIMPLE_AI_winning_time += 1
                    score_count_list.append(check_score(board, PLAYER))
                else:
                    AI_winning_time +=1
                    score_count_list.append(check_score(board, AI))
                break
        visit_count_list.append(mcts.visit_count)
        score_total_list.append(mcts.score_total)
    
    return SIMPLE_AI_winning_time, AI_winning_time, tie_game_time, mcts.visit_count, mcts.score_total, visit_count_list, score_total_list, score_count_list

def count_weight(array_4, player_dice):
    weight = 0
    array_4 = np.array2string(array_4)
    array_4 = array_4.replace('[','')
    array_4 = array_4.replace(']','')
    array_4 = array_4.replace(' ','')
    #print(player_dice, array_4)


    #win case: no need for count weight
    #if array_4.count(player_dice) == 4:
    '''
    if np.count_nonzero(array_4 == player_dice) == 4:
        weight = 0
    elif np.count_nonzero(array_4 == player_dice) == 3 :
        weight = 5
    elif np.count_nonzero(array_4 == player_dice) == 2:
        weight = 10
    elif np.count_nonzero(array_4 == player_dice) == 1:
        weight = 20
    else:
        weight = 1
    '''
    if array_4.find(str(player_dice)*3) >= 0:
        weight = 5
    elif array_4.find(str(player_dice)*2) >= 0:
        weight = 10
    elif array_4.find(str(player_dice)) >= 0:
        weight = 20
    else:
        weight = 1
    #print(weight)    
    return weight


def check_score(board_, winner):
    #print(winner == PLAYER)
    #print(winner == AI)
    check_dice = 0
    score = 0
    board = board_.copy()
    #print(board)
    #check the loser dice
    if winner == PLAYER:
        check_dice = AI_DICE
        #print(check_dice)
    if winner == AI:
        check_dice = PLAYER_DICE
        #print(check_dice)
    #print(check_dice)
    
    #sliding window
    for i in range(ROW_NUMBER - ARRAY_LENGTH + 1):
        for j in range (COLUMN_NUMBER - ARRAY_LENGTH + 1):
            array_row = board[i,j:j+ARRAY_LENGTH] 
            array_col = board[i:i+ARRAY_LENGTH, j]
            matrix = board[i:i+ARRAY_LENGTH, j:j+ARRAY_LENGTH]
            array_diag = np.diag(matrix)
            array_oppo_diag = np.diag(np.fliplr(matrix))
            temp_score = max(count_weight(array_row, check_dice) , count_weight(array_col, check_dice) , count_weight(array_diag, check_dice) , count_weight(array_oppo_diag, check_dice) )
            #print(temp_score)
            if score < temp_score:
                score = temp_score

    #miss count row
    for i in range(ROW_NUMBER - ARRAY_LENGTH + 1 , ROW_NUMBER):
        for j in range(COLUMN_NUMBER - ARRAY_LENGTH + 1):
            array_row = board[i,j:j+ARRAY_LENGTH]
            temp_score = count_weight(array_row, check_dice)
            #print(temp_score)
            if score > temp_score:
                score = temp_score
    
    #miss count col
    for j in range(COLUMN_NUMBER - ARRAY_LENGTH + 1, COLUMN_NUMBER):
        for i in range(ROW_NUMBER - ARRAY_LENGTH +1):
            array_col = board[i:i+ARRAY_LENGTH, j]
            temp_score = count_weight(array_col, check_dice)
            #print(temp_score)
            if score < temp_score:
                score = temp_score
    #print(score)
    if winner == PLAYER:
        return -score
    else:
        return score
    return score



if __name__ == '__main__':
    print('Choose the size you want to play, stardard is 6*7 has 6 row and 7 column')
    print('Please input row number: ')
    ROW_NUMBER = int(input())
    print('Please input col number: ')
    COLUMN_NUMBER = int(input())

    print(" Choose if you want to play or just want to see the analysis result.")
     
    print(" For play enter 1. \n For see analysis result eneter 2. \n For see simple AI against MCTS AI eneter 3 \n For see 100 SIMPLE_AI against AI result enter 4")
    play_decision = int(input())

    mcts = None

    for i in range(700):
        mcts = rollout(mcts)
        if i % (1000 // 10) == 0: print(i, mcts.score_total /mcts.visit_count)
    
    
    #print('training finished, total is: ',mcts.score_total, ' visit count is: ', mcts.visit_count, 'score_estimate :',mcts.score_total /mcts.visit_count)
    
    if play_decision == 1:
        while True:
            # test AI with real play
            board = create_new_board()
            count = 0
            training_time = 2500
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
    
    if play_decision == 3:

        board = create_new_board()
        count = 0
        training_time = 2500
        node = mcts
        print_board(board)
        tie_game = False
        winner = 0
        while True:
            if count == 0:
                #has some probability to drop the dice for requirement
                drop_decision = random.uniform(0,1)
                #print(drop_decision)

                #random choice one to put
                move = int(simeple_AI_choice(board))
                if drop_decision < DROP_PROBABILITY:
                    print("SIMPLE_AI drop")
                    count = (count + 1)%2
                else:
                    try:
                        new_node = node.get_child(move)
                    except:
                        tie_game = True
                    #new_node = node.get_child(move)
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
                    try:
                        new_node, move = node.select_child()
                    except:
                        tie_game = True
                    #new_node, move = node.select_child()
                    node = rollout_times(node, training_time, AI)
                    # print([(n.win, n.games) for n in node.children])
                    try:
                        node, move = node.select_child()
                    except:
                        tie_game = True
                    #node, move = node.select_child()
                    board, winner = drop_dice(board, move, AI)
                    count = (count + 1)%2

            

            #print(board)
            print_board(board)
            if tie_game == True:
                print('No winner, tie game')

            if winner != 0:
                print('Winner : ', 'SIMPLE_AI' if winner == PLAYER else 'AI')
                break
        print(' Total node visit count: ',mcts.visit_count)
    
    if play_decision == 4:
        SIMPLE_AI_winning_time, AI_winning_time, tie_game_times, visit_count ,score_total, visit_count_list, score_total_list, score_count_list = test_hundred_times(mcts)
        print('SIMPLE_AI win: ', SIMPLE_AI_winning_time, '\nAI win: ', AI_winning_time, '\nTie games: ', tie_game_times, '\nVisit node total: ', visit_count, '\nScore total is: ', score_total)
        print('Visit node count for each of 100 game list: ',visit_count_list)
        print('Score total list for each of 100 game list: ',score_total_list) 
        print('Score count list for each of 100 game list: ',score_count_list)
        

                
        