import random

def find_color_discs(board,color):
    """
        Finds all the discs of the given color and returns its currentCasees
    """
    discCoordinates=[]
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j].lower()==color:
                discCoordinates.append([i,j])

    return discCoordinates

def update_board_capture(board,currentCase,oppositCase,emptyCase):
    updated_board=board[:]
    updated_board[emptyCase[0]]=board[emptyCase[0]][:emptyCase[1]]+board[currentCase[0]][currentCase[1]]+board[emptyCase[0]][emptyCase[1]+1:]
    updated_board[oppositCase[0]]=board[oppositCase[0]][:oppositCase[1]]+'_'+board[emptyCase[0]][oppositCase[1]+1:]
    updated_board[currentCase[0]]=board[currentCase[0]][:currentCase[1]]+'_'+board[emptyCase[0]][currentCase[1]+1:]
    return updated_board

def capture_path(board,currentCase,step_direction,isKing):
    oppositCase=[currentCase[0]+step_direction[0],currentCase[1]+step_direction[1]]
    emptyCase=[currentCase[0]+2*step_direction[0],currentCase[1]+2*step_direction[1]]
    isEmpty="board[emptyCase[0]][emptyCase[1]]=='_'"
    isOpposit="board[oppositCase[0]][oppositCase[1]].lower()!=board[currentCase[0]][currentCase[1]].lower() and board[oppositCase[0]][oppositCase[1]]!='_'"

    try:
        if eval(isEmpty) and eval(isOpposit):
            path=[tuple(currentCase),tuple(emptyCase)]
            updated_board=update_board_capture(board,currentCase,oppositCase,emptyCase)
            if emptyCase[0]==0 or emptyCase[0]==len(board)-1:
                updated_isKing=True
            else:
                updated_isKing=isKing

            [path.extend(p[1:]) for p in allowed_capture_moves(updated_board,emptyCase,updated_isKing)]
            return path
    except IndexError:
            return []

    return []

def allowed_capture_moves(board,currentCase,isKing):
    """
        All possible capture moves for the disc at "currentCase" position
    """
    allowed_paths=[]
    forward_step=2*int(board[currentCase[0]][currentCase[1]].lower()=='b')-1
    step_directions=[[forward_step,1],[forward_step,-1]]
    if isKing : step_directions.extend([[-forward_step,1],[-forward_step,-1]])
    allowed_paths=[capture_path(board,currentCase,step_direction,isKing) for step_direction in step_directions]

    return allowed_paths

def allowed_non_capture_moves(board,currentCase,isKing):
    """
        All possible non capture moves for the disc at "currentCase" position supposing it's a black disc
    """
    allowed_paths=[]
    forward_step=2*int(board[currentCase[0]][currentCase[1]].lower()=='b')-1
    step_directions=[[forward_step,1],[forward_step,-1]]
    if isKing : step_directions.extend([[-forward_step,1],[-forward_step,-1]])

    for step_direction in step_directions:
        emptyCase=[currentCase[0]+step_direction[0],currentCase[1]+step_direction[1]]
        if board[emptyCase[0]][emptyCase[1]]=='_':
            allowed_paths.append([tuple(currentCase),tuple(emptyCase)])

    return allowed_paths

def allowed_paths(board, color):
    """
        All possible moves for player "color" for a given board
    """
    allowed_paths=[]
    for case in find_color_discs(board,color):
        allowed_paths.extend(allowed_capture_moves(board,case,board[case[0]][case[1]].isupper()))

    allowed_paths=list(filter(lambda x:x!=[],allowed_paths))

    if not len(allowed_paths):
        for case in find_color_discs(board,color):
            allowed_paths.extend(allowed_non_capture_moves(board,case,board[case[0]][case[1]].isupper()))
            return allowed_paths

    return allowed_paths

def play(board, color):
    """
        Play must return the next move to play.
        You can define here any strategy you would find suitable.
    """
    return random_play(board, color)

def random_play(board, color):
    """
        An example of play function based on allowed_paths.
    """
    moves = allowed_paths(board, color)
    # There will always be an allowed move
    # because otherwise the game is over and
    # 'play' would not be called by main.py
    return random.choice(moves)
