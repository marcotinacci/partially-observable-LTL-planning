"""
@author: Marco Tinacci
"""
import itertools as it

class ppomdp:

	S = []
	A = []
	T = {} # T : L.S * M.S * L.A -> distr(L.S * M.S)
	O = []
	Z = {} # Z : L.S -> distr(L.O)
	
	def __init__(self,L,M,O=[],Z={}):
		self.A=L.A
		self.O=O
		self.Z=Z
		
		# cartesian product of states
		LS = enumerate(L.S)
		MS = enumerate(M.S)
		self.S = list(it.product(LS.keys(),MS.keys()))

		self.T = {}
		for ls,(ms,a) in it.product(LS.keys(),MS.keys()):
			newk = ((ls,ms),(a))
			self.T[newk] = {}
			for ms1,pr in M.T[(ms,a)].iteritems():
				if (ls,a) in L.T:
					newk1 = ((L.T[(ls,a)]),ms1)
					self.T[newk][newk1] = pr


		# transition function
		self.T = {}
		for ls,(ms,a) in it.product(LS.keys(),MS.keys()):
			newk = ((ls,ms),(a))
			self.T[newk] = {}
			for ms1,pr in M.T[(ms,a)].iteritems():
				if (ls,a) in L.T:
					newk1 = ((L.T[(ls,a)]),ms1)
					self.T[newk][newk1] = pr

	def __str__(self):
		ret = 'S\n'+str(self.S)+'\nA\n'+str(self.A)+'\nT\n'
		for k in self.T:
			ret = ret + str(k) + ':' + str(self.T[k]) + '\n'
		ret = ret + 'O\n' + str(self.O) + '\nZ\n'
		for k in self.Z:
			ret = ret + str(k) + ':' + str(self.Z[k]) + '\n'
		return ret