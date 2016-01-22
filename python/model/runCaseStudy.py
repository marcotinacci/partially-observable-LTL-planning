#!/usr/bin/env python
# -*- coding: utf-8 -*-

# >>> import modules

from partiallyObservableMarkovDecisionProcess import *
from beliefMarkovDecisionProcess import *
from distribution import *
import exportToPrism as e2p
import exportToDot as e2d
import caseStudies as cs

# >>> code

if __name__ == '__main__':
	pomdp = cs.treeStatesPomdp()
	prior = Distribution(set(pomdp.states.values()), lambda el,dom: \
		Distribution.uniformPdf(el,dom))
	bmdp = BeliefMarkovDecisionProcess(pomdp,6,prior)
	e2d.export2dot(bmdp,'bmdp','test.dot')
	e2p.mdp2sta(bmdp,'test.sta')
	e2p.mdp2tra(bmdp,'test.tra')
	print str(bmdp)

# >>> authorship information

__author__ = "Marco Tinacci"
__copyright__ = "Copyright 2016"
__credits__ = ["Marco Tinacci"]
__license__ = "ASF"
__version__ = "2.0"
__maintainer__ = "Marco Tinacci"
__email__ = "marco.tinacci@gmail.com"
__status__ = "Production"