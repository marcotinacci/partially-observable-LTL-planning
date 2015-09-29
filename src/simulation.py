# -*- coding: utf-8 -*-
"""
@author: Marco Tinacci
"""

from data import mdp
from data import belief
import robots as cs
import random

# implicit MDP out of the POMDP
imp = mdp.mdp()
imp.initImplicit(cs.P)

# precomputed probability matrix for each position of the 3x3 arena
Prob = [
    [0.19753086419858046, 0.027777777778000057, 0.19753086419858046],
    [0.027777777778000057, 0.012345679013431976, 0.027777777778000057],
    [0.19753086419858046, 0.027777777778000057, 0.19753086419858046]
]

# controller initial state
ci = 's0'
# environment initial state (non observable)
ei = random.choice(cs.M.S)
# initialize belief state
b = belief.belief(imp,cs.P.Z)

cs.print_grid(ei,cs.dim,pause=True)
# simulation run
maxiter = 10
for i in range(maxiter):
    # extract observation ...

    # random choice
    a = random.choice(cs.L.A)
    b.update(a)
    ei = (cs.step(ei[0],a,cs.dim),
        cs.step(ei[1],random.choice(cs.L.A),cs.dim),
        cs.step(ei[2],random.choice(cs.L.A),cs.dim))
    print 'action:',a
    cs.print_grid(ei,cs.dim,pause=True)


    
    

    