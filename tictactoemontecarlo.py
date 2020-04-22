"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 80         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player
    
# Add your functions here.
def mc_trial(board, player):
    """
    given a board and next player, makes random moves until board is full
    """
    
    while board.check_win() == None:
        empty_squares = board.get_empty_squares()
        chosen_square = random.choice(empty_squares)
        board.move(chosen_square[0], chosen_square[1], player) 
        player = provided.switch_player(player)

def mc_update_scores(scores, board, player):
    """
    Updates the scores for each square, given a board which represents a completed game, and the current player
    """
    dim = board.get_dim()
    winner = board.check_win()
    if winner == player:
        flip = 1
    else:
        flip = -1
    if winner == provided.DRAW:
        pass
    else:
        for row in range(dim):
            for col in range(dim):
                square = board.square(row, col)
                if square == player:
                    scores[row][col] += (SCORE_CURRENT) * flip
                elif square == provided.EMPTY:
                    pass
                else:
                    scores[row][col] += (-SCORE_OTHER) * flip
    print "Updating scores:" + str(scores)

def get_best_move(board, scores):
    """
    Given a tic tac toe board and a list of scores, returns a move with maximum score
    """
    possibilities = []
    empty_squares = board.get_empty_squares()
    relevant_scores = []
    for square in empty_squares:
        score = scores[square[0]][square[1]]
        relevant_scores.append(score)
    max_score = max(relevant_scores)
    for square in empty_squares:
        if scores[square[0]][square[1]] == max_score:
            possibilities.append(square)
    #print possibilities
    choice = random.choice(possibilities)
    #print choice
    return choice

def mc_move(board, player, trials):
    """
    Given a board, the current player, and a number of trials, runs that number of trial games
    and chooses the best move based on these trials
    """
    dim = board.get_dim()
    scores = [[0 for dummy_row in range(dim)] for dummy_col in range(dim)]
    for dummy_trial in range(trials):
        temp_board = board.clone()
        mc_trial(temp_board, player)
        mc_update_scores(scores, temp_board, player)
    return get_best_move(board, scores)

# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

provided.play_game(mc_move, NTRIALS, False)        
#poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)