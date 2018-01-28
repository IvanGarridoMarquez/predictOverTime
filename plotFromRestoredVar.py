# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 20:53:28 2018

@author: ivan
"""

import cPickle
import plotOverTime as plOT
import os
import argparse
import moduleFlog as flog

def resultType(tp):
    if tp=="ACC" or tp=="ACCw":
        return "Accuracy"
    if tp=="F1" or tp=="F1w":
        return "F1-measure"
    if tp=="PRE" or tp=="PREw":
        return "Precision"
    if tp=="REC" or tp=="RECw":
        return "Recall"

parser = argparse.ArgumentParser(description='process to evaluate the fall in performance in category prediction over time')
parser.add_argument('blog', metavar='blog', type=str, help='location of the blog')

args=parser.parse_args()
path="latestTAL/predOT-master/results/"+args.blog+"/"
#allfiles=os.listdir("latestTAL/predOT-master/results/shots/predictions")
#allfiles=next(os.walk(path))[2]

#fileIn="../testing/test_correct_nologs/results/coupleofpixels_F1M_predTime.pkl"
curBlog=flog.Blog(args.blog)
#first_year=earliest year of the data
first_year=curBlog.getBlogOriginDate().year
#last_year=latest year of the data
last_year=curBlog.getBlogLastDate().year
nyrs=last_year-first_year

for fl in next(os.walk(path))[2]:
    fileIn=fl
    
    output = open(fileIn)
    restoredVar=cPickle.load(output)
    
    fnamep=fileIn.split('_')
    #print type(restoredVar)
    #nyrs=[2009,2010,2011,2012,2013,2014,2015]
    #nyrs=4
    
    xlb,dat_crv,lb_crv=plOT.getScoresCurves(restoredVar,nyrs)
    #print dat_crv
    #print xlb
    #xlbWA,dat_crvWA,lb_crvWA=plOT.getScoresCurves(f1_curveWA,nyrs)
    operMes=resultType(fnamep[1])
    legends=["Years",operMes,operMes+" of predictions over time"]
    plOT.plotBehaviorN(xlb,dat_crv,lb_crv,legends,"../plots/"+args.blog+"_"+fnamep[1]+"_svc_ovrtm.png")
    #plOT.plotBehaviorN(xlb,dat_crv,lb_crv,legends,"../plots/"+blog+"_f1_svc_ovrtm.png")
    #plOT.plotBehaviorN(xlbWA,dat_crvWA,lb_crv,legends,"../plots/"+blog+"_f1WA_svc_ovrtm.png")