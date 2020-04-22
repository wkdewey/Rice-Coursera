"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(200)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set



def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    max_score = 0.0
    for value in range(1, 7):
        temp_score = 0
        for die in hand:
            if die == value:
                temp_score += die
        if temp_score > max_score:
            max_score = temp_score
    return max_score


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    
    possible_rolls = list(gen_all_sequences(range(1, num_die_sides+1), num_free_dice))
    trials = 0
    total_score = 0.0
    for possible_roll in possible_rolls:
        trials += 1
        trial_hand = held_dice + possible_roll
        total_score = total_score + score(trial_hand)
    return total_score/trials


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    answer_set = set([()])
    for dummy_idx in range(len(hand)):
        temp_set = set()
        for partial_sequence in answer_set:
            temp_hand = list(hand)
            for item in partial_sequence:
                temp_hand.remove(item)
            for item in temp_hand:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                new_sequence.sort()
                temp_set.add(tuple(new_sequence))
            answer_set = answer_set.union(temp_set)
    return answer_set





def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    holds = list(gen_all_holds(hand))
    print holds
    values = []
    for hold in holds:
        held_dice = hold
        num_free_dice = len(hand) - len(held_dice)
        values.append(expected_value(held_dice, num_die_sides, num_free_dice))
    print values
    max_value = max(values)
    print max_value
    ans = holds[values.index(max_value)]
    return (max_value, ans)


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
    
run_example()

#print expected_value((2, 2), 6, 2)
#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)
                                       
    
    
    



