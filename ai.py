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

def update_board(board,currentCase,emptyCase,oppositCase=None):
    updated_board=board[:]
    updated_board[currentCase[0]]=board[currentCase[0]][:currentCase[1]]+'_'+board[currentCase[0]][currentCase[1]+1:]
    if emptyCase[0]==0 or emptyCase[0]==len(board)-1:
        updated_board[emptyCase[0]]=board[emptyCase[0]][:emptyCase[1]]+board[currentCase[0]][currentCase[1]].upper()+board[emptyCase[0]][emptyCase[1]+1:]
    else:
        updated_board[emptyCase[0]]=board[emptyCase[0]][:emptyCase[1]]+board[currentCase[0]][currentCase[1]]+board[emptyCase[0]][emptyCase[1]+1:]

    if oppositCase is not None:
        updated_board[oppositCase[0]]=board[oppositCase[0]][:oppositCase[1]]+'_'+board[oppositCase[0]][oppositCase[1]+1:]
    return updated_board

def capture_path(board,currentCase,step_direction):
    oppositCase=[currentCase[0]+step_direction[0],currentCase[1]+step_direction[1]]
    emptyCase=[currentCase[0]+2*step_direction[0],currentCase[1]+2*step_direction[1]]
    isEmpty="board[emptyCase[0]][emptyCase[1]]=='_' and emptyCase[0]>=0 and emptyCase[1]>=0"
    isOpposit="board[oppositCase[0]][oppositCase[1]].lower()!=board[currentCase[0]][currentCase[1]].lower() and board[oppositCase[0]][oppositCase[1]]!='_'"

    try:
        if eval(isEmpty) and eval(isOpposit):
            one_step=[tuple(currentCase),tuple(emptyCase)]
            updated_board=update_board(board,currentCase,emptyCase,oppositCase)


            path=[one_step+p[1:] for p in allowed_capture_moves(updated_board,emptyCase)]

            if len(path)==0:
            	path=[one_step]

            return path
    except IndexError:
            return []

    return []

def allowed_capture_moves(board,currentCase):
    """
        All possible capture moves for the disc at "currentCase" position
    """
    allowed_paths=[]
    forward_step=2*int(board[currentCase[0]][currentCase[1]].lower()=='b')-1
    step_directions=[[forward_step,1],[forward_step,-1]]
    if board[currentCase[0]][currentCase[1]].isupper() : step_directions.extend([[-forward_step,1],[-forward_step,-1]])

    [allowed_paths.extend(capture_path(board,currentCase,step_direction)) for step_direction in step_directions]

    return allowed_paths

def allowed_non_capture_moves(board,currentCase):
    """
        All possible non capture moves for the disc at "currentCase" position supposing it's a black disc
    """
    allowed_paths=[]
    forward_step=2*int(board[currentCase[0]][currentCase[1]].lower()=='b')-1
    step_directions=[[forward_step,1],[forward_step,-1]]
    if board[currentCase[0]][currentCase[1]].isupper() :
        step_directions.extend([[-forward_step,1],[-forward_step,-1]])

    for step_direction in step_directions:
    	emptyCase=[currentCase[0]+step_direction[0],currentCase[1]+step_direction[1]]
    	try:
    		if emptyCase[0]!=-1 and emptyCase[1]!=-1 and board[emptyCase[0]][emptyCase[1]]=='_':
    			allowed_paths.append([tuple(currentCase),tuple(emptyCase)])
    	except IndexError:
    		pass

    return allowed_paths

def allowed_moves(board, color):
    """
        All possible moves for player "color" for a given board
    """
    allowed_paths=[]
    for case in find_color_discs(board,color):
        allowed_paths.extend(allowed_capture_moves(board,case))

    allowed_paths=list(filter(lambda x:x!=[],allowed_paths))

    if not len(allowed_paths):
        for case in find_color_discs(board,color):
            allowed_paths.extend(allowed_non_capture_moves(board,case))

    return allowed_paths

def play(board, color):
    """
        Play must return the next move to play.
        You can define here any strategy you would find suitable.
    """
    if color=='b': opposit_color='w'
    else : opposit_color='b'

    moves=allowed_moves(board,color)
    max_length=0
    for move in moves:
        if len(move)>max_length:
            max_length=len(move)

    moves=list(filter(lambda x:len(x)==max_length,moves))

    return random.choice(moves)

def simulate_play(board,move):
    updated_board=board
    oppositCase=None
    for i in range(1,len(move)):
        if move[i-1][0]!=move[i][0]-1:
            oppositCase=[int((move[i-1][0]+move[i][0])/2),int((move[i-1][1]+move[i][1])/2)]

        updated_board=update_board(updated_board,list(move[i-1]),list(move[i]),oppositCase)

    return updated_board

def random_play(board, color):
    """
        An example of play function based on allowed_paths.
    """
    moves = allowed_moves(board, color)
    # There will always be an allowed move
    # because otherwise the game is over and
    # 'play' would not be called by main.py
    return random.choice(moves)
