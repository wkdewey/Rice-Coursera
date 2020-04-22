# implementation of card game - Memory

import simplegui
import random

# helper function to initialize globals
def new_game():
    global cards
    global exposed
    global state
    global last_pair
    global first_clicked
    global second_clicked
    global turns
    state = 0
    cards = range(8) + range(8)
    random.shuffle(cards)
    exposed = []
    first_clicked = None
    second_clicked = None
    turns = 0
    for i in range(len(cards)):
        exposed.append(False)
        
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global state
    global exposed
    global first_clicked
    global second_clicked
    global turns
    card_clicked = pos[0] // 50
    if exposed[card_clicked] == False:
        exposed[card_clicked] = True
        if state == 0:
            first_clicked = card_clicked
            state = 1
        elif state == 1:
            second_clicked = card_clicked
            turns += 1
            state = 2
        else:
            if cards[first_clicked] != cards[second_clicked]:
                exposed[first_clicked] = False
                exposed[second_clicked] = False
            first_clicked = card_clicked
            state = 1
            
# cards are logically 50x100 pixels in size    
def draw(canvas):
    for i in range(len(cards)):
        if exposed[i] == True:
            canvas.draw_text(str(cards[i]), [10 + 50 * i, 60], 40, "Red")
        if exposed[i] == False:
            canvas.draw_polygon([[50 * i, 0], [50 + 50 * i, 0], 
                                 [50 + 50 * i, 100], [50 * i, 100]],
                                 1, "Black", "Green")
    label.set_text("Turns = " + str(turns))

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric