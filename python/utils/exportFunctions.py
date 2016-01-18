# -*- coding: utf-8 -*-
"""
Function for exporting data structures to prism files

@author: Marco Tinacci
"""

import func
import time
import numpy as np

def export2lab(filename):
    with open(filename,'w') as f:
        start = time.time()
        f.write("0=\"init\" 1=\"deadlock\"\n0: 0")
        end = time.time()
        print "-> EXPORT TO LABELS (time: "+str(end - start) +")"

def export2tra(P,filename,bunch=100000):
    start = time.time()
    with open(filename,'w') as f:
        # number of states, number of choices, number of transitions
        temp = str(len(P.S))+' '+str(len(P.T))+' '+ \
            str(sum(map(len,P.T.values())))+'\n'

        # lines counter
        lc = 0
        # choice counter
        cc = {}
        # source number, choice number, destination number, probability, action
        for (s,a) in P.T:
            if s in cc:
                cc[s] += 1
            else:
                cc[s] = 0
            for k,p in P.T[(s,a)].iteritems():
                #print 's',s,'k',k
                temp += \
                    str(P.S.index(s))+' '+ \
                    str(cc[s])+' '+ \
                    str(P.S.index(k))+' '+ \
                    str(p)+' '+ \
                    str(a)+'\n'
                lc += 1
            if lc >= bunch:
                # write a bunch at the time
                f.write(str(temp))
                temp = ""
        # write the remaining
        f.write(str(temp))
        end = time.time()
        print "-> EXPORT TO TRANSITIONS (time: "+str(end - start) +")"

def export2sta(P,L,M,O,head,filename):
    start = time.time()
    f = open(filename,'w')
    
    # first line
    #head = "("
    #for i in range(N):
    #    head += "x"+str(i)+",y"+str(i)+","
    #head+="obs)\n"
    f.write(head+'\n')
    
    inv_obs = func.inverseObservation(O)

    for i,((c,e),o) in enumerate(P.S):
        #print 'i',i,'c',L.names[c],'e',M.names[e],'o',o
        line = str(i)+':('+ \
            str(c)+','+ \
            str(e) + ',' + \
            str(inv_obs[o]) + ')\n'
        f.write(line)

    end = time.time()
    print "-> EXPORT TO STATES (time: "+str(end - start)+")"

def export2prism(P):
    f = open('prism','w')
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
