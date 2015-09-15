# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 11:56:55 2015

@author: Marco Tinacci
"""

class lts:
    
    S = []
    A = []
    T = {}  # T : (s,a) |-> s'
    
    def __init__(self, S, A, T):
        self.S = S
        self.A = A
        self.T = T


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