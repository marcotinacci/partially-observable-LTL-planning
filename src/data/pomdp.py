"""
@author: Marco Tinacci
"""

import itertools as it

class pomdp:

	S = []
	A = []
	T = {} # T : L.S * M.S * L.A -> distr(L.S * M.S)
	O = []
	Z = {} # Z : L.S -> distr(L.O)

	L = None
	M = None

	def __init__(self, S=[], A=[], T={}, O=[], Z={}):
		self.S = S
		self.A = A
		self.T = T
		self.O = O
		self.Z = Z
	
	def initProduct(self,L,M,O=[],Z={}):
		self.L = L
		self.M = M

		self.A=L.A
		self.O=O
		self.Z=Z
		
		# cartesian product of states
		self.S = list(it.product(L.names.keys(),M.S))

		# transition function
		self.T = {}
		for ls,(ms,a) in it.product(L.S,M.T.keys()):
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

	def importFile(self, filename):
		''' Read the POMDP structure from file '''
		with open(filename,'r') as f:
			lines = f.read().split('\n')
			i = 0
			for line in lines:
				words = line.split(':')
				print words
				if len(words) > 0:
					if words[0] == 'discount':
						# self.gamma = float(words[1])
						pass
					elif words[0] == 'states':
						self.S = words[1].split()
					elif words[0] == 'actions':
						self.A = words[1].split()
					elif words[0] == 'observations':
						self.Z = words[1].split()
					elif words[0] == 'T':
						if lines[i+1] == 'uniform':
							for s1 in self.S:
								for s2 in self.S:
									self.T[(s1,words[1],s2)] = 1./len(self.S)
						elif lines[i+1] == 'identity':
							for s1 in self.S:
								for s2 in self.S:
									if s1 == s2:
										self.T[(s1,words[1],s2)] = 1.0
									else:
										self.T[(s1,words[1],s2)] = 0.0
						else:
							offset = 1
							for s1 in self.S:
								nums = lines[i+offset].split()
								j = 0
								for s2 in self.S:
									self.T[(s1,words[1],s2)] = float(nums[j])
									j = j+1
								offset = offset + 1
					elif words[0] == 'O':
						if lines[i+1] == 'uniform':
							for s in self.S:
								for z in self.Z:
									self.O[(s,words[1],z)] = 1./len(self.S)
						else:
							offset = 1
							for s in self.S:
								nums = lines[i+offset].split()
								j = 0
								for z in self.Z:
									self.O[(s,words[1],z)] = float(nums[j])
									j = j+1
								offset = offset + 1
					elif words[0] == 'R':
						# TOFIX
						(obs,rew) = words[4].split()
						if (words[3] == '*' and obs == '*'):
							for s in self.S:
								for o in self.Z:
									self.R[(words[1],words[2],s,o)] = int(rew)
						elif words[3] == '*':
							for s in self.S:
								self.R[(words[1],words[2],s,obs)] = int(rew)
						elif obs == '*':
							for o in self.Z:
								self.R[(words[1],words[2],words[3],o)] = int(rew)
						else:
							self.R[(words[1],words[2],words[3], obs)] = int(rew)
					i = i+1

if __name__ == '__main__':
	P = pomdp(
		['s0','s1','s2'],
		['a','b'],
		{
			('s0','a'): {'s0': 0, 's1': 0.2, 's2': 0.8},
			('s0','b'): {'s0': 0, 's1': 0.4, 's2': 0.6}
		},
		['o1','o2'],
		{
			's0': {'o1': 0.5, 'o2': 0.5},
			's1': {'o1': 0.5, 'o2': 0.5},
			's2': {'o1': 0.3, 'o2': 0.7}
		}
	)
	