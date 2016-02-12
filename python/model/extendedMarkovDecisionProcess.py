#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

# >>> import modules

import itertools as it
import csTests as cs
import exportToDot as e2d
from distribution import Distribution
from markovDecisionProcess import MarkovDecisionProcess
from partiallyObservableMarkovDecisionProcess import PartiallyObservableMarkovDecisionProcess

# >>> code

class ExplicitMarkovDecisionProcess(MarkovDecisionProcess):
	"""docstring for ExtendedMarkovDecisionProcess"""

	def __init__(self, pomdp, prior):
		self.pomdp = pomdp
		# initial belief
		self.prior = prior
		# extended states (state id, observation id)
		S = set(it.product(pomdp.states.values(),pomdp.observations.values()))
		# transition function
		T = dict()
		for (s1,o1),a in it.product(S,pomdp.actions.values()):
			for (s2,o2) in S:
				if pomdp.inv_states[s2] in pomdp.transitionFunction[(pomdp.inv_states[s1],pomdp.inv_actions[a])] and pomdp.inv_observations[o2] in pomdp.observationFunction[pomdp.inv_states[s2]]:
					if ((s1,o1),a) not in T:
						T[((s1,o1),a)] = dict()
					T[((s1,o1),a)][(s2,o2)] = pomdp.transitionFunction[(pomdp.inv_states[s1],pomdp.inv_actions[a])][pomdp.inv_states[s2]] * pomdp.observationFunction[pomdp.inv_states[s2]][pomdp.inv_observations[o2]]
		print 'S:',S,'\nA:',pomdp.actions.values(),'\nT:',T

		MarkovDecisionProcess.__init__(self,S,pomdp.actions.values(),T)

# >>> main test

if __name__ == '__main__':
	pomdp = cs.tigerPomdp()
	print pomdp
	prior = Distribution(set(pomdp.states.keys()),lambda el,dom: Distribution.restrictedUniformPdf(el,dom,{pomdp.inv_states['tl'],pomdp.inv_states['tr']}))
	# generate explicit MDP
	emdp = ExplicitMarkovDecisionProcess(pomdp,prior)
	print emdp
	# export to DOT
	e2d.export2dot(emdp,'emdp','emdp.dot', [], [], [],[])

# >>> authorship information

__author__ = "Marco Tinacci"
__copyright__ = "Copyright 2016"
__credits__ = ["Marco Tinacci"]
__license__ = "ASF"
__version__ = "2.0"
__maintainer__ = "Marco Tinacci"
__email__ = "marco.tinacci@gmail.com"
__status__ = "Production"