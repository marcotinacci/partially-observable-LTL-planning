# -*- coding: utf-8 -*-
"""
@author: Marco Tinacci
"""
import time

# TODO rendere le chiavi della distribuzione come riferimenti agli stati della struttura

class belief:
    # state distribution
    d = {}
    # implicit MDP reference
    M = None
    # observation function
    Z = None
    
    def __init__(self, M, Z, init={}):
        if not init:
            # uniform distribution
            self.d = { s : (1./len(M.S)) for s in M.S }
        else:
            self.d = init
        self.M = M
        self.Z = Z
    
    def normalize(self):
        """ Normalize the distribution """
        total = sum(self.d.values())
        for k,v in self.d.iteritems():
            self.d[k] = v / total
            
    def clean(self):
        """ Removes zero values from the distribution """
        self.d = { k:v for k,v in self.d.iteritems() if v != 0 }
    
    def update(self, act=None, obs=None):
        """ Belief update """
        #print "BELIEF UPDATE"
        #start = time.time()
        
        if act and obs: # ACTION AND OBSERVATION UPDATE
            new = {}
            for s in self.d.keys():
                for sp,prob in self.M.T[(s,act)].iteritems():
                    z = self.Z[sp[0]][obs]
                    # create a new entry only if different from zero
                    if sp not in new:
                        new[sp] = self.d[s] * prob * z
                    else:
                        new[sp] += self.d[s] * prob * z
            self.d = new
            self.normalize()
            
        elif act: # ACTION UPDATE
            # temporary updated ditribution
            new = {}
            for s in self.d.keys():
                for k,v in self.M.T[(s,act)].iteritems():
                    # create a new entry only if different from zero
                    if k not in new:
                        new[k] = self.d[s] * v
                    else:
                        new[k] += self.d[s] * v
                    
            # replace the old distribution
            self.d = new
            
        elif obs: # OBSERVATION UPDATE
            new = {}
            for k,v in self.d.iteritems():
                if obs in self.Z[k[0]] and obs == k[1]:
                    new[k] = v * self.Z[k[0]][obs]            
            self.d = new
            self.normalize()
        else: # bad call method
            raise ValueError("at least one action or one observation must be present")

        #end = time.time()
        #print "time: "+ str(end-start)
