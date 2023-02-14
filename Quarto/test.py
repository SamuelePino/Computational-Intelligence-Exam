
import numpy as np
import utils



def check_win(grid):
  # Check rows
  for row in grid:
    print( "XOR", row[0] ^ row[1] ^ row[2] ^ row[3])
    if (row[0] ^ row[1] ^ row[2] ^ row[3]) > 0:
      return True
  # Check columns
  for col in range(4):
    if grid[0][col] ^ grid[1][col] ^ grid[2][col] ^ grid[3][col] and grid[0][col] != ' ':
      return True
  # Check diagonals
  if grid[0][0] ^ grid[1][1] ^ grid[2][2] ^ grid[3][3] and grid[0][0] != ' ':
    return True
  if grid[0][3] ^ grid[1][2] ^ grid[2][1] ^ grid[3][0] and grid[0][3] != ' ':
    return True
  return False

def check_win_human(board: np.ndarray):

    for row in board:   

        res = 0
        for elem in row:
            if elem != -1: 
                res ^= elem 

        if  res > 0:
            return  True

    for col in board.transpose():   

        res = 0
        for elem in col:
            if elem != -1: 
                res ^= elem 
                
        if  res > 0:
            return  True

    for elem in board.diagonal():   

            res = 0
            if elem != -1: 
                res ^= elem 
                    
            if  res > 0:
                return  True


    for elem in np.rot90(board).diagonal():   

        res = 0
        if elem != -1: 
            res ^= elem 
                
        if  res > 0:
            return  True

    return False
    


board: np.ndarray = np.array([ [0,2,3,4], [5,6,7,8], [-1,-1,-1,-1], [13,14,15,1]])
board_nuwwd: np.ndarray = np.array([[0,-1,5,9], [7,-1,1,10], [15,2, -1, 8], [3, 4, 11, 6]])
# for row  in board:
#     #print(row)
#     res: int = 0
#     for elem in row:
#         res ^= elem
#     if  sum(res.to_bytes()) >= 1:
#         # riga vincente
#         print("Row vincente")

# for l  in board.transpose():
#     print(l)


# print(check_win(board))
# print(board, board.diagonal(), np.rot90(board).diagonal())
# print("JJJ", check_win_human(board_nuwwd))

from dataclasses import dataclass

@dataclass
class MinMaxNode():
    """
    Mainly to think about implementation
    """
    board: np.ndarray
    remaining_pieces: list
    is_opponent: bool   #True is opponent's turn
poss_states = utils.cook_status(board=board, 
                                selected_piece= 10, 
                                my_test=True)["future_states"]
poss_pieces = utils.cook_status(choosing=True, board=board)

print("\n\n", poss_states[0:5], poss_pieces)