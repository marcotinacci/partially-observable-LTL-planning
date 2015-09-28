# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 16:10:01 2015

@author: Marco Tinacci
"""

from data import mdp
from data import lts
from data import pomdp
from data import belief
import itertools as it
import time

# === support functions ===

def around(s,dim):
    return {(i,j) for i,j in it.product(range(dim),range(dim)) 
        if (s[0] == i and (s[1] == j-1 or s[1] == j+1))
            or (s[1] == j and (s[0] == i-1 or s[0] == i+1)
            or (s[0] == i and s[1] == j))
    }

def step(s,a,dim):
    switcher = {
        'h': (s[0],s[1]),
        'n': (max(s[0]-1,0),s[1]),
        's': (min(s[0]+1,dim-1),s[1]),
        'e': (s[0],min(s[1]+1,dim-1)),
        'w': (s[0],max(s[1]-1,0))
    }
    return switcher[a]

# === export functions ===

def export2tra(P):
    start = time.time()
    with open('robots.tra','w') as f:
        # number of states, number of choices, number of transitions
        temp = str(len(P.S))+' '+str(len(P.T))+' '+str(sum(map(len,P.T.values())))+'\n'
        # source number, choice number, destination number, probability, action
        for s in P.S:
            # choice counter
            cc = 0
            for a in P.A:
                for k,p in P.T[(s,a)].iteritems():
                    temp += str(P.S.index(s))+' '+str(cc)+' '+ \
                        str(P.S.index(k))+' '+str(p)+' '+str(a)+'\n'
                cc += 1
        f.write(str(temp))

        end = time.time()
        print "-> EXPORT TO TRANSITIONS (time: "+str(end - start) +")"

        
def export2sta(P):
    start = time.time()

    f = open('robots.sta','w')
    f = open('robots.sta','a')
    f.write("(sl,x0,y0,x1,y1,x2,y2,obs)\n")
    for i,s in enumerate(P.S):
        f.write(str(i)+':(0,'+str(s[0][1][0][0])+','+str(s[0][1][0][1])+','+
        str(s[0][1][1][0])+','+str(s[0][1][1][1])+','+str(s[0][1][2][0])+','+
        str(s[0][1][2][1])+','+str('0' if s[1] == 'none' else '1')+')\n')

    end = time.time()
    print "-> EXPORT TO STATES (time: "+str(end - start)+")"

def export2prism(P):
    f = open('prism','w')
    f = open('prism','a')
    for k,v in P.T.iteritems():
        f.write( \
            "\n["+str(k[2])+"]"+ \
            " rx="+str(k[1][0][0])+ \
            " & ry="+str(k[1][0][1])+ \
            " & x1="+str(k[1][1][0])+ \
            " & y1="+str(k[1][1][1])+ \
            " & x2="+str(k[1][2][0])+ \
            " & y2="+str(k[1][2][1])+ \
            " -> ")
        for i, (k1,v1) in enumerate(v.iteritems()):
            f.write( \
                str(v1) + " : " + \
                "(rx'="+str(k1[1][0][0])+") & " + \
                "(ry'="+str(k1[1][0][1])+") & " + \
                "(x1'="+str(k1[1][1][0])+") & " + \
                "(y1'="+str(k1[1][1][1])+") & " + \
                "(x2'="+str(k1[1][2][0])+") & " + \
                "(y2'="+str(k1[1][2][1])+") " \
            )
            if i == len(v)-1:
                f.write(";\n")
            else:
                f.write("+ ");

# ==== PARAMS ====

dim = 3
N = 3

# ==== LTS controller ==== 
L = lts.lts(
        ['s0'],
        ['h','n','s','e','w'],
        {
            ('s0','h'): 's0', 
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

print "-> TRANSITION FUNCTION GENERATION"
T = {}
for s1,a in it.product(S,A):
    ar1 = around(s1[1],dim)
    ar2 = around(s1[2],dim)
    S2 = it.product(ar1,ar2)
    p = 1.0 / float(len(ar1)) / float(len(ar2))
    T[(s1,a)] = {}
    for s2 in S2:
        s = (step(s1[0],a,dim),s2[0],s2[1])
        T[(s1,a)][s] = p

M = mdp.mdp(S,A,T)

# ==== POMDP partially observable ====
P = pomdp.pomdp()
print "-> INIT PRODUCT POMDP"
P.initProduct(L,M)
print "-> OBSERVATION FUNCTION"
P.O = ['some', 'none']
P.Z = {}
for s in P.S:
    P.Z[s] = {}
    P.Z[s]['some'] = 1 if s[1][0] in around(s[1][1],dim) \
        or s[1][0] in around(s[1][2],dim) \
        or s[1][0] == s[1][1] or s[1][0] == s[1][2] else 0
    P.Z[s]['none'] = 1 - P.Z[s]['some']

imp = mdp.mdp()
imp.initImplicit(P)

b = belief.belief(imp,P.Z)

