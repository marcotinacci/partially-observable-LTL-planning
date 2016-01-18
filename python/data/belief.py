"""
@author: Marco Tinacci
"""
import time

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

    def normalize(self):
            """ Normalize the belief distribution """
            total = sum(self.d.values())
            for k,v in self.d.iteritems():
                self.d[k] = v / total
                
    def clean(self):
        """ Removes zero values from the belief distribution """
        self.d = { k:v for k,v in self.d.iteritems() if v != 0 }

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
        # new belief distribution
        if act != None and obs != None: # ACTION AND OBSERVATION UPDATE
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
            self.clean()
            self.normalize()
            
        elif act != None: # ACTION UPDATE
            new = {}
            for ls,ms in self.d.keys():
                for k,v in self.M.T[((ls,ms),(act))].iteritems():
                    # create a new entry only if different from zero
                    if k not in new:
                        new[k] = self.d[(ls,ms)] * v
                    else:
                        new[k] += self.d[(ls,ms)] * v
            self.d = new
        elif obs != None: # OBSERVATION UPDATE
            new = {}
            for k,v in self.d.iteritems():
                if obs in self.Z[k]:
                    new[k] = v * self.Z[k][obs]
            self.d = new
            self.normalize()
        else: # bad call method
            raise ValueError("at least one action or one observation must be present")

        #end = time.time()
        #print "time: "+ str(end-start)
