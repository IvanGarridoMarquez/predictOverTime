# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 14:45:54 2018

@author: ivan
"""

from sklearn import metrics
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.cross_validation import train_test_split
from sklearn.svm import SVC


x = [[1,2,3],[3,3,2],[8,8,7],[3,7,1],[4,5,6]]
y = [['bar','foo'],['bar'],['foo'],['foo','jump'],['bar','fox','jump']]

mlb = MultiLabelBinarizer()
y_enc = mlb.fit_transform(y)

train_x, test_x, train_y, test_y = train_test_split(x, y_enc, test_size=0.33)

clf = OneVsRestClassifier(SVC(probability=True))
clf.fit(train_x, train_y)
predictions = clf.predict(test_x)

print predictions

my_metrics = metrics.classification_report( test_y, predictions)
print my_metrics