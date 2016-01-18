# -*- coding: utf-8 -*-
"""
Plot procedure
@author: Marco Tinacci
"""

import numpy as np
import matplotlib.pyplot as plt
import sys

FOLDER = 'export_results'
SCHEDULER = '0'

#LABEL1 = 'dim = 3, collisions'
#LABEL2 = 'dim = 4, collisions'
LABEL3 = 'collisions'
#LABEL4 = 'dim = 3, perceptions'
#LABEL5 = 'dim = 4, perceptions'
LABEL6 = 'perceptions'

# load data
#s1 = np.load(FOLDER+'/arena_track_C0S'+SCHEDULER+'D3N3.npy')
#s2 = np.load(FOLDER+'/arena_track_C0S'+SCHEDULER+'D4N3.npy')
s3 = np.load(FOLDER+'/arena_track_C0S'+SCHEDULER+'D5N3.npy')
#t1 = np.load(FOLDER+'/arena_track_C1S'+SCHEDULER+'D3N3.npy')
#t2 = np.load(FOLDER+'/arena_track_C1S'+SCHEDULER+'D4N3.npy')
t3 = np.load(FOLDER+'/arena_track_C1S'+SCHEDULER+'D5N3.npy')

# sum them up
#s1 = np.sum(s1,axis=0)
#s2 = np.sum(s2,axis=0)
s3 = np.sum(s3,axis=0)
#t1 = np.sum(t1,axis=0)
#t2 = np.sum(t2,axis=0)
t3 = np.sum(t3,axis=0)

# cumulative sum
#s1 = np.cumsum(s1)/100.
#s2 = np.cumsum(s2)/100.
s3 = np.cumsum(s3)/100.
#t1 = np.cumsum(t1)/100.
#t2 = np.cumsum(t2)/100.
t3 = np.cumsum(t3)/100.

# plot
fig = plt.figure(figsize=(4, 5))
ax = fig.add_subplot(111)
ax.set_title('Tracking')
ax.set_xlabel('t')
ax.set_ylabel('Average number of collisions and perceptions until t')

#l4, = plt.plot(t1, 'r', label=LABEL4)
#l5, = plt.plot(t2, 'g', label=LABEL5)
l6, = plt.plot(t3, 'b', label=LABEL6)
#l1, = plt.plot(s1, 'r--', label=LABEL1)
#l2, = plt.plot(s2, 'g--', label=LABEL2)
l3, = plt.plot(s3, 'b--', label=LABEL3)

plt.legend(loc='upper left',prop={'size':10})
plt.plot()
plt.axis([0,100,0,120])
#plt.gcf().tight_layout()
plt.gcf().subplots_adjust(left=0.15)
plt.savefig('figures/track_S'+SCHEDULER+'N3.eps', format='eps')
