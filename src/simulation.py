# -*- coding: utf-8 -*-
"""
@author: Marco Tinacci
"""

from data import belief
import robots as cs
import random
import time

# === INIT ===

# random seed
#random.seed(1)
random.seed(time.time()) 

# simulation run
MAXITER = 100

# implicit MDP out of the POMDP
#imp = mdp()
#imp.initImplicit(cs.P)

# precomputed probability matrix for each position of the 3x3 arena
# from the property filter(max,Pmin=? [G<=2 (obs=0)], (x0=0 & y0=1 & obs=0))
# i.e. the maximum minimum probability to never perceive any robot within two 
# steps starting from a specific position
Prob = [
    [0.19753086419858046, 0.027777777778000057, 0.19753086419858046],
    [0.027777777778000057, 0.012345679013431976, 0.027777777778000057],
    [0.19753086419858046, 0.027777777778000057, 0.19753086419858046]
]

# controller initial state
ci = (1,1)
# environment initial state (non observable)
ei = random.choice(cs.M.S)
# initialize belief state
b = belief.belief(cs.P,cs.P.Z)

# === SIMULATION ===
cs.print_grid(ci,ei,cs.dim,pause=True)
for i in range(MAXITER):
    # scheduled choice
    #a = random.choice(cs.L.A)
    maximum = -1
    act_max = None
    for a in cs.L.A:
        ba = b.returnUpdate(act=a)
        val = cs.opt(ba,Prob,cs.P)
        if round(val,10) == round(maximum,10):
            act_max.add(a)
            print 'EV act:',a,' - val:',val
        elif val > maximum:
            maximum = val
            act_max = {a}
            print 'OK act:',a,' - val:',val
        else:
            print 'NO act:',a,' - val:',val
    a = random.choice(list(act_max))
    # apply action
    ci = cs.step(ci,a,cs.dim)
    ei = (cs.step(ei[0],random.choice(cs.L.A),cs.dim), cs.step(ei[1],random.choice(cs.L.A),cs.dim))
    # extract observation
    o = cs.weighted_choice(cs.P.Z[((ci),(ei))])
    # belief update
    b.update(act=a,obs=o)
    print 'act:',a
    print 'obs:',o
    print 'b(s):',b.d[((ci),(ei))] if ((ci),(ei)) in b.d else 0
    cs.print_grid(ci,ei,cs.dim,pause=True)


    
    

    