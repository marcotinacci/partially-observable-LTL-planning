#!/usr/bin/env python
# -*- coding: utf-8 -*-

# >>> import modules

from partiallyObservableMarkovDecisionProcess import *
from beliefMarkovDecisionProcess import *
from distribution import *
import exportToPrism as e2p
import exportToDot as e2d
import csTests as cs
import modelChecking as mc

# >>> code

if __name__ == '__main__':
	# partially observable model
	pomdp = cs.tigerPomdp()
	# initial belief
	prior = Distribution(set(pomdp.states.keys()), lambda el,dom: \
		Distribution.restrictedUniformPdf(el,dom,\
			#{pomdp.inv_states['tl'],pomdp.inv_states['tr']}))
			{pomdp.inv_states['tl'],pomdp.inv_states['tr']}))
	# generate belief MDP
	bmdp = BeliefMarkovDecisionProcess(pomdp,10,prior)

	# export to PRISM
	e2p.mdp2sta(bmdp,'test.sta')
	e2p.mdp2tra(bmdp,'test.tra')
	e2p.mdp2lab(bmdp,bmdp.inv_states[prior],'test.lab')

	# compute initial, accepting and refusing states
	accept = []
	refuse = []
	for k,v in bmdp.states.iteritems():
		if pomdp.inv_states['win'] in v.distr:
			if v.distr[pomdp.inv_states['win']] > 0.85:
				accept.append(k)
		if pomdp.inv_states['lose'] in v.distr:
			if v.distr[pomdp.inv_states['lose']] > 0.85:
				refuse.append(k)

	# export to DOT
	e2d.export2dot(
		bmdp,'bmdp','test.dot', refuse, accept, 
		[bmdp.inv_states[prior]],
		map(lambda s: bmdp.inv_states[s],bmdp.fringe))
	# model checking
	mc.checkPCTLonMDP('test','filter(print,Pmin=? [ true U<=3 (' + \
		reduce(lambda y,z: y+'|'+z , \
			map(lambda x : 'index='+str(x),accept)) \
		+ ') ], true)')

# >>> authorship information

__author__ = "Marco Tinacci"
__copyright__ = "Copyright 2016"
__credits__ = ["Marco Tinacci"]
__license__ = "ASF"
__version__ = "2.0"
__maintainer__ = "Marco Tinacci"
__email__ = "marco.tinacci@gmail.com"
__status__ = "Production"