# -*- coding: utf-8 -*-
"""
@author: Marco Tinacci
"""
import time

# TODO rendere le chiavi della distribuzione come riferimenti agli stati della struttura

# === STATIC METHODS ===
def normalize(dist):
        """ Normalize the dist distribution (static function) """
        total = sum(dist.values())
        for k,v in dist.iteritems():
            dist[k] = v / total
            
def clean(dist):
    """ Removes zero values from the dist distribution (static function) """
    dist = { k:v for k,v in dist.iteritems() if v != 0 }

# === CLASS BELIEF ===
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

    def returnUpdate(self, act=None, obs=None):
        """ 
        Return the updated belief without modifying the internal one, relies on
        the update method(act,obs)
        """
        old = self.d
        self.update(act,obs)
        new = self.d
        self.d = old
        return belief(self.M,self.Z,init=new)
    
    def update(self, act=None, obs=None):
        """ 
        Compute the updated belief on actions and observations received 
        and save it internally
        """
        #print "BELIEF UPDATE"
        #start = time.time()
        # new belief distribution
        if act and obs: # ACTION AND OBSERVATION UPDATE
            new = {}
            for s in self.d.keys():
                for sp,prob in self.M.T[(s,act)].iteritems():
                    z = self.Z[sp][obs] if obs in self.Z[sp] else 0
                    # create a new entry only if different from zero
                    if sp not in new:
                        new[sp] = self.d[s] * prob * z
                    else:
                        new[sp] += self.d[s] * prob * z
            self.d = new
            normalize(self.d)
            
        elif act: # ACTION UPDATE
            # temporary updated ditribution
            new = {}
            for ls,ms in self.d.keys():
                for k,v in self.M.T[((ls,ms),(act))].iteritems():
                    # create a new entry only if different from zero
                    if k not in new:
                        new[k] = self.d[(ls,ms)] * v
                    else:
                        new[k] += self.d[(ls,ms)] * v
                    
            # replace the old distribution
            self.d = new
        elif obs: # OBSERVATION UPDATE
            new = {}
            for k,v in self.d.iteritems():
                if obs in self.Z[k[0]] and obs == k[1]:
                    new[k] = v * self.Z[k[0]][obs]            
            self.d = new
            normalize(self.d)
        else: # bad call method
            raise ValueError("at least one action or one observation must be present")

        #end = time.time()
        #print "time: "+ str(end-start)
