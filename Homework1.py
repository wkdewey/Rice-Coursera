def appendsums(lst):
    """ 
    Repeatedly append the sum of the current last three elements 
    of lst to lst. 
    """
    
    for i in range(25):
        to_append = lst[-3] + lst[-2] + lst[-1]
        lst.append(to_append)

sum_three = [0, 1, 2]
appendsums(sum_three)
print sum_three
print sum_three[10]
print sum_three[20]
