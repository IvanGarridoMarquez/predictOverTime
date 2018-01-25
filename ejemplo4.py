# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 16:57:35 2018

@author: ivan
"""

def rowsTimsWeight(mat):
    for i in range(0,mat.get_shape()[0]):
        mat.data[mat.indptr[i] : mat.indptr[i + 1]] *= w[i]

import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse import diags

row = np.array([0, 0, 1, 2, 2, 2])
col = np.array([0, 2, 2, 0, 1, 3])
data = np.array([1, 2, 3, 4, 5, 6])
mat=csr_matrix((data, (row, col)), shape=(3, 4))
print mat.toarray()
w= np.array([1, 3, 2])
w1=diags(w,0)

print w1.toarray()
print mat.get_shape()

#s=w1.dot(mat.dot(w1))
#mat.data[mat.indptr[0] : mat.indptr[0 + 1]] *= 2
#mat.data[mat.indptr[1] : mat.indptr[1 + 1]] *= 3

#print s.toarray()

for i in range(0,mat.get_shape()[0]):
    mat.data[mat.indptr[i] : mat.indptr[i + 1]] *= w[i]

Z = mat.copy()
# simply repeat each value in Y by the number of nnz elements in each row: 
Z.data *= w.repeat(np.diff(Z.indptr))
#print Z.toarray()
#s=np.dot(np.dot(w, mat), w)
print mat.toarray()