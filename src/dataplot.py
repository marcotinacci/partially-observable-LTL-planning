# -*- coding: utf-8 -*-
"""
Plot procedure
@author: Marco Tinacci
"""

import numpy as np
import matplotlib.pyplot as plt
import sys

DIM = '5'
FOLDER = 'export_results'
MEASURE = '0'
PROP = 'avoid'
FIGNAME = DIM+'x'+DIM

LABEL1 = 'AVG'
LABEL2 = 'MAX'
LABEL3 = 'RND'
LABEL4 = 'RPL'

# load data
s1 = np.load(FOLDER+'/arena_'+PROP+'_C'+MEASURE+'S0D'+DIM+'N3.npy')
s2 = np.load(FOLDER+'/arena_'+PROP+'_C'+MEASURE+'S1D'+DIM+'N3.npy')
s3 = np.load(FOLDER+'/arena_'+PROP+'_C'+MEASURE+'S2D'+DIM+'N3.npy')
s4 = np.load(FOLDER+'/arena_'+PROP+'_C'+MEASURE+'S3D'+DIM+'N3.npy')

# sum them up
s1 = np.sum(s1,axis=0)
s2 = np.sum(s2,axis=0)
s3 = np.sum(s3,axis=0)
s4 = np.sum(s4,axis=0)

# cumulative sum
s1 = np.cumsum(s1)/100.
s2 = np.cumsum(s2)/100.
s3 = np.cumsum(s3)/100.
s4 = np.cumsum(s4)/100.

# plot
fig = plt.figure(figsize=(8, 3))
ax = fig.add_subplot(111)
ax.set_title('Arena '+DIM+'x'+DIM)
ax.set_xlabel('t')
ax.set_ylabel('Average number \n of collisions until t')

l1, = plt.plot(s1, 'r', label=LABEL1)
l2, = plt.plot(s2, 'g', label=LABEL2)
l3, = plt.plot(s3, 'b', label=LABEL3)
l4, = plt.plot(s4, 'y', label=LABEL4)
plt.legend(loc='upper left')
plt.plot()
plt.axis([0,100,0,16])
#plt.gcf().tight_layout()
plt.gcf().subplots_adjust(bottom=0.15)
plt.savefig('figures/'+PROP+'_C'+MEASURE+'D'+DIM+'N3.eps', format='eps')
