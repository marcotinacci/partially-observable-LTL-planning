#!/usr/bin/env python
# -*- coding: utf-8 -*-

# >>> import modules

# >>> code

class Controller:
	"""docstring for Controller"""
	def __init__(self, bmdp, aggr, prob, init):
		""" Constructor
		:param bmdp: belief MDP model
		:param aggr: probability aggregation function, 
			takes the current belief and returns a distribution
			over actions
		:param prob: maps beliefs into probabilities of
			satisfying the desired formula
		:param init: initial belief
		"""
		self.current = init
		self.aggr = aggr
		self.bmdp = bmdp
		self.prob = prob

	def choose(self):
		# action distribution
		actDistr = dict()
		for act in self.bmdp.actions:

			for belief,pr in \
				self.bmdp.transitions[(self.current)].iteritems():


	@staticmethod
	def aggregateByWeightedSum():
		pass
	
	@staticmethod
	def weightedChoice(choices):
    """ 
    Weighed extraction
        choices: discrete distribution dictionary with elements as keys and 
            probabilities as values (it must be sum 1)
    """
    r = random.uniform(0, 1)
    upto = 0
    for st,pr in choices.iteritems():
        if upto + pr > r:
            return st
        upto += pr
    assert False, "Shouldn't get here"
		

# >>> authorship information

__author__ = "Marco Tinacci"
__copyright__ = "Copyright 2016"
__credits__ = ["Marco Tinacci"]
__license__ = "ASF"
__version__ = "2.0"
__maintainer__ = "Marco Tinacci"
__email__ = "marco.tinacci@gmail.com"
__status__ = "Production"