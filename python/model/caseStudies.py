#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

# >>> import modules

import partiallyObservableMarkovDecisionProcess as pomdp

# >>> code

def tigerPomdp():
	return pomdp.PartiallyObservableMarkovDecisionProcess(
		{'tl', 'tr', 'win', 'lose'},
		{'l', 'ol', 'or'},
		{
			('tl','l') : { 'tl' : 1 },
			('tl','ol') : { 'lose' : 1 },
			('tl','or') : { 'win' : 1 },
			('tr','l') : { 'tr' : 1 },
			('tr','ol') : { 'win' : 1 },
			('tr','or') : { 'lose' : 1 },
			('win','l') : { 'win' : 1 },
			('win','ol') : { 'win' : 1 },
			('win','or') : { 'win' : 1 },
			('lose','l') : { 'lose' : 1 },
			('lose','ol') : { 'lose' : 1 },
			('lose','or') : { 'lose' : 1 }
		},
		{'hl','hr'},
		{
			'tl' : {'hl' : 0.85, 'hr' : 0.15},
			'tr' : {'hl' : 0.15, 'hr' : 0.85},
			'win' : {'hl' : 0.5, 'hr' : 0.5},
			'lose' : {'hl' : 0.5, 'hr' : 0.5}
		}
	)

def treeStatesPomdp():
	return pomdp.PartiallyObservableMarkovDecisionProcess(
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

def twoStatesPomdp():
	return pomdp.PartiallyObservableMarkovDecisionProcess(
		{'s0','s1'},
		{'a'},
		{
			('s0','a'): {'s0': 0.5, 's1': 0.5},
			('s1','a'): {'s0': 0.5, 's1': 0.5},
		},
		{'o0','o1'},
		{
			's0': {'o0': 0.5, 'o1': 0.5},
			's1': {'o0': 0.5, 'o1': 0.5}
		}
	)

# >>> authorship information

__author__ = "Marco Tinacci"
__copyright__ = "Copyright 2016"
__credits__ = ["Marco Tinacci"]
__license__ = "ASF"
__version__ = "2.0"
__maintainer__ = "Marco Tinacci"
__email__ = "marco.tinacci@gmail.com"
__status__ = "Production"