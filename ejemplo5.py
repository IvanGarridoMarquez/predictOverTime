# -*- coding: utf-8 -*-
"""
Created on Fri Jan 26 16:40:24 2018

@author: ivan
"""

import numpy as np
from scipy import sparse

tiMat=sparse.csr_matrix(np.array([[0.2,0.8,1,0,0,0,0,0.6,0.9],[0.7,0.45,1,0,0,0,0,0.6,0.6],[0.9,0.25,1,0,0,0.2,0,0.6,0.4]]))
w=[0.1,0.5,0.3]
#print type(tiMat)
print tiMat.toarray()
A=sparse.lil_matrix(tiMat)
#A.tolil()
print type(A)
#tiMat.transpose()
#print tiMat.indices
#print tiMat.indptr

print range(0,tiMat.get_shape()[0])
for i in range(0,A.get_shape()[0]):
        print i
        #print tiMat[i].toarray()
        A[i]*= w[i]
        #r=tiMat.getrow(i)*w[i]
        #print r.toarray()
        #print tiMat.multiply(w[i])
        #print tiMat.indptr[i]
        #tiMat.data[0 : tiMat.indptr[i + 1]] *= w[i]
        #tiMat.data[tiMat.indptr[i] : tiMat.indptr[i + 1]] *= w[i]
#tiMat.transpose()
print "------"
tiMat=sparse.csc_matrix(A)
print tiMat.toarray()