#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

# >>> import modules

import partiallyObservableMarkovDecisionProcess as pomdp
from beliefMarkovDecisionProcess import *
import itertools as it
from distribution import *
import exportToDot as e2d

# >>> code

# moving position functions
goUp = lambda (x,y),env,rows : (x,y+1) if (x,y+1) not in env \
	and y < rows-1 else (x,y)
goDown = lambda (x,y),env : (x,y-1) if (x,y-1) not in env \
	and y > 0 else (x,y)
goLeft = lambda (x,y),env : (x-1,y) if (x-1,y) not in env \
	and x > 0 else (x,y)
goRight = lambda (x,y),env,cols : (x+1,y) if (x+1,y) not in env \
	and x < cols-1 else (x,y)

def robotArenaPomdp(rows, cols, robots):
	states = generateStates(rows,cols,robots)
	actions = {'up','left','right'}
	transitionFunction = generateTransitions(states,actions,rows,cols)
	# e.g., 'uu' = 2 steps up, 'ur' = 1 step up and 1 step right
	basicObservations = ['uu','u','ul','ur','l','r']
	observations = map(lambda o : frozenset(o) , \
		reduce(lambda l1,l2: list(l1) + list(l2), \
		map(lambda i : it.combinations(basicObservations,i), \
		range(robots+1))))
	observationFunction = generateObservationFunction(states,robots)
	return pomdp.PartiallyObservableMarkovDecisionProcess(states, 
		actions, transitionFunction, observations, observationFunction)

def generateObservationFunction(states,robots):
	obsFun = dict()
	for s in states:
		obsFun[s] = dict()
		# real observation
		realObs = reduce(lambda o1,o2: o1.union(o2),\
			map(lambda pos: observationDistance(s[0],pos) ,s[1]))
		if not realObs:
			obsFun[s][frozenset()] = 1.
		else:
			prob = reduce(lambda i,j: i*j, map( \
				lambda o: 0.5 if (len(o) == 2) else 1.0 ,realObs))
			dist2 = set(filter(lambda e : len(e) == 1, realObs))
			for obs in powerset(list(realObs)):
				if dist2.issubset(obs):
					obsFun[s][frozenset(obs)] = prob
	return obsFun

def powerset(seq):
	if len(seq) <= 1:
		yield seq
		yield []
	else:
		for item in powerset(seq[1:]):
			yield [seq[0]]+item
			yield item

def observationDistance(p1,p2):
	# switch on distances
	if p1[0] == p2[0] and p1[1]+2 == p2[1]:
		return frozenset({'uu',})
	elif p1[0] == p2[0] and p1[1]+1 == p2[1]:
		return frozenset({'u',})
	elif p1[0]-1 == p2[0] and p1[1] == p2[1]:
		return frozenset({'l',})
	elif p1[0]+1 == p2[0] and p1[1] == p2[1]:
		return frozenset({'r',})
	elif p1[0]+1 == p2[0] and p1[1]+1 == p2[1]:
		return frozenset({'ur',})
	elif p1[0]-1 == p2[0] and p1[1]+1 == p2[1]:
		return frozenset({'ul',})
	else:
		return frozenset()

def generateTransitions(states, actions, rows, cols):
	tran = dict()
	for s1 in states:
		for a in actions:
			tran[(s1,a)] = dict()
			main = updateMainRobotPosition(s1,a,rows,cols)
			nextStates = updateEnvironmentRobotsPositions(s1,main,rows,cols)
			for s2 in nextStates:
				tran[(s1,a)][(main,s2)] = 1./len(nextStates)
	return tran

def updateMainRobotPosition(state,action,rows,cols):
	# main robot position
	pos = state[0]
	# switch on actions
	if action == 'up':
		return goUp(pos,state[1],rows)
	elif action == 'left':	
		return goLeft(pos,state[1])
	elif action == 'right':
		return goRight(pos,state[1],cols)
	return pos

def updateEnvironmentRobotsPositions(state,main,rows,cols):
	# single robot actions
	baseActions = {'up','down','left','right'}
	# action configurations
	actions = it.product(baseActions,repeat=len(state[1]))
	positions = list(state[1])
	nextStates = set()
	for a in actions:
		newState = set()
		for i in range(len(positions)):
			if a[i] == 'up':
				newState.add(goUp(positions[i],set(),rows))
			elif a[i] == 'down':
				newState.add(goDown(positions[i],set()))
			elif a[i] == 'left':
				newState.add(goLeft(positions[i],set()))
			elif a[i] == 'right':
				newState.add(goRight(positions[i],set(),cols))
		# if every update position is different, even from the main position
		if len(newState) == len(positions) and main not in newState:
			nextStates.add(frozenset(newState))
	return nextStates

def generateStates(rows, cols, robots):
	""" 
	State space generator, every state is represented with the
	structure ((x,y),frozenset({(x1,y1),(x2,y2)})), the first pair
	of coordinates are the main robot's position, then random robots'
	positions follow in the frozenset.
		:param rows: number of rows, goal included
		:param cols: number of columns
		:param robots: number of random robots
		:return: the set of states
	"""
	# possible positions of a robot
	pos = {(c,r) for c in range(cols) for r in range(rows)}
	# add robots' positions
	states = set(map(lambda p : frozenset((p,)),pos))
	for rob in range(robots-1):
		temp = set()
		for s in states:
			for p in pos:
				if p not in s:
					temp.add(s.union(frozenset((p,))))
		states = temp
	# add main robot's position
	temp = set()
	for p in pos:
		for s in states:
			if p not in s:
				temp.add((p,s))
	states = temp
	return states

if __name__ == '__main__':
	P = robotArenaPomdp(6,5,2)
	# initial belief
	prior = Distribution(set(P.states.keys()), lambda el,dom: \
		Distribution.diracPfd(el,dom, \
		P.inv_states[((1,0),frozenset({(0,2),(2,2)}))]))
	# generate belief MDP
	print len(P.states), len(P.observations)
	print '>>> bmdp generation'
	bmdp = BeliefMarkovDecisionProcess(P,2,prior)
	# compute initial, accepting and refusing states
	accept = []	
	for k,v in bmdp.states.iteritems():
		if pomdp.inv_states[((1,0),frozenset({(0,2),(2,2)}))] in v.distr:
			if v.distr[pomdp.inv_states['win']] > 0.85:
				accept.append(k)
	# export to DOT
	print '>>> export to dot'
	e2d.export2dot(
		bmdp,'bmdp','test.dot', [], [], 
		[bmdp.inv_states[prior]],
		map(lambda s: bmdp.inv_states[s],bmdp.fringe))


# >>> authorship information

__author__ = "Marco Tinacci"
__copyright__ = "Copyright 2016"
__credits__ = ["Marco Tinacci"]
__license__ = "ASF"
__version__ = "2.0"
__maintainer__ = "Marco Tinacci"
__email__ = "marco.tinacci@gmail.com"
__status__ = "Production"