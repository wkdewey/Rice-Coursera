# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []	# create Hand object
    

    def __str__(self):
        string = ""
        for card in self.cards:
            string += str(card)
            string += " "
            
            
        return "Hand contains " + string	# return a string representation of a hand

    def add_card(self, card):
        self.cards.append(card)	# add a card object to a hand

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        card_values = []
        for card in self.cards:
            card_values.append(VALUES[card.get_rank()])
        hand_value = sum(card_values)
        # compute the value of the hand, see Blackjack video
        if 1 not in card_values:
            return hand_value
        elif hand_value + 10 <= 21:
            hand_value += 10
            return hand_value
        else:
            return hand_value
        
    def draw(self, canvas, pos):
        for card in self.cards:
            card.draw(canvas, pos)
            pos[0] += CARD_SIZE[0] + 10 # draw a hand on the canvas, use the draw method for cards
    
 
        
# define deck class 
class Deck:
    def __init__(self):
        self.deck = [Card(suit, rank) for suit in SUITS for rank in RANKS] # create a Deck object

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck) # use random.shuffle()

    def deal_card(self):
        card = self.deck.pop(0)
        return card	# deal a card object from the deck
    
    def __str__(self):
        string = "Deck contains "
        for card in self.deck:
            string += str(card)
            string += " "
        return string# return a string representing the deck





#define event handlers for buttons
def deal():
    global outcome, in_play, deck, player_hand, dealer_hand, hands, score

    # your code goes here
    if in_play:
        score -= 1
    deck = Deck()
    deck.shuffle()
    player_hand = Hand()
    dealer_hand = Hand()
    hands = [player_hand, dealer_hand]
    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    in_play = True
    outcome = "Hit or stand?"

def hit():
    # replace with your code below
    global in_play, outcome, score
    # if the hand is in play, hit the player
    if in_play:
        player_hand.add_card(deck.deal_card())
    # if busted, assign a message to outcome, update in_play and score
    if 21 < player_hand.get_value():
        outcome = "You have busted. Dealer wins. New deal?"
        in_play = False
        score -= 1
    
def stand():
    # replace with your code below
    global in_play, outcome, score
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        while dealer_hand.get_value() <= 17:
            dealer_hand.add_card(deck.deal_card())
    else:
        return
    # assign a message to outcome, update in_play and score
    in_play = False
    if dealer_hand.get_value() > 21:
        outcome = "Dealer has busted. Player Wins. New deal?"
        score += 1
    elif player_hand.get_value() > dealer_hand.get_value():
        outcome = "Player wins. New deal?"
        score += 1
    else:
        outcome = "Dealer wins. New deal?"
        score -= 1

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text("BLACKJACK", [50, 40], 30, "Black")
    pos = [50, 50]
    for hand in hands:
        hand.draw(canvas, pos)
        pos[1] += CARD_SIZE[1] * 2
        pos[0] = 50
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [50 + CARD_CENTER[0], pos[1] - CARD_SIZE[1] * 2+ CARD_CENTER[1]], CARD_BACK_SIZE)
    canvas.draw_text(outcome, [50, 50 + CARD_SIZE[1] + CARD_CENTER[1]], 30, "Black")
    canvas.draw_text("Score: " + str(score), [50, 50 + CARD_SIZE[1] * 3 + CARD_CENTER[1]], 30, "Black")
    
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric