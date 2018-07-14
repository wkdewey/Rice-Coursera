# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console
import simplegui
import random

# helper function to start and restart the game
def new_game():
    # initialize global variables used in your code here
    global secret_number
    global guesses_remaining
    if game_range == 100:
        guesses_remaining = 7
    else:
        guesses_remaining = 10
    secret_number = random.randrange(0, game_range)
    print
    print "Guess a number between 0 and " + str(game_range - 1)
    print "You have " + str(guesses_remaining) + " guesses."

# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game
    global game_range
    game_range = 100
    new_game()
       

def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    global game_range
    game_range = 1000
    new_game()
    
def input_guess(guess):
    # main game logic goes here
    global guesses_remaining
    guesses_remaining -= 1
    guess = int(guess)
    print
    print "Guess was " + str(guess) + "."
    if guess > secret_number:
        print "Lower"
    elif guess < secret_number:
        print "Higher"
    else:
        print "Correct"
        new_game()
    print ("You have " + str(guesses_remaining) +
           " guesses remaining")
    if guesses_remaining == 0:
        print "Sorry, out of guesses"
        print
        new_game()
    

    
# create frame
frame = simplegui.create_frame("Guess the number", 200, 200)

# register event handlers for control elements and start frame
inp = frame.add_input("Enter your number", input_guess, 50)
frame.add_button("Range is [0, 100)", range100)
frame.add_button("Range is [0, 1000)", range1000)
frame.start()
range100()
