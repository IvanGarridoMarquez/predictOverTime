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
#blog=flog.mapBlogs(args.blog)
blog=args.blog
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
nyrs=last_year-first_year
#last_year=2013
if v:
    print "blog's life from "+str(first_year)+" to "+str(last_year)
if v:
    print "///////////////////////////////////////////////////////////"
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
    featC,featTI,tiMat,cntMat=ct.getWeighBagOfWords(ct.loadStopwords("stopwords.french.list"),pre_train_set_parse,wa)
    if v:
         print "training matrix shape:"+str(tiMat.shape)
#process labels to multilabel format
    handLbl,labels_trn=ct.labelsToMultilabelF(pre_train_set_parse.getInstancesCategories())
    if v:
        print "objects with labels: "+str(labels_trn.shape)+" - number of categories: "+str(len(list(handLbl.classes_)))
#    predictor=ct.trainPredictor(tiMat,labels_trn)
#    for i in range(0,tiMat.get_shape()[0]):
#        #tiMat[i]*= wa[i]
#        tiMat.data[tiMat.indptr[i] : tiMat.indptr[i + 1]] *= wa[i]
    predictorWa=ct.trainPredictor(tiMat,labels_trn)
    if v:
        print "size of weights array:"+str(len(wa))
#get all posterior examples to curr_yr=test_set
    for year_tst in range(curr_year+1,last_year+1):      
 
        test_set=curBlog.getPostsBetweeDates(str(curr_year+1)+"-01-01",str(year_tst)+"-12-31")
        if v:
            print "test set range:["+str(curr_year+1)+"-"+str(year_tst)+"]-test_total:"+str(len(test_set))
        test_set_parse=flog.microCorpus(test_set)
    #vectorize the test_set in feature space
        tiMat_tst,cntMat_tst=ct.transformToFeat(featC,featTI,test_set_parse)
        true_labels_tst=ct.labelsToMultilabelT(test_set_parse.getInstancesTextsCategoriesFiltered(list(handLbl.classes_)),handLbl)
        if v:
            print "test matrix shape:"+str(tiMat_tst.shape)
            print "objects with labels: "+str(true_labels_tst.shape)
    #test predictor with test_set
#        lbls_predicted=predictor.predict(tiMat_tst)
        lbls_predictedWa=predictorWa.predict(tiMat_tst)
        if v:
#            print "labels predicted shape:"+str(lbls_predicted.shape)
            print "labels predicted shape:"+str(lbls_predictedWa.shape)
    #evaluate
#        acc_score,prec_score,rec_score,f1_score=ct.evaluateMultilabelPrediction(true_labels_tst,lbls_predicted)
        acc_scoreWa,prec_scoreWa,rec_scoreWa,f1_scoreWa=ct.evaluateMultilabelPrediction(true_labels_tst,lbls_predictedWa)
        if v:
#            print "scores[accuracy,precision,recall,f1-measure]:"
#            print "s--"+str(acc_score)+","+str(prec_score)+","+str(rec_score)+","+str(f1_score)
            print "scoresWa[accuracy,precision,recall,f1-measure]:"
            print "sw--"+str(acc_scoreWa)+","+str(prec_scoreWa)+","+str(rec_scoreWa)+","+str(f1_scoreWa)
    #register the results
#        acc_curve.append([curr_year,year_tst,acc_score])
#        prec_curve.append([curr_year,year_tst,prec_score])
#        rec_curve.append([curr_year,year_tst,rec_score])
#        f1_curve.append([curr_year,year_tst,f1_score])
        
        acc_curveWA.append([curr_year,year_tst,acc_scoreWa])
        prec_curveWA.append([curr_year,year_tst,prec_scoreWa])
        rec_curveWA.append([curr_year,year_tst,rec_scoreWa])
        f1_curveWA.append([curr_year,year_tst,f1_scoreWa])
        
        if v:
            print "-------------------------------------------------------"
            
    if tictac:
        print datetime.now() - startTime
    if v:
        print "==========================================================="
    #break

#save results into files
#output = open(args.output+"/"+blog+'_ACC_predTime.pkl', 'wb')
#cPickle.dump(acc_curve, output)
#output = open(args.output+"/"+blog+'_PRE_predTime.pkl', 'wb')
#cPickle.dump(prec_curve, output)
#output = open(args.output+"/"+blog+'_REC_predTime.pkl', 'wb')
#cPickle.dump(rec_curve, output)
#output = open(args.output+"/"+blog+'_F1M_predTime.pkl', 'wb')
#cPickle.dump(f1_curve, output)

output = open(args.output+"/"+blog+'_ACCw_predTime.pkl', 'wb')
cPickle.dump(acc_curveWA, output)
output = open(args.output+"/"+blog+'_PREw_predTime.pkl', 'wb')
cPickle.dump(prec_curveWA, output)
output = open(args.output+"/"+blog+'_RECw_predTime.pkl', 'wb')
cPickle.dump(rec_curveWA, output)
output = open(args.output+"/"+blog+'_F1Mw_predTime.pkl', 'wb')
cPickle.dump(f1_curveWA, output)

#Plot results
#print acc_curve
#xlb,dat_crv,lb_crv=plOT.getScoresCurves(acc_curve,nyrs)
#print xlb
#print dat_crv
xlbWA,dat_crvWA,lb_crvWA=plOT.getScoresCurves(acc_curveWA,nyrs)
legends=["Years","Accuracy","Accuracy of predictions over time"]
#plOT.plotBehaviorN(xlb,dat_crv,lb_crv,legends,"../plots/"+blog+"_acc_svc_ovrtm.png")
plOT.plotBehaviorN(xlbWA,dat_crvWA,lb_crvWA,legends,"../plots/"+blog+"_accWA_svc_ovrtm.png")

#xlb,dat_crv,lb_crv=plOT.getScoresCurves(prec_curve,nyrs)
xlbWA,dat_crvWA,lb_crvWA=plOT.getScoresCurves(prec_curveWA,nyrs)
legends=["Years","Precision","Precision of predictions over time"]
#plOT.plotBehaviorN(xlb,dat_crv,lb_crv,legends,"../plots/"+blog+"_prec_svc_ovrtm.png")
plOT.plotBehaviorN(xlbWA,dat_crvWA,lb_crvWA,legends,"../plots/"+blog+"_precWA_svc_ovrtm.png")

#xlb,dat_crv,lb_crv=plOT.getScoresCurves(rec_curve,nyrs)
xlbWA,dat_crvWA,lb_crvWA=plOT.getScoresCurves(rec_curveWA,nyrs)
legends=["Years","recall","Recall of predictions over time"]
#plOT.plotBehaviorN(xlb,dat_crv,lb_crv,legends,"../plots/"+blog+"_rec_svc_ovrtm.png")
plOT.plotBehaviorN(xlbWA,dat_crvWA,lb_crvWA,legends,"../plots/"+blog+"_recWA_svc_ovrtm.png")

#xlb,dat_crv,lb_crv=plOT.getScoresCurves(f1_curve,nyrs)
xlbWA,dat_crvWA,lb_crvWA=plOT.getScoresCurves(f1_curveWA,nyrs)
legends=["Years","f1-measure","F1-measure of predictions over time"]
#plOT.plotBehaviorN(xlb,dat_crv,lb_crv,legends,"../plots/"+blog+"_f1_svc_ovrtm.png")
plOT.plotBehaviorN(xlbWA,dat_crvWA,lb_crvWA,legends,"../plots/"+blog+"_f1WA_svc_ovrtm.png")

if tictac:
    print "Total time:"+str(datetime.now() - startTime)
#print pre_train_set_parse.getInstancesIds()