"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    #print "beginning mm_move with player " + str(SCORES[player])
    #print board
    winner = board.check_win()
    if winner is not None:
        #print "returning score " + str(SCORES[winner]) + " for " + str(SCORES[player])
        return SCORES[winner], (-1, -1)
    possible_squares = board.get_empty_squares()
    max_score = None
    #print "player to move " + str(SCORES[player])
    #print "possible moves " + str(possible_squares)
    for square in possible_squares:
        #print "testing move " + str(square)
        new_board = board.clone()
        new_board.move(square[0], square[1], player)
        score = mm_move(new_board, provided.switch_player(player))[0]
        corrected_score = score * SCORES[player]
        #print "score for move " + str(square) + " is " + str(score)
        #print "for player " + str(SCORES[player])
        if corrected_score > max_score or max_score == None:
            max_score = corrected_score
            best_move = square
            #print "returning max_score of " + str(max_score * SCORES[player]) + " with move " + str(best_move)
        if corrected_score == 1:
            return max_score * SCORES[player], best_move
    #print "returning max_score of " + str(max_score * SCORES[player]) + " with move " + str(best_move)
    return max_score * SCORES[player], best_move            
                       
def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.
#mm_move(provided.TTTBoard(2, False, [[provided.EMPTY, provided.EMPTY], [provided.EMPTY, provided.EMPTY]]), provided.PLAYERX)
#mm_move(provided.TTTBoard(2, False, [[provided.EMPTY, provided.EMPTY], [provided.EMPTY, provided.EMPTY]]), provided.PLAYERO)
