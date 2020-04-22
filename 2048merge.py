"""
Merge function for 2048 game.
"""

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    # move zeroes to the end
    moved_list = [0 for number in line]
    index = 0
    for number in line:
        if number != 0:
            moved_list[index] = number
            index += 1
    # replace with your code
    paired_list = []
    paired = False
    for index, number in enumerate(moved_list):
        if index < (len(moved_list) - 1):
            if number == moved_list[index + 1] and number != 0 and not paired:
                paired_list.append(number * 2)
                paired_list.append(0)
                paired = True
            elif paired:
                paired = False
            else:
                paired_list.append(number)
        elif not paired:
            paired_list.append(number)
    final_list = [0 for number in line]
    index = 0
    for number in paired_list:
        if number != 0:
            final_list[index] = number
            index += 1
    return final_list
