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
    
    def initProduct(self,L,M,O=[],Z={}):

        self.A = L.A
        self.O = O
        self.Z = Z

        # cartesian product of states
        self.S = list(it.product(L.S,M.S))

        # transition function
        for k1 in it.product(L.S,M.T.keys()):
            newk = ((k1[0],k1[1][0]),k1[1][1])
            if k1[1] in M.T:
                self.T[newk] = {}
                for k2 in M.T[k1[1]].keys():
                    if (k1[0],k1[1][1]) in L.T:
                        self.T[newk][(L.T[(k1[0],k1[1][1])],k2)] = \
                        M.T[k1[1]][k2]

    def __init__(self, S=[], A=[], T={}, O=[], Z={}):
        self.S = S
        self.A = A
        self.T = T
        self.O = O
        self.Z = Z
        
    def __str__(self):
        ret = 'S\n'+str(self.S)+'\nA\n'+str(self.A)+'\nT\n'
        for k in self.T:
            ret = ret + str(k) + ':' + str(self.T[k]) + '\n'
        ret = ret + 'O\n' + str(self.O) + '\nZ\n'
        for k in self.Z:
            ret = ret + str(k) + ':' + str(self.Z[k]) + '\n'
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
    