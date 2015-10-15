# -*- coding: utf-8 -*-
"""
Support functions

@author: Marco Tinacci
"""

import random
import itertools as it
import robots as rob

def counter(ci,ei,dim,countType):
    if countType == 0: 
        return 1 if ci in ei else 0
    elif countType == 1:
        return reduce(lambda y,z: y+z, \
            map(lambda x: 1 if ci in rob.around(x,dim) else 0,ei))
    else:
        raise ValueError("countType value is not valid")

def inverseObservation(O):
    return { obs:k for k,obs in enumerate(O)}

def powerset(iterable):
    s = list(iterable)
    temp = [list(it.combinations(s, r)) for r in range(len(s)+1)]
    return [frozenset(el) for t in temp for el in t]

def weighted_choice(choices):
    """ 
    Weighed extraction
        choices: discrete distribution dictionary with elements as keys and 
            probabilities as values (it must be sum 1)
    """
    # total = sum(w for c, w in choices) # total is 1
    r = random.uniform(0, 1)
    upto = 0
    for st,pr in choices.iteritems():
        if upto + pr > r:
            return st
        upto += pr
    assert False, "Shouldn't get here"