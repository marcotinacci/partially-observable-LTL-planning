# -*- coding: utf-8 -*-
"""
File generator of the robot arena case study
	DxD arena 
	N robots, 1 controller and N-1 random walks
	sensors of the robot have position sensing

@author: Marco Tinacci
"""

# TODO generalize to N environment robots
# TODO wrap it up and run simulations in parallel

from data import lts, mdp, pomdp, belief
from utils import func
from utils import robots as rob
from utils import exportFunctions as exp
from utils import importFunctions as imp 
from utils import scheduler as sched
import sys, os, random, time, subprocess, itertools as it
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Pool

name, argdim, argsched, argcounter, argprop = sys.argv

# ==== PARAMS ====
# random seed
SEED = time.time()
random.seed(SEED)

# arena dimension
DIM = int(argdim)
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
SCHEDULER = int(argsched)
INTTYPE = np.int16
# counting functions: 0 = collisions, 1 = tracking
COUNTER = int(argcounter)

# phases enabling
MODELGENERATION = False
MODELCHECKING = True
SIMULATION = False

# files and paths
# legend: 
#	C: counter measure, 
#	S: scheduler, 
#	D: dimension, 
#	N: number of robots
PRISMPATH = '/Applications/prism-4.2.1-osx64/bin/prism'
EXPORTFILENAME = 'export_models/arena_D'+str(DIM)+'N'+str(NROB)
FORMULAFILENAME = 'formulae/arena'
PROPNAME = argprop # check formulae/arena.props for formula names
PRISMFILENAME = 'export_prism_results/pmin_'+PROPNAME+'_D'+str(DIM)+'N'+str(NROB)+'.txt'
EXPERIMENTFILENAME = 'export_results/arena_'+PROPNAME+'_C'+str(COUNTER)+ \
	'S'+str(SCHEDULER)+'D'+str(DIM)+'N'+str(NROB)+'.npy'

# ==== LTS controller ==== 
LS = list(it.product(range(DIM),range(DIM)))
LA = ['h','n','s','e','w']
LT = { (s,a):rob.step(s,a,DIM) for s,a in it.product(LS,LA) }
L = lts.lts(LS, LA, LT)

# ==== MDP environment ==== 
#if NROB > 2:
MS = list(it.product(it.product(range(DIM),range(DIM)),repeat=NROB-1))
#else: # NROB == 2
#	MS = list(it.product(range(DIM),range(DIM)))

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
P = pomdp.pomdp()
P.initProduct(L,M)

# single observation
single_obs = ['n','s','e','w','h']
# collective observation
P.O = list(func.powerset(single_obs))

# inexpensive state space construction
P.Z = {}
for (l,m) in P.S:
	# print l,m
#	if NROB > 2:
	obs_set = set()
	for i in range(NROB-1):
		dir = rob.comparePos(P.L.names[l],P.M.names[m][i])
		if dir != 'o':
			obs_set.add(dir)
	P.Z[(l,m)] = { frozenset(obs_set) : 1 }
#	else:
#		dir = rob.comparePos(P.L.names[l],P.M.names[m])
#		if dir != 'o':
#			P.Z[(l,m)] = { frozenset(dir) : 1 }
#		else:
#			P.Z[(l,m)] = { frozenset({}) : 1 }

# === OFFLINE ===

if MODELGENERATION:
	if os.path.isfile(EXPORTFILENAME+'.sta'):
		print "WARINING: Model files already exist, delete them to generate them again"
	else:
		# implicit MDP out of the POMDP
	    print "-> MODEL GENERATION"
	    start = time.time()

	    implicit = mdp.mdp()
	    implicit.initImplicit(P)
	    exp.export2sta(implicit, P.L, P.M, P.O, NROB, EXPORTFILENAME+'.sta')
	    exp.export2tra(implicit, EXPORTFILENAME+'.tra')
	    exp.export2lab(EXPORTFILENAME+'.lab')
	    
	    end = time.time()
	    print "-> DONE (time: "+ str(end-start) + ")"

if MODELCHECKING:
	if os.path.isfile(PRISMFILENAME):
		print "WARINING: Probability file already exists, delete it to generate it again"
	else:
	    command = PRISMPATH + " -importmodel " + EXPORTFILENAME + \
	        ".all -mdp " + FORMULAFILENAME + ".props -prop " + \
	        PROPNAME + " > " + PRISMFILENAME
	    print "-> EXECUTING: " + command
	    start = time.time()
	    os.system(command)
	    end = time.time()
	    print "-> DONE (time: "+ str(end-start) + ")"

# === ONLINE ===

#def sim(args):
#	global PRINT, DIM, PAUSE, MAXITER, SCHEDULER
#	run, Prob, P = args
#	print "-> RUN "+str(run)
#	# crash history
#	#ch = np.zeros((RUNS,MAXITER+1), dtype=INTTYPE)
#	ch = np.zeros(MAXITER+1, dtype=INTTYPE)
#	# track history
#	#th = np.zeros((RUNS,MAXITER+1), dtype=INTTYPE)
#	th = np.zeros(MAXITER+1, dtype=INTTYPE)
#	# controller initial state
#	ci = L.names[random.choice(P.L.S)]
#	# environment initial state (non observable)
#	ei = M.names[random.choice(P.M.S)]
#	# data tracking		
#	ch[0] = 1 if ci in ei else 0
#	th[0] = 1 if \
#		reduce( lambda y,z: y or z, map(lambda x:ci in rob.around(x,DIM),ei)) \
#		else 0
#	init = { s for s in P.S if P.L.names[s[0]] == ci }
#	distr = { s:1./len(init) for s in init }
#	# initialize belief state
#	b = belief.belief(P,P.Z,init=distr)
#	# first observation
#	o = func.weighted_choice(
#		P.Z[((P.L.inv_names[ci]),(P.M.inv_names[ei]))])
#	# belief update
#	b.update(obs=o)
#	if PRINT:
#		print 'b(s):',b.d[((P.L.inv_names[ci]),(P.M.inv_names[ei]))] \
#			if ((P.L.inv_names[ci]),(P.M.inv_names[ei])) in b.d else 0
#		rob.print_grid(ci,ei,DIM,pause=PAUSE)
#
#	for it in range(MAXITER):
#		# scheduled choice
#		a = None
#		if SCHEDULER == 0:
#			a = sched.beliefScheduler(b, P, Prob, sched.avgMinVal, verbose=PRINT)
#		elif SCHEDULER == 1:
#			a = sched.beliefScheduler(b, P, Prob, sched.maxMinVal, verbose=PRINT)
#		elif SCHEDULER == 2:
#			a = sched.randomScheduler((ci,ei), P)
#		elif SCHEDULER == 3:
#			a = sched.repulsiveScheduler((ci,ei), P, DIM)
#		else:
#			raise ValueError("SCHEDULER value is not valid")
#		# apply action
#		ci = rob.step(ci,a,DIM)
#		# TOFIX generalize to NROB
#		if type(ei[0]) is tuple:
#			ei = (rob.step(ei[0],random.choice(P.L.A),DIM), 
#				rob.step(ei[1],random.choice(P.L.A),DIM))
#		else:
#			ei = rob.step(ei,random.choice(P.L.A),DIM)
#		# data tracking
#		ch[it+1] = 1 if ci in ei else 0
#		th[it+1] = 1 if \
#			reduce( lambda y,z: y or z, map(lambda x:ci in rob.around(x,DIM),ei)) \
#			else 0
#		# extract observation
#		o = func.weighted_choice(
#			P.Z[((P.L.inv_names[ci]),(P.M.inv_names[ei]))])
#		# belief update
#		b.update(act=a,obs=o)
#		if PRINT:
#			print 'act:',a
#			print 'obs:', list(o)
#			print 'b(s):',b.d[((P.L.inv_names[ci]),(P.M.inv_names[ei]))] \
#				if ((P.L.inv_names[ci]),(P.M.inv_names[ei])) in b.d else 0
#			rob.print_grid(ci,ei,DIM, pause=PAUSE)
#	print "END RUN "+ str(run)
#	return ch,th

if SIMULATION:
	Prob = imp.importProb(PRISMFILENAME,NPAR)
	ch = np.zeros((RUNS,MAXITER+1), dtype=INTTYPE)

#	pool = Pool()
#	results = pool.map(sim, [ (run,Prob,P) for run in range(RUNS) ])
#	pool.close()
#	pool.join()
#	# split counters
#	ch_res = map(lambda a:a[0],results)
#	th_res = map(lambda a:a[1],results)
#	# merge rows
#	ch = np.vstack(ch_res)
#	th = np.vstack(th_res)

	for run in range(RUNS):
		#sim((run, Prob, P))
		print "-> RUN "+str(run)
		# count history
		#ch = np.zeros(MAXITER+1, dtype=INTTYPE)
		# controller initial state
		ci = L.names[random.choice(L.S)]
		# environment initial state (non observable)
		ei = M.names[random.choice(M.S)]
		# data tracking		
		ch[run,0] = func.counter(ci,ei,DIM,COUNTER)
		init = { s for s in P.S if P.L.names[s[0]] == ci }
		distr = { s:1./len(init) for s in init }
		# initialize belief state
		b = belief.belief(P,P.Z,init=distr)
		# first observation
		o = func.weighted_choice(
			P.Z[((L.inv_names[ci]),(M.inv_names[ei]))])
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
			# data tracking
			ch[run,it+1] = func.counter(ci,ei,DIM,COUNTER)
			# extract observation
			o = func.weighted_choice(
				P.Z[((L.inv_names[ci]),(M.inv_names[ei]))])
			# belief update
			b.update(act=a,obs=o)
			if PRINT:
				print 'act:',a
				print 'obs:', list(o)
				print 'b(s):',b.d[((P.L.inv_names[ci]),(P.M.inv_names[ei]))] \
					if ((L.inv_names[ci]),(M.inv_names[ei])) in b.d else 0
				rob.print_grid(ci,ei,DIM, pause=PAUSE)
		#print "END RUN "+ str(run)

	if APPEND:
		ch_old = np.load(EXPERIMENTFILENAME, dtype=INTTYPE)
		ch = np.bmat([[ch_old],[ch]])
	np.save(EXPERIMENTFILENAME, ch)
