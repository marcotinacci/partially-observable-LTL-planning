#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Export to DOT format file """

# >>> import modules

# >>> code

def export2dot(mdp,name,filename):
	FILE = open(filename,'w')
	FILE.write('digraph ' + name + ' {\n')

	# states style
	for i in mdp.states:
		FILE.write( '\t' + str(i) + ' [label="' + str(i) + '"];\n' )

	# print
	for (i1,a),d in mdp.transitions.iteritems():
		#FILE.write( str(i1) + ' -> ' + str(a) + ';\n')
		for i2,pr in d.iteritems():
			FILE.write( '\t' + str(i1) + ' -> ' + str(i2) +\
				' [label="' + str(mdp.actions[a]) + '"];\n')
	FILE.write('}')
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