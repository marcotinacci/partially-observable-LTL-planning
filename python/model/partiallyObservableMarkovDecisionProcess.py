#!/usr/bin/env python
# -*- coding: utf-8 -*-

# >>> import modules

import caseStudies as cs

# >>> code

class PartiallyObservableMarkovDecisionProcess:

	def __init__(self, S, A, T, O, Z):
		# states
		self.states = dict(enumerate(S))
		self.inv_states = {v:k for k,v in self.states.iteritems()}
		# actions
		self.actions = dict(enumerate(A))
		self.inv_actions = {v:k for k,v in self.actions.iteritems()}
		# transitions
		self.transitionFunction = {
		    (self.inv_states[s1],self.inv_actions[a]) : 
		    {self.inv_states[s2]:pr for s2,pr in d.iteritems()} 
		        for (s1,a),d in T.iteritems()}
		# observations
		self.observations = dict(enumerate(O))
		self.inv_observations = {v:k for k,v in self.observations.iteritems()}
		# observation function
		self.observationFunction = {
			self.inv_states[s] : 
			{self.inv_observations[o]:pr for o,pr in d.iteritems()} 
				for s,d in Z.iteritems()}

	def __str__(self):
		ret = 'S: '+ str(self.states) + '\nA: '+ str(self.actions) + '\nT: '+ str(self.transitionFunction) + '\nO: '+ str(self.observations) + '\nZ: '+ str(self.observationFunction)
		return ret

# >>> main test

if __name__ == '__main__':
	pomdp = cs.treeStatesPomdp()
	print pomdp

# >>> authorship information

__author__ = "Marco Tinacci"
__copyright__ = "Copyright 2016"
__credits__ = ["Marco Tinacci"]
__license__ = "ASF"
__version__ = "2.0"
__maintainer__ = "Marco Tinacci"
__email__ = "marco.tinacci@gmail.com"
__status__ = "Production"
	