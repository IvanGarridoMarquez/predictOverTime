# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 14:01:57 2018

@author: ivan
"""

from sklearn.datasets import make_multilabel_classification
from skmultilearn.problem_transform import BinaryRelevance
from sklearn.naive_bayes import GaussianNB

# this will generate a random multi-label dataset
X, y = make_multilabel_classification(sparse = True, n_labels = 20,
return_indicator = 'sparse', allow_unlabeled = False)

print type(X)
print X[0]
print type(y)

# initialize binary relevance multi-label classifier
# with a gaussian naive bayes base classifier
classifier = BinaryRelevance(GaussianNB())

# train
classifier.fit(X, y)

# predict
#predictions = classifier.predict(X_test)