# -*- coding: utf-8 -*-
"""
Simulation of the robot arena case study
    DxD arena 
    3 robots, 1 controller and 2 random walks
    sensors of the robot have some/none observations

@author: Marco Tinacci
"""

from data import lts, mdp, pomdp, belief
from utils import func
from utils import robots as rob
from utils import exportFunctions as exp
from utils import importFunctions as imp 
from utils import scheduler as sched
import sys, os, random, time, subprocess, itertools as it

# ==== PARAMS ====

# random seed
SEED = time.time()
random.seed(SEED)

# arena dimension
DIM = 4
# number of robots
NROB = 3
# number of parameters
NPAR = NROB * 2 + 1

# simulation run
MAXITER = 10
PAUSE = False

# phases enabling
MODELGENERATION = False
MODELCHECKING = False
SIMULATION = True

# files
PRISMPATH = '/Applications/prism-4.2.1-osx64/bin/prism'
filename = 'export/arena1_D'+str(DIM)+'N'+str(NROB) # no extention
formulaeFileName = 'formulae/arena'
propName = 'avoid1'
tempFileName = 'export/pmin1_D'+str(DIM)+'N'+str(NROB)+'.txt'

# ==== LTS controller ==== 
LS = list(it.product(range(DIM),range(DIM)))
LA = ['h','n','s','e','w']
LT = { (s,a):rob.step(s,a,DIM) for s,a in it.product(LS,LA) }
L = lts.lts(LS, LA, LT)

# ==== MDP environment ==== 
print "-> MDP"
if NROB > 2:
    MS = list(it.product(
        it.product(range(DIM),range(DIM)),repeat=NROB-1))
else: # NROB == 2
    MS = list(it.product(range(DIM),range(DIM)))

print "--> TRANSITION FUNCTION GENERATION"
T = {}
for s1,a in it.product(MS,L.A):
    # TOFIX
    if NROB == 2:
        S2 = rob.around(s1,DIM)
    else: # NROB > 2
        S2 = rob.around(s1[0],DIM)
        for i in range(1,NROB-1):
            S2 = list(it.product(S2,rob.around(s1[i],DIM)))
    p = 1.0 / float(len(S2))
    T[(s1,a)] = {}
    for s2 in S2:
        s = (s2[0],s2[1])
        T[(s1,a)][s] = p

M = mdp.mdp(MS,L.A,T)

# ==== POMDP partially observable ====
print "-> POMDP"
print "--> INIT PRODUCT POMDP"
P = pomdp.pomdp()
P.initProduct(L,M)

print "--> OBSERVATION FUNCTION"
P.O = ['some','none']

# inexpensive state space construction
P.Z = {}
for (l,m) in P.S:
    #print l,m
    if NROB > 2: # TOFIX
        obs_set = set()
        for i in range(NROB-1):
            dir = rob.comparePos(P.L.names[l],P.M.names[m][i])
            if dir != 'o':
                P.Z[(l,m)] = { 'some' : 1 }
            else:
                P.Z[(l,m)] = { 'none' : 1 }
    else:
        dir = rob.comparePos(P.L.names[l],P.M.names[m])
        if dir != 'o':
            P.Z[(l,m)] = { 'some' : 1 }
        else:
            P.Z[(l,m)] = { 'none' : 1 }

# === OFFLINE ===

if MODELGENERATION:
    # implicit MDP out of the POMDP
    print "-> MODEL GENERATION"
    imp = mdp.mdp()
    imp.initImplicit(P)
    print "--> export sta"
    exp.export2sta(imp, P.L, P.M, P.O, NROB, filename+'.sta')
    print "--> export tra"
    exp.export2tra(imp, filename+'.tra')
    print "--> export lab"
    exp.export2lab(filename+'.lab')

if MODELCHECKING:
    print "-> MODEL CHECKING"
    command = PRISMPATH + " -importmodel " + filename + \
        ".all -mdp " + formulaeFileName + ".props -prop " + \
        propName + " > " + tempFileName
    print "--> EXECUTING: " + command
    start = time.time()
    os.system(command)
    end = time.time()
    print "--> DONE (time: "+ str(end-start) + ")"

# === ONLINE ===

if SIMULATION:
    Prob = imp.importProb(tempFileName,NPAR)
    # controller initial state
    ci = (1,1)
    # environment initial state (non observable)
    ei = M.names[random.choice(M.S)]
    # initialize belief state
    b = belief.belief(P,P.Z)

    #print "ci:"+str(ci),"ei:" + str(ei)
    rob.print_grid(ci,ei,DIM,pause=PAUSE)
    for i in range(MAXITER):
        # scheduled choice
        #a = random.choice(cs.L.A)
        maximum = -1
        act_max = None
        for a in L.A:
            ba = b.returnUpdate(act=a)
            val = sched.avgMinScheduler(ba,Prob,P)
            #val = rob.opt(ba,Prob,P)
            if round(val,10) == round(maximum,10):
                act_max.add(a)
                print 'EQ act:',a,' - val:',val
            elif val > maximum:
                maximum = val
                act_max = {a}
                print 'OK act:',a,' - val:',val
            else:
                print 'NO act:',a,' - val:',val
                pass
        a = random.choice(list(act_max))
        # apply action
        ci = rob.step(ci,a,DIM)
        ei = (rob.step(ei[0],random.choice(L.A),DIM), 
            rob.step(ei[1],random.choice(L.A),DIM))
        # extract observation
        o = func.weighted_choice(P.Z[(L.inv_names[ci],M.inv_names[ei])])
        # belief update
        b.update(act=a,obs=o)
        print 'act:',a
        print 'obs:',o
        print 'b(s):',b.d[(L.inv_names[ci],M.inv_names[ei])] \
            if (L.inv_names[ci],M.inv_names[ei]) in b.d else 0
        rob.print_grid(ci,ei,DIM,pause=PAUSE)
