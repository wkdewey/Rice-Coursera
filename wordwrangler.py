"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    no_duplicates = []
    for index in range(len(list1)):
        if list1[index] != list1[index - 1] or index == 0:
            no_duplicates.append(list1[index])
    return no_duplicates

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    intersection = []
    for element in list1:
        if element in list2:
            intersection.append(element)
    return intersection

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing those elements that are in
    either list1 or list2.

    This function can be iterative.
    """
    merged_list = []
    first_list = list(list1)
    second_list = list(list2)
    while len(first_list) > 0 or len(second_list) > 0:
        if len(first_list) == 0:
            merged_list.extend(second_list)
            second_list = []
        elif len(second_list) == 0:
            merged_list.extend(first_list)
            first_list = []
        elif first_list[0] <= second_list[0]:
            merged_list.append(first_list[0])
            first_list.pop(0)
        else:
            merged_list.append(second_list[0])
            second_list.pop(0)
            
    return merged_list
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    midpoint = int(len(list1) / 2)
    first_list = list1[0:midpoint]
    second_list = list1[midpoint:len(list1)]
    print "merging " + str(first_list) + " and " + str(second_list)
    merged_list = []
    if len(first_list) == 0:
        merged_list = second_list
    elif len(second_list) == 0:
        merged_list = first_list
    elif len(first_list) == 1 and len(second_list) == 1:
        merged_list = merge(first_list, second_list)
    else:
        first_list = merge_sort(first_list)
        print "first list after merge sort " + str(first_list)
        second_list = merge_sort(second_list)
        print "second list after merge sort " + str(second_list)
        merged_list = merge(first_list, second_list)
    return merged_list

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    if word == '':
        return ['']
    first = word[0]
    rest = word[1:]
    rest_strings = gen_all_strings(rest)
    new_strings = [first]
    for string in rest_strings:
        print "string in rest_strings " + string
        for index in range(len(string)):
            half1 = string[:index]
            half2 = string[index:]
            print "1. " + half1 + " 2. " + first + " 3. " + half2
            new_string = half1 + first + half2
            print "new_string " + new_string
            new_strings.append(new_string)
            if index == 0:
                new_strings.append(half2 + first)
    rest_strings.extend(new_strings)
    return rest_strings
        

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    return []

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
# run()
#print merge_sort([2, 6, 8, 10])
print str(gen_all_strings('ab'))  
    