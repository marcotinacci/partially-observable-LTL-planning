# -*- coding: utf-8 -*-
"""
Scheduler functions

@author: Marco Tinacci
"""

import random
import func
import robots as rob

def randomScheduler(s, P):
	obs = P.Z[((P.L.inv_names[s[0]]),(P.M.inv_names[s[1]]))]
	freeDir = set(P.A) - obs.iteritems().next()[0]
	if freeDir:
		return random.choice(list(freeDir))
	else:
		return random.choice(P.A)

def repulsiveScheduler(s, P, dim):
	# compute set of observations
	obs = P.Z[((P.L.inv_names[s[0]]),(P.M.inv_names[s[1]]))].keys()[0]
	if not obs:
		# do not move if no robot is perceived
		return random.choice(['e', 'n', 's', 'w', 'h'])

	# if at least a robot is perceived, then consider walls as well
	walls = set()
	if s[0][0] == 0:
		walls = walls.union({'n'})
	if s[0][0] == dim-1:
		walls = walls.union({'s'})
	if s[0][1] == 0:
		walls = walls.union({'w'})
	if s[0][1] == dim-1:
		walls = walls.union({'e'})

	obs = obs.union(walls)

	switcher = {
		frozenset(): {'h'}, # never choose this
		frozenset({'h'}): {'e', 'n', 's', 'w'},
		frozenset({'n'}): {'s'},
		frozenset({'s'}): {'n'},
		frozenset({'e'}): {'w'},
		frozenset({'w'}): {'e'},
		frozenset({'h', 'n'}): {'s'},
		frozenset({'h', 's'}): {'n'},
		frozenset({'e', 'h'}): {'w'},
		frozenset({'h', 'w'}): {'e'},
		frozenset({'n', 's'}): {'e', 'w'},
		frozenset({'e', 'n'}): {'s', 'w'},
		frozenset({'n', 'w'}): {'e', 's'},
		frozenset({'e', 's'}): {'n', 'w'},
		frozenset({'s', 'w'}): {'e', 'n'},
		frozenset({'e', 'w'}): {'n', 's'}, 
		frozenset({'h', 'n', 's'}): {'e', 'w'},
		frozenset({'e', 'h', 'n'}): {'s', 'w'},
		frozenset({'h', 'n', 'w'}): {'e', 's'},
		frozenset({'e', 'h', 's'}): {'n', 'w'},
		frozenset({'h', 's', 'w'}): {'e', 'n'},
		frozenset({'e', 'h', 'w'}): {'n', 's'},
		frozenset({'e', 'n', 's'}): {'w'},
		frozenset({'n', 's', 'w'}): {'e'},
		frozenset({'e', 'n', 'w'}): {'s'},
		frozenset({'e', 's', 'w'}): {'n'},
		frozenset({'e', 'h', 'n', 's'}): {'w'},
		frozenset({'h', 'n', 's', 'w'}): {'e'},
		frozenset({'e', 'h', 'n', 'w'}): {'s'},
		frozenset({'e', 'h', 's', 'w'}): {'n'},
		frozenset({'e', 'n', 's', 'w'}): {'h'},
		frozenset({'e', 'h', 'n', 's', 'w'}): {'e', 'n', 's', 'w', 'h'}
	}
	return random.choice(list(switcher[obs]))

def beliefScheduler(b, P, pmin, valFunc, verbose=False):
	maximum = -1
	act_max = None
	for a in P.L.A:
		ba = b.returnUpdate(act=a)
		val = valFunc(ba,pmin,P)
		if round(val,10) == round(maximum,10):
			act_max.add(a)
			if verbose:
				print 'EQ act:',a,' - val:',val
		elif val > maximum:
			maximum = val
			act_max = {a}
			if verbose:
				print 'OK act:',a,' - val:',val
		else:
			if verbose:
				print 'NO act:',a,' - val:',val
	return random.choice(list(act_max))

def avgMinVal(b, pmin, P):
	"""
	MAX AVG MIN probability value:
		b: belief state
		pmin: minimum probability for every state
		P: pomdp
	"""
	ret = 0
	inv_obs = func.inverseObservation(b.M.O)
	#print inv_obs
	for st,pr in b.d.iteritems():
		ctrl = b.M.L.names[st[0]] # controller state
		env = b.M.M.names[st[1]] # environment state
		inner = 0
		for obs in P.O:
			obspr = P.Z[st][obs] if obs in P.Z[st] else 0
			if obspr == 0:
				continue
			env = tuple(item for t in env for item in t)
			key = tuple(item for t in (ctrl,env) for item in t)
			key = key + (inv_obs[obs],)
			if key in pmin:
				inner += obspr * pmin[key]
		ret += pr * inner
	return ret

def maxMinVal(b, pmin, P):
	"""
	MAX MAX MIN probability scheduler:
		b: belief state
		pmin: minimum probability for every state
		P: pomdp
	"""
	ret = 0
	inv_obs = func.inverseObservation(b.M.O)
	for st,pr in b.d.iteritems():
		ctrl = b.M.L.names[st[0]] # controller state
		env = b.M.M.names[st[1]] # environment state
		inner = 0
		for obs in P.O:
			obspr = P.Z[st][obs] if obs in P.Z[st] else 0
			if obspr == 0:
				continue
			env = tuple(item for t in env for item in t)
			key = tuple(item for t in (ctrl,env) for item in t)
			key = key + (inv_obs[obs],)
			if key in pmin:
				inner += obspr * pmin[key]
		if pr * inner > ret:
			ret = pr * inner
	return ret

def minMinVal(b, pmin, P):
	"""
	MAX MAX MIN probability scheduler:
		b: belief state
		pmin: minimum probability for every state
		P: pomdp
	"""
	ret = 0
	inv_obs = func.inverseObservation(b.M.O)
	for st,pr in b.d.iteritems():
		ctrl = b.M.L.names[st[0]] # controller state
		env = b.M.M.names[st[1]] # environment state
		inner = 0
		for obs in P.O:
			obspr = P.Z[st][obs] if obs in P.Z[st] else 0
			if obspr == 0:
				continue
			env = tuple(item for t in env for item in t)
			key = tuple(item for t in (ctrl,env) for item in t)
			key = key + (inv_obs[obs],)
			if key in pmin:
				inner += obspr * pmin[key]
		if pr * inner < ret:
			ret = pr * inner
	return ret


