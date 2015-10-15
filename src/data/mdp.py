# -*- coding: utf-8 -*-
"""
@author: Marco Tinacci
"""

import itertools as it
import time

class mdp:
    
    names = {}
    inv_names = {}
    S = []
    A = []
    T = {}  # T : (S,A) -> distr(S)
    
    def __init__(self, S=[], A=[], T={}):
        self.names = dict(enumerate(S))
        self.inv_names = {v:k for k,v in self.names.iteritems()}
        self.S = self.names.keys()
        self.A = A
        self.T = {
            (self.inv_names[s1],a) : 
            {self.inv_names[s]:pr for s,pr in s2.iteritems()} 
                for (s1,a),s2 in T.iteritems()}
    
    def initImplicit(self, P):
        print "INIT IMPLICIT MDP"
        start = time.time()
        #self.S = list(it.product(P.S, P.O))
        self.S = [(s,o.keys()[0]) for s,o in P.Z.iteritems()]
        self.names = dict(enumerate(P.S))
        self.inv_names = {v:k for k,v in self.names.iteritems()}
        self.A = P.A

        # transition
        for (s1,a),d in P.T.iteritems():
            temp = {}
            # distribution
            for (s2,pr_st) in d.iteritems():
                # observation
                for (o,pr_obs) in P.Z[s2].iteritems():
                    #print pr_st
                    temp[(s2,o)] = pr_st * pr_obs
            # previous observation
            for o in P.Z[s1]:
                self.T[((s1,o),a)] = temp

        end = time.time()
        print "time: "+str(end-start)
    
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
    print M