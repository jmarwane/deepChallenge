import random
# import numpy as np

# def board_to_matrix(board):
        # boardMatrix=np.vstack(   \
        #     [np.fromstring( \
        #     row.replace('_','0 ').replace('w','1 ').replace('W','2 ').replace('b','-1 ').replace('B','-2 '),    \
        #     dtype=np.int,sep=' ')   \
        #     for row in board])

def find_color_discs(board,color):
    """
        Finds all the discs of the given color and returns its indexes
    """
    discCoordinates=[]
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j].lower()==color:
                discCoordinates.append([i,j])

    return discCoordinates

def is_allowed(board,index,step_forward,direction)

def allowed_captue_moves(board,index,isKing=False):
    """
        All possible capture moves for the disc at "index" position
    """

    return []

def allowed_non_capture_moves(board,index):
    """
        All possible non capture moves for the disc at "index" position supposing it's a black disc
    """
    allowed_paths=[]
    step_forward=2*int(board[index[0]][index[1]].lower()=='b')-1

    if board[index[0]+step_forward][index[1]+1]=='_': allowed_paths.append([index[0]+step_forward,index[1]+1])
    if board[index[0]+step_forward][index[1]-1]=='_': allowed_paths.append([index[0]+step_forward,index[1]-1])
    if board[index[0]][index[1]].isupper():
        if board[index[0]-step_forward][index[1]+1]=='_': allowed_paths.append([index[0]-step_forward,index[1]+1])
        if board[index[0]-step_forward][index[1]-1]=='_': allowed_paths.append([index[0]-step_forward,index[1]-1])

    return allowed_paths

def allowed_moves(board, color):
    """
        All possible moves for player "color" for a given board
    """

    return []

def play(board, color):
    """
        Play must return the next move to play.
        You can define here any strategy you would find suitable.
    """
    return random_play(board, color)

def random_play(board, color):
    """
        An example of play function based on allowed_moves.
    """
    moves = allowed_moves(board, color)
    # There will always be an allowed move
    # because otherwise the game is over and
    # 'play' would not be called by main.py
    return random.choice(moves)
