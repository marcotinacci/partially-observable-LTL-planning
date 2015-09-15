# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 12:20:54 2015

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
        # cartesian product of states
        for s in it.product(L.S, M.S):
            self.S.append(s)
        self.A = L.A
        for s1,a,s2 in it.product(self.S,self.A,self.S):
            print s1,a,s2
            if L.T[(s1[0],a)] == s2[0]:
                if (s1,a) not in self.T.keys():
                    self.T[(s1,a)] = {}
                self.T[(s1,a)][s2] = M.T[(s1[1],a)][s2[1]]
        
        #for s1 in self.S:
        #    for a in self.A:
        #        distr = []
        #        for s2 in self.S:
        #            if L.T[(s1[0],a)] == s2[0]:
        #                distr.append(M.T[(s1[1],a)][s2[1]])
        #            else:
        #                distr.append(0)
        #        self.T[(s1,a)] = distr
        self.O = O
        self.Z = Z

    def __str__(self):
        ret = 'S\n'+str(self.S)+'\nA\n'+str(self.A)+'\nT\n'
        for k in self.T:
            ret = ret + str(k) + ':' + str(self.T[k]) + '\n'
        return ret

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
    