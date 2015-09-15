# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 16:10:01 2015

@author: Marco Tinacci
"""

from data import mdp
from data import lts
from data import pomdp
import itertools as it

# === support functions ===
def prob(s1,a,s2,dim):
    p = prob0(s1[0],a,s2[0],dim)
    for i in xrange(1,len(s1)):
        p = p * probi(s1[i],s2[i],dim)
    return p

def prob0(s1,a,s2,dim):
    switcher = {
        'n': 1.0 if (min(s1[0]+1,dim-1),s1[1]) == s2 else 0.0,
        's': 1.0 if (max(s1[0]-1,0),s1[1]) == s2 else 0.0,
        'e': 1.0 if (s1[0],min(s1[1]+1,dim-1)) == s2 else 0.0,
        'w': 1.0 if (s1[0],max(s1[1]-1,0)) == s2 else 0.0
    }
    return switcher[a]

def probi(s1,s2,dim):
    ar = around(s1,dim)
    return 1.0/float(len(ar)) if s2 in ar else 0.0
    
def around(s,dim):
    return {(i,j) for i,j in it.product(range(dim),range(dim)) 
        if (s[0] == i and (s[1] == j-1 or s[1] == j+1))
            or (s[1] == j and (s[0] == i-1 or s[0] == i+1))
    }

# ==== PARAMS ====

dim = 3
N = 3

# ==== LTS controller ==== 
L = lts.lts(
        ['s0'],
        ['n','s','e','w'],
        {
            ('s0','n'): 's0', 
            ('s0','e'): 's0', 
            ('s0','s'): 's0', 
            ('s0','w'): 's0' 
        }
    )

# ==== MDP environment ==== 
S = list(it.product(
    it.product(range(dim),range(dim)),
    it.product(range(dim),range(dim)),
    it.product(range(dim),range(dim))))
A = L.A
K = it.product(S,A)
T = {}
for s1,a,s2 in it.product(S,A,S):
    p = prob(s1,a,s2,dim)
    if p != 0:
        if (s1,a) not in T.keys():
            T[(s1,a)] = {}
        T[(s1,a)][s2] = p

M = mdp.mdp(S,A,T)

# ==== POMDP partially observable ====
P = pomdp.pomdp()
P.initProduct(L,M)
O = ['o1', 'o2']
Z = {}
#for s in P.S:
    