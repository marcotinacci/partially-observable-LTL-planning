#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

# >>> import modules

from distribution import Distribution
from markovDecisionProcess import MarkovDecisionProcess
from partiallyObservableMarkovDecisionProcess import PartiallyObservableMarkovDecisionProcess
from Queue import Queue

# >>> code

class BeliefMarkovDecisionProcess(MarkovDecisionProcess):
	"""docstring for BeliefMarkovDecisionProcess"""

	def __init__(self, pomdp, horizon, prior):
		""" 
		Generation of the belief space MDP starting from a prior distribution
		and limited to a fixed horizon H, level 0 is the root, level H is
		included in the generation as a special level without outgoing 
		transitions.
			:param pomdp: partially observable model
			:param horizon: generation horizon
			:parm prior: initial belief distribution
		"""
		self.pomdp = pomdp
		# initial state
		self.root = prior
		# belief states
		B = set()
		# belief transition function
		T = dict()
		# belief-state space generation using a BFS
		Q = Queue()
		nxtQ = Queue()
		Q.put(prior)
		level = 0
		while not Q.empty() and level < horizon:
			current = Q.get()
			B.add(current)
			for act in pomdp.actions:
				for obs in pomdp.observations:
					nxt = self.__beliefUpdate(pomdp,current,act,obs)
					# find-the-copy function
					find = lambda lst, el : \
						reduce(lambda a,b: a if a != None else b, \
						map(lambda x : x if el.equals(x) else None, lst))
					# search for the same belief state
					same = find(list(B) + list(Q.queue) + list(nxtQ.queue),nxt)
					# do not add the state if already visited before
					if same == None:
						nxtQ.put(nxt)
					else:
						# keep the reference to compute 
						# the transition function probability
						nxt = same
					# add the probability mass to the transition function
					# compute Pr(o|b,a)
					pr = 0.0
					for i1,p1 in current.distr.iteritems():
						sub_pr = 0.0
						for i2,p2 in nxt.distr.iteritems():
							if i2 in pomdp.transitionFunction[(i1,act)]:
								sub_pr += pomdp.transitionFunction[(i1,act)][i2] \
									* pomdp.observationFunction[i2][obs]
						pr += p1 * sub_pr
					# do not add null mass probabilities
					if pr > 0.0:
						if (current, pomdp.actions[act]) not in T:
							# if (b,a) entry does not exist, create it
							T[(current,pomdp.actions[act])] = {}
						if nxt not in T[(current,pomdp.actions[act])]:
							# if (b,a)(b') entry does not exist
							# create it as the probability
							T[(current,pomdp.actions[act])][nxt] = pr
						else:
							# if (b,a)(b') entry already exists 
							# increment the probability
							T[(current,pomdp.actions[act])][nxt] += pr
			# if Q is empty replace it with nxtQ of the next level
			if Q.empty():
				Q = nxtQ
				nxtQ = Queue()
				level += 1

		# add last level from Q 
		for b in Q.queue:
			B.add(b)

		MarkovDecisionProcess.__init__(self,B,pomdp.actions.values(),T)

	@staticmethod
	def __beliefUpdate(pomdp, belief, action, observation):
		"""
		Compute the belief update, the time complexity of this function
		is quadratic on the size of the number of states of the pomdp
			:param pomdp: partiallyObservableMarkovDecisionProcess
			:param belief: initial belief distribution
			:param action: performed action ID
			:param observation: received observation ID
			:return: a distribution that represent the updated belief
		"""
		# build custom pdf
		pdf = dict()
		for s1 in belief.distr.keys():
			for s2,prob in pomdp.transitionFunction[ \
				(s1,action)].iteritems():
				if observation in pomdp.observationFunction[s2]:
					if s2 not in pdf:
						pdf[s2] = belief.distr[s1] * prob * \
						pomdp.observationFunction[s2][observation]
					else:
						pdf[s2] += belief.distr[s1] * prob * \
						pomdp.observationFunction[s2][observation]
		Distribution.normalize(pdf)
		return Distribution(belief.support,\
			lambda e,domain : Distribution.customPdf(e,pdf))

# >>> main test

if __name__ == "__main__":
	pomdp = PartiallyObservableMarkovDecisionProcess(
			{'s0','s1','s2'},
			{'a','b'},
			{
				('s0','a'): {'s0': 0.0, 's1': 0.2, 's2': 0.8},
				('s0','b'): {'s0': 0.0, 's1': 0.4, 's2': 0.6},
				('s1','a'): {'s1': 1.0},
				('s1','b'): {'s1': 1.0},
				('s2','a'): {'s2': 1.0},
				('s2','b'): {'s2': 1.0}
			},
			{'o1','o2'},
			{
				's0': {'o1': 0.5, 'o2': 0.5},
				's1': {'o1': 0.5, 'o2': 0.5},
				's2': {'o1': 0.3, 'o2': 0.7}
			}
        )
#    pomdp = PartiallyObservableMarkovDecisionProcess(
#			{'s0','s1'},
#			{'a'},
#			{
#				('s0','a'): {'s0': 0.5, 's1': 0.5},
#				('s1','a'): {'s0': 0.5, 's1': 0.5},
#			},
#			{'o0','o1'},
#			{
#				's0': {'o0': 0.5, 'o1': 0.5},
#				's1': {'o0': 0.5, 'o1': 0.5}
#			}
#        )
    prior = Distribution(pomdp.states,Distribution.uniformPdf)
    bmdp = BeliefMarkovDecisionProcess(pomdp,3,prior)
    print 'print bmdp:',bmdp
    import exportToPrism as exp
    exp.mdp2sta(bmdp,'test.sta')
    exp.mdp2tra(bmdp,'test.tra')

# >>> authorship information

__author__ = "Marco Tinacci"
__copyright__ = "Copyright 2016"
__credits__ = ["Marco Tinacci"]
__license__ = "ASF"
__version__ = "2.0"
__maintainer__ = "Marco Tinacci"
__email__ = "marco.tinacci@gmail.com"
__status__ = "Production"