
import numpy as np
import pygame
import sys
import math
import random
import time
#from .MCTNode import *



COLOR_BLUE = (0,0,255)
COLOR_RED = (255,0,0)
COLOR_YELLOW = (255,255,0)
COLOR_WHITE = (255,255,255)

ROW_NUMBER = 6
COLUMN_NUMBER = 7

ARRAY_LENGTH = 4

PLAYER = 0
AI = 1
EMPTY = 0

PLAYER_DICE = 1
AI_DICE = 2

CONSTANT = 0.5

class Node:
    def __init__(self, state, winning, move, parent):
        self.state = state
        self.parent = parent
        self.score_total = 0
        self.visit_count = 0
        self.children = None
        self.is_winning = winning
        self.move = move
    
    def put_children(self, children):
        self.children = children

    def uct(self):
        if self.visit_count == 0:
            return None
        else:
            return self.score_total/self.visit_count + np.sqrt(2*np.log(self.parent.visit_count)/self.visit_count)

    
    def select_child(self):
        if self.children is None:
            return None, None
        
        else:
            win_array = [w for w in self.children if w.is_winning]
            if len(win_array) > 0:
                choose = random.choice(win_array)
                return choose, choose.move
            
            visit_count_list = [child.score_total/child.visit_count if child.visit_count > 0 else 0 for child in self.children]

            choosed_child = self.children[np.argmax(visit_count_list)]

            return choosed_child, choosed_child.move

    def get_child(self, move):
        if not self.children:
            return None
        
        for child in self.children:
            if child.move == move:
                return child
        
        print("No child exist")



def create_new_board():
	board = np.zeros((ROW_NUMBER,COLUMN_NUMBER))
	return board

def drop_dice(board, row, col, dice):
	board[row][col] = dice

def is_valid_location(board, col):
	return board[ROW_NUMBER-1][col] == 0

def get_next_open_row(board, col):
    #check if there still have valid position for next round
    #return np.where(board[:,col] == 0)[0][0]
    if np.array_equal(np.where(board[:,col] == 0)[0], []):
        return None
    else:
        return np.where(board[:,col] == 0)[0][0]

def valid_col_list(board):
    some_list = [col for col in range(COLUMN_NUMBER) if get_next_open_row(board,col)!= None]
    return some_list

def get_player(board):
    if np.count_nonzero(board == 1) < np.count_nonzero(board == 2):
        return PLAYER
    else:
        return AI

def can_play(board, col):
    return np.sum(np.abs(board[:, col])) < len(board[:, col])

def play(board_, column, player=None):
    board = board_.copy()
    if player is None:
        player = get_player(board)
    
    player_dice = 0
    if player == PLAYER:
        player_dice = PLAYER_DICE
    else:
        player_dice = AI_DICE

    if get_next_open_row(board, column) != None:
        #row = board.shape[0] - 1 - np.sum(np.abs(board[:, column]), dtype=int)
        row = get_next_open_row(board,column)
        board[row, column] = player_dice
    else:
        raise Exception('Error : Column {} is full'.format(column))
    return board, player if win_check(board, player_dice) else 0


def print_board(board):
	print(np.flip(board, 0))


def win_check(board, player_piece):
    # Check for col location for win
    for col in range(COLUMN_NUMBER-3):
        for row in range(ROW_NUMBER):
            if board[row][col] == board[row][col+1] == board[row][col+2] == board[row][col+3] == player_piece:
            #if board[row][col] == piece and board[row][col+1] == piece and board[row][col+2] == piece and board[row][col+3] == piece:
                return True

    # Check for row locations for win
    for col in range(COLUMN_NUMBER):
        for row in range(ROW_NUMBER-3):
            if board[row][col] == board[row+1][col] == board[row+2][col] == board[row+3][col] == player_piece:
            #if board[row][col] == piece and board[row+1][col] == piece and board[row+2][col] == piece and board[row+3][col] == piece:
                return True

	# Check diaganols location for win
    for col in range(COLUMN_NUMBER-3):
        for row in range(ROW_NUMBER-3):
            if board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3] == player_piece:
            #if board[row][col] == piece and board[row+1][col+1] == piece and board[row+2][col+2] == piece and board[row+3][col+3] == piece:
                return True

	# Check negatively diaganols location for win
    for col in range(COLUMN_NUMBER-3):
        for row in range(3, ROW_NUMBER):
            if board[row][col] == board[row-1][col+1] == board[row-2][col+2] == board[row-3][col+3] == player_piece:
            #if board[row][col] == piece and board[row-1][col+1] == piece and board[row-2][col+2] == piece and board[row-3][col+3] == piece:
                return True


def draw_new_board(board):
	for col in range(COLUMN_NUMBER):
		for row in range(ROW_NUMBER):
			pygame.draw.rect(screen, COLOR_BLUE, (col*SQUARESIZE, row*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
			pygame.draw.circle(screen, COLOR_WHITE, (int(col*SQUARESIZE+SQUARESIZE/2), int(row*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
	
	for col in range(COLUMN_NUMBER):
		for row in range(ROW_NUMBER):		
			if board[row][col] == 1:
				pygame.draw.circle(screen, COLOR_RED, (int(col*SQUARESIZE+SQUARESIZE/2), height-int(row*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[row][col] == 2: 
				pygame.draw.circle(screen, COLOR_YELLOW, (int(col*SQUARESIZE+SQUARESIZE/2), height-int(row*SQUARESIZE+SQUARESIZE/2)), RADIUS)
	pygame.display.update()


def count_weight(array_4, player_dice):
    weight = 0
    against_player_dice = 0
    if player_dice == PLAYER_DICE:
        against_player_dice = AI_DICE
    else:
        against_player_dice = PLAYER_DICE
    #win case: no need for count weight
    #if array_4.count(player_dice) == 4:
    if np.count_nonzero(array_4 == player_dice) == 4:
        weight += 100
    elif np.count_nonzero(array_4 == player_dice) == 3 and np.count_nonzero(array_4 == EMPTY) == 1:
        weight += 10
    elif np.count_nonzero(array_4 == player_dice) == 2 and np.count_nonzero(array_4 == EMPTY) == 2:
        weight += 5

    if np.count_nonzero(array_4 ==against_player_dice) == 3 and np.count_nonzero(array_4 == EMPTY)== 1:
        weight -= 8
    elif np.count_nonzero(array_4 ==against_player_dice) == 2 and np.count_nonzero(array_4 == EMPTY)== 2:
        weight -= 4

    return weight

def count_weight_in_board(board, player):
    #COUNT FOR ROW SCORE
    score = 0
    #sliding window
    for i in range(ROW_NUMBER - ARRAY_LENGTH + 1):
        for j in range (COLUMN_NUMBER - ARRAY_LENGTH + 1):
            array_row = board[i,j:j+ARRAY_LENGTH] 
            array_col = board[i:i+ARRAY_LENGTH, j]
            matrix = board[i:i+ARRAY_LENGTH, j:j+ARRAY_LENGTH]
            array_diag = np.diag(matrix)
            array_oppo_diag = np.diag(np.fliplr(matrix))
            score += count_weight(array_row, player) + count_weight(array_col, player) + count_weight(array_diag, player) + count_weight(array_oppo_diag, player)
    
    #miss count row
    for i in range(ROW_NUMBER - ARRAY_LENGTH + 1 , ROW_NUMBER):
        for j in range(COLUMN_NUMBER - ARRAY_LENGTH + 1):
            array_row = board[i,j:j+ARRAY_LENGTH]
            score += count_weight(array_row, player)
    
    #miss count col
    for j in range(COLUMN_NUMBER - ARRAY_LENGTH + 1, COLUMN_NUMBER):
        for i in range(ROW_NUMBER - ARRAY_LENGTH +1):
            array_col = board[i:i+ARRAY_LENGTH, j]
            score += count_weight(array_col, player)

    return score

def check_terminal_node(board):
	return win_check(board, PLAYER_DICE) or win_check(board, AI_DICE) or len(get_valid_col_list(board)) == 0


def get_valid_col_list(board):
    valid_col_locations = np.arange(0, COLUMN_NUMBER)
    valid_col_locations_new = valid_col_locations[is_valid_location(board, valid_col_locations)]
    return valid_col_locations_new
    '''
    for col in range(COLUMN_NUMBER):
        if is_valid_location(board, col):
            valid_col_locations.append(col)
    return valid_col_locations
    '''

def children_of(board, player):
    children_without_loss = []
    #children_with_loss = []
    dice = 0
    oppo_dice = 0
    if player == PLAYER:
        dice = AI_DICE
        #oppo_dice = PLAYER_DICE
    else:
        dice = PLAYER_DICE
        #oppo_dice = AI_DICE

    for j in range(COLUMN_NUMBER):
        if get_next_open_row(board, j) != None:
            child = board.copy()
            i = get_next_open_row(board,j)
            child[i][j] = dice
            children_without_loss.append(child)
    '''
    for j in range(COLUMN_NUMBER):
        if get_next_open_row(board, j) != None:
            child = board.copy()
            i = get_next_open_row(board,j)
            child[i][j] = oppo_dice
            children_with_loss.append(child)
    '''
    return children_without_loss
    #return np.array([children_without_loss, children_with_loss], np.int32)


def minmax(board, depth, min_value, max_value, maximizingPlayer):
    valid_locations = get_valid_col_list(board)
    check_terminal = check_terminal_node(board)
    if check_terminal:
        if win_check(board, AI_DICE):
            return(None, math.inf)
        elif win_check(board, PLAYER_DICE):
            return(None, -math.inf)
        else:
            return(None,-1)
    
    if depth == 0:
        return(None, count_weight_in_board(board, AI_DICE))

    if maximizingPlayer == AI:
        score = -math.inf
        column = valid_locations[0]
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_dice(b_copy, row, col, AI_DICE)
            new_score_without_drop = minmax(b_copy, depth-1, min_value, max_value, PLAYER)[1]
            #new_score_with_drop = minmax(b_copy,depth-1, min_value, max_value, AI)[1]
            #expected value of this new_score
            new_score = 0.85*new_score_without_drop #- 0.15*new_score_with_drop
            if new_score > score:
                score = new_score
                column = col
            min_value = max(min_value, score)
            if min_value >= max_value:
                break
        return column, score

    else: 
        score = math.inf
        column = valid_locations[0]
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_dice(b_copy, row, col, PLAYER_DICE)
            #new_score = minmax(b_copy, depth-1, min_value, max_value, AI)[1]
            new_score_without_drop = minmax(b_copy,depth-1, min_value, max_value, AI)[1]
            #new_score_with_drop = minmax(b_copy, depth-1, min_value, max_value, PLAYER)[1]
            new_score = 0.85*new_score_without_drop #- 0.15*new_score_with_drop
            if new_score < score:
                score = new_score
                column = col
            max_value = min(max_value, score)
            if min_value >= max_value:
                break
        return column, score




def rollout_times(mcts, training_time):
    start = int(round(time.time() * 1000))
    current = start
    while (current - start) < training_time:
        mcts = rollout(mcts)
        current = int(round(time.time() * 1000))
    return mcts


def rollout(mcts_node = None):
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
            states = [(play(node.state, move), move) for move in valid_move]
            node.put_children([Node(state_winning[0], state_winning[1], move=move, parent=node) for state_winning, move in states])
            wining_node_list = [n for n in node.children if n.is_winning]
            if len(wining_node_list) > 0:
                node = wining_node_list[0]
                victorious = node.is_winning
            else:
                node = random.choice(node.children)
                #victorious = random_rollout(node.state)
                board = node.state
                #player = get_player(board)
                col, minmax_score = minmax(board, 1, -math.inf, math.inf, AI)
                victorious = play(node.state,col)
        else:
            victorious = node.is_winning
        
        parent = node
        while parent is not None:
            parent.visit_count += 1
            if victorious != 0 and get_player(parent.state) != victorious:
                parent.score_total += 1
            parent = parent.parent
    else:
        print('no valid moves, expended all')

    return mcts_node

    return None


board = create_new_board()
print_board(board)
game_over = False
turn = 0
pygame.init()

SQUARESIZE = 100

width = COLUMN_NUMBER * SQUARESIZE
height = (ROW_NUMBER+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
draw_new_board(board)
pygame.display.update()

game_font = pygame.font.SysFont("Corbel", 40)

#print(count_weight_in_board(board,PLAYER_DICE))
#print(children_of(board,AI)[1])

mcts = None
for i in range(500):
        mcts = rollout(mcts)

while not game_over:
    node = mcts

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, COLOR_WHITE, (0,0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == PLAYER:
                pygame.draw.circle(screen, COLOR_RED, (posx, int(SQUARESIZE/2)), RADIUS)
            else: 
                pygame.draw.circle(screen, COLOR_YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, COLOR_WHITE, (0,0, width, SQUARESIZE))

            #Add an random variable that choose either drop or not. This random variable is uniform distributed between (0,1)
            decision = random.uniform(0, 1)
            print(decision)

			#print(event.pos)
			# Ask for Player 1 Input

            if turn == PLAYER:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                #for 15 persent chance drop the dice
                if decision <= 0.15:
                    label = game_font.render("Player 1 drops!! Player 2 turns", 1, COLOR_RED)
                    screen.blit(label, (40,10))
                    turn += 1
                    turn = turn % 2
                    continue
                else:
                    #new_node = node.get_child(col)
                    #node = rollout_times(node, 1500).get_child(col)
                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_dice(board, row, col, PLAYER_DICE)

                        if win_check(board, PLAYER_DICE):
                            label = game_font.render("Player 1 wins!!", 1, COLOR_RED)
                            screen.blit(label, (40,10))
                            game_over = True
                
                        print_board(board)
                        draw_new_board(board)

                        turn += 1
                        turn = turn % 2

    if turn == AI and not game_over:
        

        decision = random.uniform(0, 1)
        print(decision)

        if decision <= 0.15:
            label = game_font.render("Player 2 drops!! Player 1 turns", 1, COLOR_RED)
            screen.blit(label, (40,10))
            turn += 1
            turn = turn % 2
            continue
        else:
            col, minmax_score = minmax(board, 5, -math.inf, math.inf, True)
            
            #current_node = Node(board, 0, None,  None)
            #rollout_times(current_node, 1500)
            #best_child, col = node.select_child()
            #node = rollout_times(node, 1500)
            #best_child, col = node.select_child()

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_dice(board,row,col,AI_DICE)

                if win_check(board, AI_DICE):
                    label = game_font.render("Player 2 wins!!", 1, COLOR_YELLOW)
                    screen.blit(label, (40,10))
                    game_over = True

                print(board)
                draw_new_board(board)
                
                turn += 1
                turn = turn % 2

            

    if game_over:
        pygame.time.wait(3000)
