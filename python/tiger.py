# -*- coding: utf-8 -*-
"""
@author: Marco Tinacci
"""

from data import lts, mdp, pomdp, belief
from utils import func
from utils import exportFunctions as exp
from utils import importFunctions as imp 
from utils import scheduler as sched
import sys, os, random, time, subprocess, itertools as it
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Pool


# ==== PARAMS ====
# random seed
SEED = time.time()
random.seed(SEED)
# number of parameters
NPAR = 3

# simulation run
MAXITER = 5
RUNS = 10
PAUSE = False
PRINT = False
APPEND = False # TODO replace it with check for existing file
# schedulers: 0 = avg, 1 = max, 2 = random, 3 = repulsive
SCHEDULER = 0
INTTYPE = np.int16

# phases enabling
MODELGENERATION = False
MODELCHECKING = False
SIMULATION = True

# files and paths
# legend: 
#	C: counter measure, 
#	S: scheduler, 
#	D: dimension, 
#	N: number of robots
FILENAME = os.path.splitext(os.path.basename(__file__))[0]
PRISMPATH = '/Applications/prism-4.3-osx64/bin/prism'
EXPORTFILENAME = FILENAME+'/export_models/'+FILENAME
FORMULAFILENAME = FILENAME+'/formulae/'+FILENAME
PROPNAME = "open" # check formulae/arena.props for formula names
PRISMFILENAME = FILENAME+'/export_prism_results/pmin_'+PROPNAME+'.txt'
EXPERIMENTFILENAME = FILENAME+'/export_results/arena_'+PROPNAME+'_S'+str(SCHEDULER)+'.npy'

# ==== LTS controller ==== 
# single state controller
LS = [ 0 ]
# listen, open left, open right
LA = ['l', 'ol', 'or']
LT = { 
	(0,'l') : 0, 
	(0,'ol') : 0, 
	(0,'or') : 0
}
L = lts.lts(LS, LA, LT)

# ==== MDP environment ==== 
# tiger left, tiger right, win, lose
MS = ['tl', 'tr', 'win', 'lose']

MT = {
	('tl','l') : { 'tl' : 1 },
	('tl','ol') : { 'lose' : 1 },
	('tl','or') : { 'win' : 1 },
	('tr','l') : { 'tr' : 1 },
	('tr','ol') : { 'win' : 1 },
	('tr','or') : { 'lose' : 1 },
	('win','l') : { 'win' : 1 },
	('win','ol') : { 'win' : 1 },
	('win','or') : { 'win' : 1 },
	('lose','l') : { 'lose' : 1 },
	('lose','ol') : { 'lose' : 1 },
	('lose','or') : { 'lose' : 1 }
}

M = mdp.mdp(MS,L.A,MT)

# ==== POMDP partially observable ====
P = pomdp.pomdp()
P.initProduct(L,M)

# observations
P.O = ['hl','hr']

# observation function
P.Z = {
	(0,P.M.inv_names['tl']) : {'hl' : 0.85, 'hr' : 0.15},
	(0,P.M.inv_names['tr']) : {'hl' : 0.15, 'hr' : 0.85},
	(0,P.M.inv_names['win']) : {'hl' : 0.5, 'hr' : 0.5},
	(0,P.M.inv_names['lose']) : {'hl' : 0.5, 'hr' : 0.5}
}

# === OFFLINE ===

if MODELGENERATION:
	if os.path.isfile(EXPORTFILENAME+'.sta'):
		print "WARINING: Model files already exist, delete them to generate them again"
	else:
		# explicit MDP out of the POMDP
	    print "-> MODEL GENERATION"
	    start = time.time()

	    explicit = mdp.mdp()
	    explicit.initExplicit(P)
	    exp.export2sta(explicit, P.L, P.M, P.O, "(c,pos,obs)", EXPORTFILENAME+'.sta')
	    exp.export2tra(explicit, EXPORTFILENAME+'.tra')
	    exp.export2lab(EXPORTFILENAME+'.lab')
	    
	    end = time.time()
	    print "-> DONE (time: "+ str(end-start) + ")"

if MODELCHECKING:
	if os.path.isfile(PRISMFILENAME):
		print "WARNING: Probability file already exists, delete it to generate it again"
	else:
	    command = PRISMPATH + " -importmodel " + EXPORTFILENAME + \
	        ".all -mdp " + FORMULAFILENAME + ".props -prop " + \
	        PROPNAME + " > " + PRISMFILENAME
	    print "-> EXECUTING: " + command
	    start = time.time()
	    os.system(command)
	    end = time.time()
	    print "-> DONE (time: "+ str(end-start) + ")"

if SIMULATION:
	Prob = imp.importProb(PRISMFILENAME,NPAR)

	for run in range(RUNS):
		#sim((run, Prob, P))
		print "-> RUN "+str(run)
		# controller initial state
		ci = L.names[random.choice(L.S)]
		# environment initial state (not observable)
		ei = 'tl' #M.names[random.choice([M.inv_names['tl'],M.inv_names['tr']])]

		init = { s for s in P.S if P.L.names[s[0]] == ci }
		distr = {(0,M.inv_names['tl']):0.5, (0,M.inv_names['tr']):0.5}
		# initialize belief state
		b = belief.belief(P,P.Z,init=distr)
		# first observation
		o = func.weighted_choice(
			P.Z[((L.inv_names[ci]),(M.inv_names[ei]))])
		# belief update
		print 'init: ', b.d
		b.update(obs=o)
		if PRINT:
			print 'b(s):',b.d[((L.inv_names[ci]),(M.inv_names[ei]))] \
				if ((L.inv_names[ci]),(M.inv_names[ei])) in b.d else 0

		for it in range(MAXITER):
			print 'belief: ', b.d
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
			print 'choice: ', a
			# apply action
			ci = L.T[(ci,a)]
			ei = M.names[func.weighted_choice(M.T[(M.inv_names[ei],a)])]
			# extract observation
			o = func.weighted_choice(P.Z[(ci,M.inv_names[ei])])

			# belief update
			b.update(act=a,obs=o)
			if PRINT:
				print 'act:',a
				print 'obs:', list(o)
				print 'b(s):',b.d[((P.L.inv_names[ci]),(P.M.inv_names[ei]))] \
					if ((L.inv_names[ci]),(M.inv_names[ei])) in b.d else 0
				rob.print_grid(ci,ei,DIM, pause=PAUSE)
		#print "END RUN "+ str(run)

	#if APPEND:
	#	ch_old = np.load(EXPERIMENTFILENAME, dtype=INTTYPE)
	#	ch = np.bmat([[ch_old],[ch]])
	#np.save(EXPERIMENTFILENAME, ch)
