import random
import time

def find_color_discs(board,color):
    """
        Finds all the discs of the given color and returns their coordinates
    """
    discCoordinates=[]
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j].lower()==color:
                discCoordinates.append([i,j])

    return discCoordinates

def update_board(board,current_case,empty_case,opposit_case=None):
    """
        Updates the game board after by moving the current_case disc to empty_case
        and eventually deleting the one in opposit_case if it's a capture move

        Handles the king status changement
    """
    updated_board=board[:]
    updated_board[current_case[0]]=board[current_case[0]][:current_case[1]]+'_'+board[current_case[0]][current_case[1]+1:]
    if empty_case[0]==0 or empty_case[0]==len(board)-1:   #if the disc reaches the border line it becomes a king
        updated_board[empty_case[0]]=board[empty_case[0]][:empty_case[1]]+board[current_case[0]][current_case[1]].upper()+board[empty_case[0]][empty_case[1]+1:]
    else:
        updated_board[empty_case[0]]=board[empty_case[0]][:empty_case[1]]+board[current_case[0]][current_case[1]]+board[empty_case[0]][empty_case[1]+1:]

    if opposit_case is not None:
        updated_board[opposit_case[0]]=board[opposit_case[0]][:opposit_case[1]]+'_'+board[opposit_case[0]][opposit_case[1]+1:]
    return updated_board

def capture_path(board,current_case,step_direction):
    """
        Find all the possible COMPLETE paths allowing a capture in the direction step_direction starting from current_case
        The function checks the one step capture path, updates the board and then calls the allowed_capture_moves function
            to complete the path in a recursive way

        opposit_case is the case that should contain an opposit color disc if the capture move is valid
        empty_case is the case that should be empty if the capture move is valid
    """
    opposit_case=[current_case[0]+step_direction[0],current_case[1]+step_direction[1]]
    empty_case=[current_case[0]+2*step_direction[0],current_case[1]+2*step_direction[1]]

    inRange="and empty_case[0]>=0 and empty_case[1]>=0"
    isEmpty="board[empty_case[0]][empty_case[1]]=='_'"
    isOpposit="board[opposit_case[0]][opposit_case[1]].lower()!=board[current_case[0]][current_case[1]].lower() and board[opposit_case[0]][opposit_case[1]]!='_'"

    try:
        if eval(inRange) and eval(isEmpty) and eval(isOpposit): #conditions for the capture move to be valid
            one_step=[tuple(current_case),tuple(empty_case)]
            updated_board=update_board(board,current_case,empty_case,opposit_case)
            path=[one_step+p[1:] for p in allowed_capture_moves(updated_board,empty_case)]

            if len(path)==0:
            	path=[one_step]

            return path
    except IndexError:  #Errors due to an out of range index
            return []

    return []

def allowed_capture_moves(board,current_case):
    """
        All possible capture moves for the disc at current_case
        Calls capture_path to check each possible moving direction
    """
    allowed_paths=[]
    #forward_step calculates the positive direction of motion for the current player : +1 for black and -1 for white
    forward_step=2*int(board[current_case[0]][current_case[1]].lower()=='b')-1
    #step_directions contains all allowed moving directions considering the color of the disc and its king status
    step_directions=[[forward_step,1],[forward_step,-1]]
    if board[current_case[0]][current_case[1]].isupper(): #if king all directions are allowed
        step_directions.extend([[-forward_step,1],[-forward_step,-1]])

    for step_direction in step_directions:
        allowed_paths.extend(capture_path(board,current_case,step_direction))

    return allowed_paths

def allowed_non_capture_moves(board,current_case):
    """
        All possible non capture moves for the disc at current_case
    """
    allowed_paths=[]
    #forward_step calculates the positive direction of motion for the current player : +1 for black and -1 for white
    forward_step=2*int(board[current_case[0]][current_case[1]].lower()=='b')-1
    #step_directions contains all allowed moving directions considering the color of the disc and its king status
    step_directions=[[forward_step,1],[forward_step,-1]]
    if board[current_case[0]][current_case[1]].isupper(): #if king all directions are allowed
        step_directions.extend([[-forward_step,1],[-forward_step,-1]])

    for step_direction in step_directions:
    	empty_case=[current_case[0]+step_direction[0],current_case[1]+step_direction[1]]
    	try:
    		if empty_case[0]!=-1 and empty_case[1]!=-1 and board[empty_case[0]][empty_case[1]]=='_':
    			allowed_paths.append([tuple(current_case),tuple(empty_case)])
    	except IndexError:
    		pass

    return allowed_paths

def allowed_moves(board, color):
    """
        All possible moves for player "color" for a given board
        Calls allowed_capture_moves to look for valid capture moves
        if none are, calls allowed_non_capture_moves to look for valid non capture moves
    """
    allowed_paths=[]
    for case in find_color_discs(board,color):
        allowed_paths.extend(allowed_capture_moves(board,case))

    allowed_paths=list(filter(lambda x:x!=[],allowed_paths)) #delete empty paths

    if not len(allowed_paths): # if no valid capture moves are found
        for case in find_color_discs(board,color):
            allowed_paths.extend(allowed_non_capture_moves(board,case))

    return allowed_paths

def play(board, color):
    """
        Play must return the next move to play.

        Chooses the next move in a minimax adversary fashion :
        explores all possible moves after several playing tours and chooses the best possible move
        supposing the opposit player is also playing his best available move

        Is not limited by a number of playing tours to explore but only with exploring time to avoid making the searching very long
        max_time is the eploring time limit

        Calls best_move to find the best possible move
    """
    start_time=time.time()
    max_time=10 #exploring time limit
    best_move=find_best_move(board,color,start_time,max_time)[1]
    print('Execution time : {}'.format(time.time()-start_time))

    return best_move

def simulate_play(board,move):
    """
        Simulate the advancing of the game given a starting board state "board" and a move "move"
        Returns the new board state
    """
    updated_board=board
    opposit_case=None

    for i in range(1,len(move)):
        if move[i-1][0]!=move[i][0]-1:
            opposit_case=[int((move[i-1][0]+move[i][0])/2),int((move[i-1][1]+move[i][1])/2)]

        updated_board=update_board(updated_board,list(move[i-1]),list(move[i]),opposit_case)

    return updated_board

def find_best_move(board,color,start_time,max_time):
    """
        Finds the best move which in a recursive fashion : for each allowed move calls itself to find the opposit best move and so on
        Stop when the time limit is reached or when the game is over

        Also calls evaluate_score() to evaluate the goodness of a move
        Returns both the move considered to be optimal and its score
    """
    #determinate the opposit player's color
    if color=='b': opposit_color='w'
    else : opposit_color='b'

    moves = allowed_moves(board,color)
    random.shuffle(moves)

    #stop condition is either the end of the game or the exploring time limit
    if time.time()-start_time>max_time or len(moves)==0:
        return [evaluate_score(board,color,opposit_color)] #evaluates the goodness of a move when searching is over

    best_move = moves[0]
    best_score = float('-inf')
    # for move in moves:
    for i in range(len(moves)):
        move=moves[i]
        clone = simulate_play(board,move)
        score = find_best_move(clone,opposit_color,start_time,max_time)[0]
        if score > best_score:
            best_move = move
            best_score = score

    return [best_score,best_move]

def evaluate_score(board,color,opposit_color):
    """
        Evaluates the goodness of a move : each own disc adds 1 to the score while each opposit disc retires 1
        A win is automatically a positive infinite score while a defeat is a negative infinite
    """
    if len(allowed_moves(board,color))==0:
        return float('-inf')
    if len(allowed_moves(board,opposit_color))==0:
        return float('inf')

    return len(find_color_discs(board,color))-len(find_color_discs(board,opposit_color))
