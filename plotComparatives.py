# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 00:20:31 2018

@author: ivan
"""

import plotOverTime as plOT
import os
#import argparse
#import moduleFlog as flog

def getDataToPlot(csvfile):
    data=[]
    f=open(csvfile)
    g=0
    t=0
    for x in f.readlines():
        a=[]
        dat=x.replace("\"","").split(',')
        if t>0:
            for y in dat:
                if y=="":
                    #a.append(0)
                    g+=2
                else:
                    a.append(float(y))
            data.append(a)
        else:
            for y in dat:
                if y=="":
                    #a.append(0)
                    g+=2
                else:
                    a.append(int(y))
            data.append(a)
        t+=1
    return data


path="../comparative/"
#allfiles=os.listdir("latestTAL/predOT-master/results/shots/predictions")
allfiles=next(os.walk(path))[2]
lb_crv=["lastYr","eachYr","eachYrW"]
for blf in allfiles:
    prplt=getDataToPlot(path+blf)
    print prplt
    blname=blf.split('.')[0]
    legends=["Years","F1-measure","Comparative of approaches for re-training over time"]
    plOT.plotBehaviorN(prplt[0],prplt[1:],lb_crv,legends,path+"plots/"+blname+"_f1_3approach.png")