"""
Support functions for the robot arena case studies

@author: Marco Tinacci
"""

import itertools as it

def comparePos(p1,p2):
    """ Position p2 is in direction dir with respect to p1 """
    if p1 == p2:
        return 'h'
    if p1[0]-1 == p2[0] and p1[1] == p2[1]:
        return 'n'
    if p1[0]+1 == p2[0] and p1[1] == p2[1]:
        return 's'
    if p1[0] == p2[0] and p1[1]+1 == p2[1]:
        return 'e'
    if p1[0] == p2[0] and p1[1]-1 == p2[1]:
        return 'w'
    return 'o'

def step(s,a,dim):
    switcher = {
        'h': (s[0],s[1]),
        'n': (max(s[0]-1,0),s[1]),
        's': (min(s[0]+1,dim-1),s[1]),
        'e': (s[0],min(s[1]+1,dim-1)),
        'w': (s[0],max(s[1]-1,0))
    }
    return switcher[a]

def print_grid(ctrl,env,dim,pause=False):
    """ 
    Print the robot arena 
        ctrl: controller robot position
        env: environment robots positions
        dim: arena dimension
        pause: wait for input after print
    """
    print ctrl,env
    for i,j in it.product(range(dim),range(dim)):
        symb = '.'
        counter = 0
        if ctrl[0] == i and ctrl[1] == j:
            # controller robot
            symb = 'o'
            counter += 1
        #if type(env) is tuple:
        for t in env:
            # environment robot
            if t[0] == i and t[1] == j:
                symb = 'x'
                counter+=1
        if counter > 1:
            # multiple robots
            symb = str(counter)
        if j == dim-1:
            print symb
        else:
            print symb,
    if pause:
        raw_input()

def around(s,dim):
    return {(i,j) for i,j in it.product(range(dim),range(dim)) 
        if (s[0] == i and (s[1] == j-1 or s[1] == j+1))
            or (s[1] == j and (s[0] == i-1 or s[0] == i+1)
            or (s[0] == i and s[1] == j))
    }