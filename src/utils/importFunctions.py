# -*- coding: utf-8 -*-
"""
Function for importing preprocessed data

@author: Marco Tinacci
"""

import re
import time
import numpy as np

def importProb(filename, numPar, verbose=False):
	"""
	Import data probabilities
		filename: file name
		numPar: number of state parameters
		verbose: allows print commands if true
	"""
	if verbose:
		print "-> IMPORT PROBABILITIES"
	start = time.time()
	data = {}
	pattern = r'\d+:\(\d+,\d+,\d+,\d+,\d+,\d+,\d+\)=\d+.\d+'
	with open(filename,'r') as f:
		for line in f:
			for item in re.findall(pattern,line):
				intNum = re.findall(r'\d+',item)
				key = tuple(map(int,intNum[1:numPar+1]))
				floatNum = re.findall(r'-?\d+\.\d+',item)
				data[key] = float(floatNum[0])
	end = time.time()
	if verbose:
		print "-> DONE (time: " + str(end - start) + ")"
	return data
