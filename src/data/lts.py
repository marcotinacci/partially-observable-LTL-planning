"""
@author: Marco Tinacci
"""

class lts:
    
    names = {}
    inv_names = {}
    S = []
    A = []
    T = {}  # T : (s,a) |-> s'
    
    def __init__(self, S, A, T):
        self.names = dict(enumerate(S))
        self.inv_names = {v:k for k,v in self.names.iteritems()}
        self.S = self.names.keys()
        self.A = A
        self.T = {(self.inv_names[s1],a):self.inv_names[s2] for (s1,a),s2 in T.iteritems()}
            
    def __str__(self):
        ret = 'S\n'+str(self.S)+'\nA\n'+str(self.A)+'\nT\n'
        for k in self.T:
            ret = ret + str(k) + ':' + str(self.T[k]) + '\n'
        return ret

if __name__ == "__main__":
    L = lts(
            ['l1','l2'],
            ['a','b','c'],
            { 
                ('l1','a'): 'l2', 
                ('l1','c'): 'l1', 
                ('l2','b'): 'l1', 
                ('l2','c'): 'l2' 
            }
        )
