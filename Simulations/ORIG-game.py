#Raymond Liu, 2031256
#420-LCU Computer Programming
#Winter 2022
#R. Vincent, instructor
#Assignment 3

'''Implements the logic for the game Reversi, based on the "Othello"
version trademarked by Mattel.'''

from board import *
import time

HUMAN = 1
COMPUTER = 2

RUNTIME = open("ogruntime.txt", "a")
SCORES = open("oggames.txt", "a")

def game_start():
    '''Create and initialize the game data.

    Returns a properly initialized board object.
    '''
    # Create a board object.
    board = board_create()
    # Set up the initial board configuration for Reversi.
    board_put(board, 3, 3, COMPUTER)
    board_put(board, 4, 4, COMPUTER)
    board_put(board, 3, 4, HUMAN)
    board_put(board, 4, 3, HUMAN)
    # Return the newly-created board object.
    return board

def game_turn(board, row, col):
    '''
    board (list): an object returned by board_create()
    row (int): The row coordinate where the piece should be placed.
    col (int): The column coordinate where the piece should be placed.

    Place the human player's piece on the board at the coordinates 
    row, col.

    If the move is not legal, this function will return False.

    If the move is legal, this function will 'flip over' all of the opponent's
    pieces affected by this move.

    It will then allow the computer player to choose and perform a move, 
    turning over all of the human player's affected pieces.
    '''
    if _is_legal_move(board, row, col, HUMAN):
        # Perform the human player's chosen move.
        board_put(board, row, col, HUMAN)
        _do_flips(board, row, col, HUMAN)
        while True:
            moves = _get_legal_moves(board, COMPUTER)
            if len(moves) > 0:
                start_time = time.time()
                row, col = _choose_move(board, moves, COMPUTER)
                print(time.time()-start_time)
                RUNTIME.write(f'{time.time() - start_time}\n')
                # If _choose_move() returns an illegal move, we
                # will catch that here.
                assert _is_legal_move(board, row, col, COMPUTER)
                board_put(board, row, col, COMPUTER)
                _do_flips(board, row, col, COMPUTER)
            else:
                break
            # See if the human has any legal moves left.
            moves = _get_legal_moves(board, HUMAN)
            if len(moves) > 0:
                break
        return True
    else:
        return False

def game_over(board):
    '''Determines if the game is over'''
    if _get_legal_moves(board, HUMAN) == [] and _get_legal_moves(board, COMPUTER) == []:
        return True
    return False

def game_winner(board):
    '''Determines the winner of the game based on points'''
    human_points = board_count(board,HUMAN)
    computer_points = board_count(board,COMPUTER)

    if human_points > computer_points:
        return HUMAN
    
    elif computer_points > human_points:
        return COMPUTER
    
    return 0

def _get_opponent(player):
    '''
    player (int): HUMAN or COMPUTER
    
    Returns the opponent of the given player.
    '''
    if player == HUMAN:
        return COMPUTER
    else:
        return HUMAN

def _get_flips(board, r0, c0, player, opponent):
    '''
    board (list): an object returned from board_create()
    r0 (int): row number of the proposed move.
    c0 (int): column number of the proposed move.
    player (int): HUMAN or COMPUTER
    opponent (int): COMPUTER or HUMAN
    
    Returns a list of tuples (row, column) that would change color if the 
    player moves to position r0,c0. The length of this list will tell you
    how many pieces would flip for this move.

    The algorithm here just starts at the r0,c0 position and searches
    along each of the eight directions for possible pieces to flip.
    '''
    # Reflects the 8 directions relative to a board position.
    deltas = (( 1, 0), (-1, 0), ( 0, 1), ( 0,-1),
              (-1,-1), ( 1, 1), (-1, 1), ( 1,-1))
    result = []
    n_rows = board_rows(board)
    n_cols = board_cols(board)
    for dr, dc in deltas:
        row = r0 + dr
        col = c0 + dc
        # Start assembling possible flips
        possible = []
        while 0 <= row < n_rows and 0 <= col < n_cols:
            if board_get(board, row, col) == opponent:
                possible += [(row, col)]
            elif board_get(board, row, col) == player:
                # If we found one of our anchor pieces, everything
                # up to this position will flip, so this should
                # be saved in the result list.
                result += possible
                break
            else:
                # No anchor piece found, so we won't flip anything
                # along this direction.
                break
            row += dr
            col += dc

    return result

def _is_legal_move(board, row, col, player):
    '''
    board (list): an object created by board_create()
    row (int): the row coordinate of the proposed move.
    col (int): the column coordinate of the proposed move.
    player (int): HUMAN or COMPUTER

    Return True if a given move is legal.
    '''
    if board_get(board, row, col): # Square is occupied.
        return False
    opponent = _get_opponent(player)
    flips = _get_flips(board, row, col, player, opponent)
    return len(flips) != 0      # A move must flip at least one piece.

def _do_flips(board, row, col, player):
    '''
    board (list): an object created by board_create()
    row (int): the row coordinate of the proposed move.
    col (int): the column coordinate of the proposed move.
    player (int): HUMAN or COMPUTER

    Flip all of the appropriate pieces in response to a move.

    Returns None
    '''
    opponent = _get_opponent(player)
    for rp, cp in _get_flips(board, row, col, player, opponent):
        board_put(board, rp, cp, player)
    
def _get_legal_moves(board, player):
    '''
    board (list): an object created by board_create()
    player (int): HUMAN or COMPUTER

    Return a list containing all of the possible legal moves for this 
    player. A move is represented as a tuple of integers of the form
    (row, col).'''
    result = []
    for row in range(board_rows(board)):
        for col in range(board_cols(board)):
            if _is_legal_move(board, row, col, player):
                result += [(row, col)]
    return result

def _choose_move(board, moves, player):
    '''Algorithm to choose the computer's move'''
    #Logic is derived from an online Reversi guide and some basic principles

    #Prioritze/avoid certain squares by assigning a weight to each square
    #Calculate the points each move would make
    #Duplicate the board, play each move, and minimize the points the human can gain
    #Take all 3 factors and calculate a "score" for each move, choose the move with the best score

    def weight_fetcher(move):
        '''Returns the desirability of each square'''

        #Weight table copied from online Reversi strategy guide https://samsoft.org.uk/reversi/strategy.htm
        WEIGHTS = [
            [99, -8, 8, 6, 6, 8, -8,99],
            [-8,-24,-4,-3,-3,-4,-24,-8],
            [ 8, -4, 7, 4, 4, 7, -4, 8],
            [ 6, -3, 4, 0, 0, 4, -3, 6],
            [ 6, -3, 4, 0, 0, 4, -3, 6],
            [ 8, -4, 7, 4, 4, 7, -4, 8],
            [-8,-24,-4,-3,-3,-4,-24,-8],
            [99, -8, 8, 6, 6, 8, -8,99]
        ]

        return WEIGHTS[move[0]][move[1]] + len(_get_flips(board, move[0], move[1], player, _get_opponent(player)))

    def points_gained(board, move, player):
        '''Calculates the point gained by a given move'''
        return len(_get_flips(board, move[0], move[1], player, _get_opponent(player)))

    def move_simulator(board, move):
        '''Simulates the player's potential moves after the computer's move'''
        dupe_board = board_copy(board)  #Duplicates the current board in order to not alter the current game state while simulating
        board_put(dupe_board, move[0], move[1], COMPUTER)   #Place the computer's move
        human_moves = _get_legal_moves(dupe_board, HUMAN)    #Fetches legal human moves

        worst_case = 0  #Intiliaze the value that stores the max amount of points the human can make

        for move in human_moves:    #Iterate over each possible move after computer move
            human_pts = points_gained(board, move, HUMAN)   #Fetch the points of each given move
            if human_pts >= worst_case:
                worst_case = human_pts  #Stores the worst case (highest points for human)
        
        return worst_case


    best_pts = -64    #Sets the baseline low score. This value is chosen to ensure that there is always a move better than this baseline
    best_move = ()    #Tuple to store the best move

    for move in moves:  #Iterate over each possible computer move
        priority = weight_fetcher(move)     #Fetch the desirability of move

        pts_gained = points_gained(board,move,player)   #Fetches the points gained of move
        
        points_given  = move_simulator(board, move)     #Fetches the worst case (max human points) of move

        score = priority + pts_gained - points_given    #Calculates the score of the move

        if score >= best_pts:
            best_pts = score    #Stores the best score possible
            best_move = move    #Stores the best move possible

    return best_move

# TESTING CODE. DO NOT CHANGE ANYTHING AFTER THIS LINE!!
# When running standalone, run a few tests of the provided functions.

if __name__ == "__main__":
    print("Testing the game logic.")
    from random import randint
    # Play ten randomized games and make sure nothing breaks.
    for trial in range(100):
        board = game_start()
        moves = _get_legal_moves(board, HUMAN)
        assert len(moves) == 4
        assert (2, 3) in moves
        assert (3, 2) in moves
        assert (4, 5) in moves
        assert (5, 4) in moves

        assert not game_over(board)

        assert game_turn(board, 3, 2)

        # Now play a game automatically.
        n_turns = 1
        while not game_over(board):
            moves = _get_legal_moves(board, HUMAN)
            if len(moves) > 0:
                assert all(_is_legal_move(board, r, c, HUMAN) for r, c in moves)
                # Select move at random.
                move = moves[randint(0, len(moves) - 1)]
                assert game_turn(board, *move)
            assert n_turns < 64 # avoid possible infinite loop
            n_turns += 1

        if game_over(board):
            assert (not _get_legal_moves(board, HUMAN) and
                    not _get_legal_moves(board, COMPUTER))
            
        n_h = board_count(board, HUMAN)
        n_c = board_count(board, COMPUTER)
        print(f'Human score {n_h} Computer score {n_c}')
        SCORES.write(f"{n_h}, {n_c}\n")
        if n_h > n_c:
            assert game_winner(board) == HUMAN
        elif n_h < n_c:
            assert game_winner(board) == COMPUTER
        else:
            assert game_winner(board) == 0

    print("All tests passed.")
