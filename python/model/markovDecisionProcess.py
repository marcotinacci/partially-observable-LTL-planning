#!/usr/bin/env python
# -*- coding: utf-8 -*-

# >>> import modules

# >>> code

class MarkovDecisionProcess:
    """docstring for MarkovDecisionProcess"""
    
    def __init__(self, S, A, T):
        # states
        self.states = dict(enumerate(S))
        self.inv_states = {v:k for k,v in self.states.iteritems()}
        # actions
        self.actions = dict(enumerate(A))
        self.inv_actions = {v:k for k,v in self.actions.iteritems()}
        # transitions
        self.transitions = {
            (self.inv_states[s1],self.inv_actions[a]) : 
            {self.inv_states[s2]:pr for s2,pr in d.iteritems()} 
                for (s1,a),d in T.iteritems()}
        print 'tran:', self.transitions

    def __str__(self):
        ret = 'S: ' + str(self.states)\
            + '\nA: ' + str(self.actions)\
            + '\nT: ' + str(self.transitions)
        return ret

# >>> main test

if __name__ == "__main__":
    mdp = MarkovDecisionProcess(
            {'m1','m2'},
            {'a','b','c'},
            { 
              ('m1','a'): {'m1': 1}, 
              ('m1','b'): {'m1': 0.5, 'm2': 0.5},
              ('m1','c'): {'m1': 0.8, 'm2': 0.2},
              ('m2','a'): {'m2': 1},
              ('m2','b'): {'m2': 1},
              ('m2','c'): {'m2': 1}
            }
        )
    print str(mdp)


# >>> authorship information

__author__ = "Marco Tinacci"
__copyright__ = "Copyright 2016"
__credits__ = ["Marco Tinacci"]
__license__ = "ASF"
__version__ = "2.0"
__maintainer__ = "Marco Tinacci"
__email__ = "marco.tinacci@gmail.com"
__status__ = "Production"