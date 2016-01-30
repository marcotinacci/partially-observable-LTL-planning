#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

# >>> import modules

import os

# >>> custom parameters

# absolute path of the prism model checker
PRISMPATH = '/Applications/prism-4.3-osx64/bin/prism'

# >>> code

def checkPCTLonMDP(model, formula):
	"""
	Model checking of a PCTL formula on a MDP using PRISM
		:param model: filename of the exported MDP model
		:param formula: the PCTL formula as a string
		:return: the probability of the model of satisfying the formula
	"""
	command = PRISMPATH + " -importmodel " + model + \
		".all -mdp -pf '" + formula + "' > results.txt"
	print "EXEC: "+command
	os.system(command)
	
#	data = {}
#	pattern = r'\d+:\(' + (r'\d+,' * (numPar-1)) + r'\d+\)=\d+.\d+'
#	with open(filename,'r') as f:
#		for line in f:
#			for item in re.findall(pattern,line):
#				intNum = re.findall(r'\d+',item)
#				key = tuple(map(int,intNum[1:numPar+1]))
#				floatNum = re.findall(r'-?\d+\.\d+',item)
#				data[key] = float(floatNum[0])

# >>> authorship information

__author__ = "Marco Tinacci"
__copyright__ = "Copyright 2016"
__credits__ = ["Marco Tinacci"]
__license__ = "ASF"
__version__ = "2.0"
__maintainer__ = "Marco Tinacci"
__email__ = "marco.tinacci@gmail.com"
__status__ = "Production"