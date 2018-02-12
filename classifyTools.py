# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 14:35:55 2018

@author: ivan
"""
from __future__ import division
from lxml import etree
import os
import argparse
import moduleFlog as flog
from scipy import sparse
from sklearn import svm
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC
#from collections import Counter
from sklearn.cross_validation import StratifiedKFold
#from skmultilearn.problem_transform import BinaryRelevance
from sklearn.naive_bayes import GaussianNB

def loadStopwords(listfile):
    lf=open(listfile)
    stopwordlst=[]
    for word in lf.readlines():
        word=word.replace('\n',"")
        stopwordlst.append(unicode(word,'utf8'))
        #print word
    return stopwordlst
    
def getWeighBagOfWordsYr(stpwrds,dataSet,w,yra):
    vectorizer = CountVectorizer(ngram_range=(1,2),lowercase=True,stop_words=stpwrds)
    countMatrix=vectorizer.fit_transform(dataSet.getInstancesTexts())
    #print len(yra)
    #print yra
    yranp=np.array(yra)
    yrasc=sparse.csr_matrix(yranp)
    print yrasc.shape
    #i=0
    #print type(countMatrix)
    transformer = TfidfTransformer()
    tfidf_train = transformer.fit_transform(countMatrix)
    tfidf_trainWA=tfidf_train.copy()
    #print type(tfidf_train)
    print tfidf_train.shape
    for i in range(0,tfidf_train.shape[0]):
        #tiMat.data[tiMat.indptr[i] : tiMat.indptr[i + 1]] *= wa[i]
        #print w[i]
        #print tfidf_trainWA.data[tfidf_trainWA.indptr[i]:tfidf_trainWA.indptr[i+1]]
        #print "$$$$"
        #print tfidf_trainWA.data[tfidf_trainWA.indptr[i]:tfidf_trainWA.indptr[i+1]]*w[i]
        tfidf_trainWA.data[tfidf_trainWA.indptr[i]:tfidf_trainWA.indptr[i+1]]*=w[i]
    tfidf_train=sparse.hstack(tfidf_train,yrasc)
    tfidf_trainWA=sparse.hstack([tfidf_trainWA,yrasc])
    return vectorizer,transformer,tfidf_train,countMatrix,tfidf_trainWA    

    
def getWeighBagOfWords(stpwrds,dataSet,w):
    vectorizer = CountVectorizer(ngram_range=(1,2),lowercase=True,stop_words=stpwrds)
    countMatrix=vectorizer.fit_transform(dataSet.getInstancesTexts())
    #i=0
    #print type(countMatrix)
    transformer = TfidfTransformer()
    tfidf_train = transformer.fit_transform(countMatrix)
    tfidf_trainWA=tfidf_train.copy()
    #print type(tfidf_train)
    #print tfidf_train.shape[0]
    for i in range(0,tfidf_train.shape[0]):
        #tiMat.data[tiMat.indptr[i] : tiMat.indptr[i + 1]] *= wa[i]
        #print w[i]
        #print tfidf_trainWA.data[tfidf_trainWA.indptr[i]:tfidf_trainWA.indptr[i+1]]
        #print "$$$$"
        #print tfidf_trainWA.data[tfidf_trainWA.indptr[i]:tfidf_trainWA.indptr[i+1]]*w[i]
        tfidf_trainWA.data[tfidf_trainWA.indptr[i]:tfidf_trainWA.indptr[i+1]]*=w[i]
    return vectorizer,transformer,tfidf_train,countMatrix,tfidf_trainWA

def getBagOfWords(stpwrds,dataSet):
    vectorizer = CountVectorizer(ngram_range=(1,2),lowercase=True,stop_words=stpwrds)
    countMatrix=vectorizer.fit_transform(dataSet.getInstancesTexts())
    transformer = TfidfTransformer()
    tfidf_train = transformer.fit_transform(countMatrix)
    return vectorizer,transformer,tfidf_train,countMatrix
    
def transformToFeat(vc,tr,data):
    countMatrix = vc.transform(data.getInstancesTexts())
    tfidf=tr.transform(countMatrix)
    return tfidf,countMatrix
    
def transformToFeatYr(vc,tr,data,yra):
    countMatrix = vc.transform(data.getInstancesTexts())
    tfidf=tr.transform(countMatrix)
    yranp=np.array(yra)
    yrasc=sparse.csr_matrix(yranp)
    tfidf=sparse.hstack([tfidf,yrasc])
    return tfidf,countMatrix
    
def labelsToMultilabelF(lbl):
    mlb = MultiLabelBinarizer(sparse_output=True)
    lbls_proc=mlb.fit_transform(lbl)
    return mlb,lbls_proc

def labelsToMultilabelT(lbl,mlb):
    lbls_proc=mlb.transform(lbl)
    return lbls_proc

def trainPredictor(X,Y):
    #print type(X)
    #print type(Y)
    #classif = BinaryRelevance(GaussianNB())

# train
    classif = OneVsRestClassifier(SVC(kernel='linear'))   
    classif.fit(X, Y)
    return classif
    
def trainPredictorWithWeights(X,Y,ws):
    #print type(X)
    #print type(Y)
    #classif = BinaryRelevance(GaussianNB())

# train
    #classif.fit(X,Y)
    #classif = OneVsRestClassifier(SVC(kernel='linear'))
    classif = OneVsRestClassifier(SVC(kernel='linear'))
    classif.set_params(sample_weight=ws)
#    print classif.get_params()
        
    classif.fit(X, Y)
    return classif
    
def evaluateMultilabelPrediction(pred_y,true_y):
    acc=metrics.accuracy_score(true_y,pred_y)
    rec=metrics.recall_score(true_y,pred_y,average='micro')
    f1=metrics.f1_score(true_y,pred_y,average='micro')
    prec=metrics.precision_score(true_y,pred_y,average='micro')
    return acc,prec,rec,f1
    
    
def confusionMatrix(pred_y,true_y,labels):
    cnf=metrics.confusion_matrix(true_y,pred_y,labels)
    return cnf
    