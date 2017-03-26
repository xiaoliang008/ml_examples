#!/usr/bin/python

import numpy as np
from sklearn.cluster import KMeans
from sklearn.cluster import SpectralClustering
from sklearn.manifold import spectral_embedding
import sklearn.metrics
from drc import *
import pickle
import matplotlib
from numpy import genfromtxt
from sklearn.metrics.cluster import normalized_mutual_info_score
import os
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

 

X = genfromtxt('dataset/facial_85.csv', delimiter=',')
#noise = 10*np.random.rand(X.shape[0],12)
#noise1 = 10*np.random.randn(X.shape[0],9)
#X = np.hstack((X + noise1,noise))
#X = X + noise
label = genfromtxt('dataset/facial_true_labels_624x960.csv', delimiter=',')


clf = KMeans(n_clusters=20)
allocation = clf.fit_predict(X)
kmeans_nmi = normalized_mutual_info_score(allocation, label)
print "K means : " , kmeans_nmi


d_matrix = sklearn.metrics.pairwise.pairwise_distances(X, Y=None, metric='euclidean')
sigma = np.median(d_matrix)*3.3
Gamma = 1/(2*np.power(sigma,2))

clf = SpectralClustering(n_clusters=20, gamma=Gamma)
allocation = clf.fit_predict(X)
spectral_nmi = normalized_mutual_info_score(allocation, label)
print 'Spectral Clustering : ' , spectral_nmi


##import pdb; pdb.set_trace()
#
##p = [0.001, 0.002, 0.003, 0.004, 0.005, 0.006, 0.007,0.008,0.009,0.010,0.011,0.012,0.013, 0.1, 0.2]
result = drc(X, 20, Gamma)
allocation = result['allocation']
drc_nmi = normalized_mutual_info_score(allocation, label)
print 'DRC : ' , drc_nmi
print 'Dimension :\n' , result['L']


objects = ('K means', 'Spectral', 'DRC')
y_pos = np.arange(len(objects))
performance = [kmeans_nmi, spectral_nmi, drc_nmi]
 
plt.bar(y_pos, performance, align='center', alpha=0.5)
matplotlib.rc('xtick', labelsize=10) 
plt.xticks(y_pos, objects, rotation='vertical')
plt.ylabel('NMI')
plt.title('Breast Cancer Clustering Results against Truth NMI')
 
plt.show()





