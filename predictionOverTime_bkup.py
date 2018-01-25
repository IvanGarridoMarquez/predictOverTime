#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 16:04:19 2018

@author: Ivan Garrido Marquez
"""
from __future__ import division
import moduleFlog as flog
import classifyTools as ct
import argparse
import numpy as np
from datetime import datetime
import cPickle
import plotOverTime as plOT

parser = argparse.ArgumentParser(description='process to evaluate the fall in performance in category prediction over time')
parser.add_argument('blog', metavar='blog', type=str, help='location of the blog')
parser.add_argument('output', metavar='output', type=str, help='address to save output files')
parser.add_argument("-v", "--verbose", help="shows the process status", action="store_true")
parser.add_argument("-t", "--time", help="shows the time took", action="store_true")

args=parser.parse_args()

if args.output[-1]!='/':
    args.output+='/'

#blog
blog=flog.mapBlogs(args.blog)
v=args.verbose
tictac=args.time

if tictac:
    startTime = datetime.now()
#variables where the final results will be stored
acc_curve=[]
prec_curve=[]
rec_curve=[]
f1_curve=[]
acc_curveWA=[]
prec_curveWA=[]
rec_curveWA=[]
f1_curveWA=[]

#create object blog Handler
curBlog=flog.Blog(blog)
#first_year=earliest year of the data
first_year=curBlog.getBlogOriginDate().year
#last_year=latest year of the data
last_year=curBlog.getBlogLastDate().year
if v:
    print "blog's life from "+str(first_year)+" to "+str(last_year)
#for each year 
#fix the hypothetical current year=curr_yr
for curr_year in range(first_year,last_year):
#get all examples up to curr_yr(included)=pre_train_set
    pre_train_set=curBlog.getPostsBetweeDates(str(first_year)+"-01-01",str(curr_year)+"-12-31")
    pre_train_set_parse=flog.microCorpus(pre_train_set)
#    print pre_train_set_parse.mcCorpus[len()].locfile
    #print pre_train_set_parse.getInstancesIds()
    wa=np.ndarray(shape=(len(pre_train_set)), dtype=float)
    if v:
        print "current_year:"+str(curr_year)+"-train_total:"+str(len(pre_train_set))
#get feature space from pre_train_set
#vectorize the pre_train_set in feature space
    featC,featTI,tiMat,cntMat=ct.getBagOfWords(ct.loadStopwords("stopwords.french.list"),pre_train_set_parse)
    if v:
         print "training matrix shape:"+str(tiMat.shape)
#process labels to multilabel format
    handLbl,labels_trn=ct.labelsToMultilabelF(pre_train_set_parse.getInstancesCategories())
    if v:
        print "objects with labels: "+str(labels_trn.shape)+" - number of categories: "+str(len(list(handLbl.classes_)))
#weight=1
    weight=1
    posW=0
#for each year since curr_year until the first_year
    for year in list(reversed(range(first_year,curr_year+1))):
#	train_set+=weight samples in pre_train_set which belong to year (sample * weight)
        train_setDocs=curBlog.getPostsFromAYear(year)
        if v:
            print "year:"+str(year)+"-train:"+str(len(train_setDocs))+" w:"+str(weight)
#	weight*=2/3
        wa[posW:posW+len(train_setDocs)]=weight
        posW=posW+len(train_setDocs)
        weight*=2/3
#train multi-label classifier=predictor
    predictor=ct.trainPredictor(tiMat,labels_trn)
    for i in range(0,tiMat.get_shape()[0]):
        tiMat.data[tiMat.indptr[i] : tiMat.indptr[i + 1]] *= wa[i]
    predictorWa=ct.trainPredictor(tiMat,labels_trn)
    if v:
        print "size of weights array:"+str(len(wa))
#get all posterior examples to curr_yr=test_set
    test_set=curBlog.getPostsBetweeDates(str(curr_year+1)+"-01-01",str(last_year)+"-12-31")
    if v:
        print "test set range:["+str(curr_year+1)+"-"+str(last_year)+"]-test_total:"+str(len(test_set))
    test_set_parse=flog.microCorpus(test_set)
#vectorize the test_set in feature space
    tiMat_tst,cntMat_tst=ct.transformToFeat(featC,featTI,test_set_parse)
    true_labels_tst=ct.labelsToMultilabelT(test_set_parse.getInstancesTextsCategoriesFiltered(list(handLbl.classes_)),handLbl)
    if v:
        print "test matrix shape:"+str(tiMat_tst.shape)
        print "objects with labels: "+str(true_labels_tst.shape)
#test predictor with test_set
    lbls_predicted=predictor.predict(tiMat_tst)
    lbls_predictedWa=predictorWa.predict(tiMat_tst)
    if v:
        print "labels predicted shape:"+str(lbls_predicted.shape)
        print "labels predicted shape:"+str(lbls_predictedWa.shape)
#evaluate
    acc_score,prec_score,rec_score,f1_score=ct.evaluateMultilabelPrediction(true_labels_tst,lbls_predicted)
    acc_scoreWa,prec_scoreWa,rec_scoreWa,f1_scoreWa=ct.evaluateMultilabelPrediction(true_labels_tst,lbls_predictedWa)
    if v:
        print "scores[accuracy,precision,recall,f1-measure]:"
        print str(acc_score)+","+str(prec_score)+","+str(rec_score)+","+str(f1_score)
        print "scoresWa[accuracy,precision,recall,f1-measure]:"
        print str(acc_scoreWa)+","+str(prec_scoreWa)+","+str(rec_scoreWa)+","+str(f1_scoreWa)
#register the results
    acc_curve.append([curr_year,acc_score])
    prec_curve.append([curr_year,prec_score])
    rec_curve.append([curr_year,rec_score])
    f1_curve.append([curr_year,f1_score])
    
    acc_curveWA.append([curr_year,acc_scoreWa])
    prec_curveWA.append([curr_year,prec_scoreWa])
    rec_curveWA.append([curr_year,rec_scoreWa])
    f1_curveWA.append([curr_year,f1_scoreWa])
    
    if tictac:
        print datetime.now() - startTime
    if v:
        print "-------------------------------------------------------"
#    break

#Plot results
#a=[[0.6,0.8,1,0.32],[0.47,0.5,.21,0.9]]
Sco_crv,Yr_crv=plOT.getScoresCurve(acc_curve)
Sco_crvWA,Yr_crvWA=plOT.getScoresCurve(acc_curveWA)
curvesToplot=[Sco_crv,Sco_crvWA]
#b=[2007,2008,2009,2010]
#c=[2007,2008]
#x=["x label","y label","title"]
#plotBehaviorN(b,a,c,x,"sample.png")
plOT.plotBehaviorN(b,curvesToplot,c,x,"sample.png")

#save results into files
output = open(args.output+"/"+blog+'_ACC_predTime.pkl', 'wb')
cPickle.dump(acc_curve, output)
output = open(args.output+"/"+blog+'_PRE_predTime.pkl', 'wb')
cPickle.dump(prec_curve, output)
output = open(args.output+"/"+blog+'_REC_predTime.pkl', 'wb')
cPickle.dump(rec_curve, output)
output = open(args.output+"/"+blog+'_F1M_predTime.pkl', 'wb')
cPickle.dump(f1_curve, output)

output = open(args.output+"/"+blog+'_ACCw_predTime.pkl', 'wb')
cPickle.dump(acc_curveWA, output)
output = open(args.output+"/"+blog+'_PREw_predTime.pkl', 'wb')
cPickle.dump(prec_curveWA, output)
output = open(args.output+"/"+blog+'_RECw_predTime.pkl', 'wb')
cPickle.dump(rec_curveWA, output)
output = open(args.output+"/"+blog+'_F1Mw_predTime.pkl', 'wb')
cPickle.dump(f1_curveWA, output)

if tictac:
    print "Total time:"+str(datetime.now() - startTime)
#print pre_train_set_parse.getInstancesIds()