# -*- coding: utf-8 -*-
"""
Plot procedure
@author: Marco Tinacci
"""

import numpy as np
import matplotlib.pyplot as plt

FOLDER = 'results13102015'

# load data
s1 = np.load(FOLDER+'/_arena2_S3D3N3.npy')
s2 = np.load(FOLDER+'/_arena2_S3D4N3.npy')
s3 = np.load(FOLDER+'/_arena2_S3D5N3.npy')
#s4 = np.load(FOLDER+'/arena2_S3D5N3.npy')

# sum them up
s1 = np.sum(s1,axis=0)
s2 = np.sum(s2,axis=0)
s3 = np.sum(s3,axis=0)
#s4 = np.sum(s4,axis=0)

# cumulative sum
s1 = np.cumsum(s1)
s2 = np.cumsum(s2)
s3 = np.cumsum(s3)
#s4 = np.cumsum(s4)

# plot
#plt.plot(s1, 'r', s2, 'g', s3,'b',s4,'y')
plt.plot(s1, 'r', s2, 'g', s3, 'b')
plt.show()
