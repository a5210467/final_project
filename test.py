import numpy as np


ROW_NUMBER = 6
COLUMN_NUMBER = 7
ARRAY_LENGTH = 4
board = np.zeros((ROW_NUMBER,COLUMN_NUMBER))

board[1][1] = 1
row_array = board[1,1:1+3]
print(row_array)

for i in range(ROW_NUMBER - ARRAY_LENGTH + 1):
        for j in range (COLUMN_NUMBER - ARRAY_LENGTH + 1):
                print(i,j)

print("something here ")

for i in range(ROW_NUMBER - ARRAY_LENGTH + 1 , ROW_NUMBER):
        for j in range (COLUMN_NUMBER - ARRAY_LENGTH + 1, COLUMN_NUMBER):
                print(i,j)
test_array = [1,1,1,1]
#print( np.array_equal(np.where(test_array == 0)[0], []) )

def get_player(state):
    return "XO"[
        np.count_nonzero(state == "O") < np.count_nonzero(state == "X")]

state = np.array([["_"]*3]*3)
#state[0,1] = "X"
#print(get_player(state))

def get_next_open_row(board, col):
    #check if there still have valid position for next round
    #return np.where(board[:,col] == 0)[0][0]
    if np.array_equal(np.where(board[:,col] == 0)[0], []):
        print('Col is already full')
        return None
    else:
        return np.where(board[:,col] == 0)[0][-1]

print(get_next_open_row(board,2))

'''
for i in range(1000):
    while True:
'''   

array_4 = np.array([1,2,3,4])
col = np.random.choice(array_4, size=1)[0]
print(col)