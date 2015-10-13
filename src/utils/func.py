# -*- coding: utf-8 -*-
"""
Support functions

@author: Marco Tinacci
"""

import random
import itertools as it

def inverseObservation(O):
    return { obs:k for k,obs in enumerate(O)}

def powerset(iterable):
    # "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    # temp = [it.combinations(s, r) for r in range(len(s)+1)]
    # return map(lambda x:frozenset(x),temp)
    # "powerset([1,2,3]) --> fs{} fs{1} fs{2} fs{3} fs{1,2} fs{1,3} fs{2,3} fs{1,2,3}"
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