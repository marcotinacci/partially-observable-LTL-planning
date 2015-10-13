# -*- coding: utf-8 -*-
"""
File generator of the robot arena case study
	DxD arena 
	N robots, 1 controller and N-1 random walks
	sensors of the robot have position sensing

@author: Marco Tinacci
"""

from data import lts, mdp, pomdp, belief
from utils import func
from utils import robots as rob
from utils import exportFunctions as exp
from utils import importFunctions as imp 
from utils import scheduler as sched
import sys, os, random, time, subprocess, itertools as it
import numpy as np
import matplotlib.pyplot as plt

# ==== PARAMS ====

# random seed
SEED = time.time()
random.seed(SEED)

# arena dimension
DIM = 3
# number of robots
NROB = 3
# number of parameters
NPAR = NROB * 2 + 1

# simulation run
MAXITER = 100
RUNS = 100
PAUSE = False
PRINT = False
APPEND = False # TODO replace it with check for existing file
# schedulers: 0 = avg, 1 = max, 2 = random, 3 = repulsive
SCHEDULER = 3
INTTYPE = np.int

# phases enabling
MODELGENERATION = False
MODELCHECKING = False
SIMULATION = True
PLOTRESULTS = False

# files and paths
PRISMPATH = '/Applications/prism-4.2.1-osx64/bin/prism'
EXPORTFILENAME = 'export/arena2_D'+str(DIM)+'N'+str(NROB)
FORMULAFILENAME = 'formulae/arena'
PROPNAME = 'avoid2'
TEMPFILENAME = 'export/pmin2_D'+str(DIM)+'N'+str(NROB)+'.txt'
#EXPERIMENTFILENAME = 'experiments/test.npy'
EXPERIMENTFILENAME = 'experiments/arena2_S'+str(SCHEDULER)+ \
	'D'+str(DIM)+'N'+str(NROB)+'.npy'

# ==== LTS controller ==== 
LS = list(it.product(range(DIM),range(DIM)))
LA = ['h','n','s','e','w']
LT = { (s,a):rob.step(s,a,DIM) for s,a in it.product(LS,LA) }
L = lts.lts(LS, LA, LT)

# ==== MDP environment ==== 
if NROB > 2:
	MS = list(it.product(
		it.product(range(DIM),range(DIM)),repeat=NROB-1))
else: # NROB == 2
	MS = list(it.product(range(DIM),range(DIM)))

T = {}
for s1,a in it.product(MS,L.A):
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
P = pomdp.pomdp()
P.initProduct(L,M)

# single observation
single_obs = ['n','s','e','w','h']
# collective observation
P.O = list(func.powerset(single_obs))

# inexpensive state space construction
P.Z = {}
for (l,m) in P.S:
	#print l,m
	if NROB > 2: # TOFIX
		obs_set = set()
		for i in range(NROB-1):
			dir = rob.comparePos(P.L.names[l],P.M.names[m][i])
			if dir != 'o':
				obs_set.add(dir)
		P.Z[(l,m)] = { frozenset(obs_set) : 1 }
	else:
		dir = rob.comparePos(P.L.names[l],P.M.names[m])
		if dir != 'o':
			P.Z[(l,m)] = { frozenset(dir) : 1 }
		else:
			P.Z[(l,m)] = { frozenset({}) : 1 }

# === OFFLINE ===

if MODELGENERATION:
	# implicit MDP out of the POMDP
    implicit = mdp.mdp()
    implicit.initImplicit(P)
    exp.export2sta(implicit, P.L, P.M, P.O, NROB, EXPORTFILENAME+'.sta')
    exp.export2tra(implicit, EXPORTFILENAME+'.tra')
    exp.export2lab(EXPORTFILENAME+'.lab')

if MODELCHECKING:
    command = PRISMPATH + " -importmodel " + EXPORTFILENAME + \
        ".all -mdp " + FORMULAFILENAME + ".props -prop " + \
        PROPNAME + " > " + TEMPFILENAME
    print "-> EXECUTING: " + command
    start = time.time()
    os.system(command)
    end = time.time()
    print "-> DONE (time: "+ str(end-start) + ")"

# === ONLINE ===

if SIMULATION:
	Prob = imp.importProb(TEMPFILENAME,NPAR)
	for run in range(RUNS):
		print "-> RUN "+str(run)
		# crash history
		ch = np.zeros((RUNS,MAXITER+1), dtype=np.int16)
		# controller initial state
		ci = L.names[random.choice(L.S)]
		# environment initial state (non observable)
		ei = M.names[random.choice(M.S)]
		ch[run,0] = 1 if ci in ei else 0
		init = { s for s in P.S if L.names[s[0]] == ci }
		distr = { s:1./len(init) for s in init }
		# initialize belief state
		b = belief.belief(P,P.Z,init=distr)
		# first observation
		o = func.weighted_choice(
			P.Z[((L.inv_names[ci]),(M.inv_names[ei]))])
		if PRINT:
			print 'obs:',list(o)
		# belief update
		b.update(obs=o)
		if PRINT:
			print 'b(s):',b.d[((L.inv_names[ci]),(M.inv_names[ei]))] \
				if ((L.inv_names[ci]),(M.inv_names[ei])) in b.d else 0
			rob.print_grid(ci,ei,DIM,pause=PAUSE)

		for it in range(MAXITER):
			# scheduled choice
			a = None
			if SCHEDULER == 0:
				a = sched.beliefScheduler(b, P, Prob, sched.avgMinVal, verbose=PRINT)
			elif SCHEDULER == 1:
				a = sched.beliefScheduler(b, P, Prob, sched.maxMinVal, verbose=PRINT)
			elif SCHEDULER == 2:
				a = sched.randomScheduler((ci,ei), P)
			elif SCHEDULER == 3:
				a = sched.repulsiveScheduler((ci,ei), P, DIM)
			else:
				raise ValueError("SCHEDULER value is not valid")
			# apply action
			ci = rob.step(ci,a,DIM)
			# TOFIX generalize to NROB
			if type(ei[0]) is tuple:
				ei = (rob.step(ei[0],random.choice(L.A),DIM), 
					rob.step(ei[1],random.choice(L.A),DIM))
			else:
				ei = rob.step(ei,random.choice(L.A),DIM)
			# crash tracking
			ch[run,it+1] = 1 if ci in ei else 0
			# extract observation
			o = func.weighted_choice(
				P.Z[((L.inv_names[ci]),(M.inv_names[ei]))])
			# belief update
			b.update(act=a,obs=o)
			if PRINT:
				print 'act:',a
				print 'obs:', list(o)
				print 'b(s):',b.d[((L.inv_names[ci]),(M.inv_names[ei]))] \
					if ((L.inv_names[ci]),(M.inv_names[ei])) in b.d else 0
				rob.print_grid(ci,ei,DIM, pause=PAUSE)
	if APPEND:
		old = np.load(EXPERIMENTFILENAME, dtype=INTTYPE)
		ch = np.bmat([[old],[ch]])
	np.save(EXPERIMENTFILENAME, ch)

if PLOTRESULTS:
	res = np.load(EXPERIMENTFILENAME, dtype=INTTYPE)
	res = np.sum(res,axis=0)
	res = np.cumsum(res)
	print res
	plt.plot(res)
	plt.show()





