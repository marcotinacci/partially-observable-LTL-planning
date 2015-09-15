# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 11:57:20 2015

@author: Marco Tinacci
"""

import itertools as it

class mdp:
    
    S = []
    A = []
    T = {}  # T : (S,A) -> distr(S)
    
    def __init__(self, S=[], A=[], T={}):
        self.S = S
        self.A = A
        self.T = T
        
    def initImplicit(self, P):
        self.S = list(it.product(P.S, P.O))
        self.A = P.A
        for s1 in self.S:
            for a in self.A:
                distr = {}
                for s2 in self.S:
                    if (s1[0],a) in P.T:
                        distr[s2] = P.T[(s1[0],a)][s2[0]] * P.Z[s2[0]][s2[1]]
                if distr:
                    self.T[(s1,a)] = distr
    
    def __str__(self):
        ret = 'S\n'+str(self.S)+'\nA\n'+str(self.A)+'\nT\n'
        for k in self.T:
            ret = ret + str(k) + ':' + str(self.T[k]) + '\n'
        return ret

if __name__ == "__main__":
    M = mdp(
            ['m1','m2'],
            ['a','b','c'],
            { 
              ('m1','a'): {'m1': 1}, 
              ('m1','b'): {'m1': 0.5, 'm2': 0.5},
              ('m1','c'): {'m1': 0.8, 'm2': 0.2},
              ('m2','a'): {'m2': 1},
              ('m2','b'): {'m2': 1},
              ('m2','c'): {'m2': 1}
            }
        )