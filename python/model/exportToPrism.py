#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Export to PRISM format files """

# >>> import modules

# >>> code

def mdp2sta(mdp,filename):
	""" Export MDP to .sta prism file """
	FILE = open(filename,'w')
	head = '(index)'
	FILE.write(head+'\n')
	for i,s in enumerate(mdp.states):
		FILE.write( str(i) + ':(' + str(s) + ')\n' )
	FILE.close()

def mdp2lab(mdp,init,filename):
	""" Export labels to .lab prism file """
	with open(filename,'w') as FILE:
		FILE.write('0="init" 1="deadlock"\n'+str(init)+': 0')
	FILE.close()

def mdp2tra(mdp,filename,bunch=100000):
	""" 
	Export MDP transitions to .tra prism file. Since it could be a very
	expensive operation in terms of time it is possible to specify
	how much data to write on the file at the time.
	"""
	with open(filename,'w') as FILE:
		# number of states, number of choices, number of transitions
		temp = str(len(mdp.states)) + ' ' \
			+ str(len(mdp.transitions)) + ' ' \
			+ str(sum(map(len,mdp.transitions.values()))) + '\n'

		# lines counter
		lc = 0
		# choice counter
		cc = {}
		# source number, choice number, destination number, probability, action
		for (s1,a) in sorted(list(mdp.transitions),key=lambda e : e[0]):
			if s1 in cc:
				cc[s1] += 1
			else:
				cc[s1] = 0
			for s2,pr in mdp.transitions[(s1,a)].iteritems():
				temp += \
					str(s1)+' '+ \
					str(cc[s1])+' '+ \
					str(s2)+' '+ \
					str(pr)+' '+ \
					str(a)+'\n'
				lc += 1
			if lc >= bunch:
				# write a bunch at the time
				FILE.write(str(temp))
				temp = ""
		# write the remaining
		FILE.write(str(temp))
	FILE.close()

# >>> authorship information

__author__ = "Marco Tinacci"
__copyright__ = "Copyright 2016"
__credits__ = ["Marco Tinacci"]
__license__ = "ASF"
__version__ = "2.0"
__maintainer__ = "Marco Tinacci"
__email__ = "marco.tinacci@gmail.com"
__status__ = "Production"