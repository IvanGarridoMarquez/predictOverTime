# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 10:48:13 2018

@author: ivan
"""
import matplotlib.pyplot as plt
import numpy as np

def getScoresCurve(scr):
    cleanScr=[]
    cleanYr=[]
    for sc in scr:
        cleanScr.append(sc[1])
        cleanYr.append(sc[0])
    return cleanScr,cleanYr

def getScoresCurves(listCur,asz):
    cleanScr=[]
    scr=np.array(listCur)
    curves=np.unique(scr[:,0])
    curves.sort()
    #n=len(curves)
    labels=np.unique(scr[:,1])
    labels.sort()
    for yr in curves:
        crv=scr[scr[:,0]==yr][:,2]
        vn=len(crv)
        dfn=asz-vn
        if dfn>0:
            d=np.empty((1,dfn))
            d[:]=None
            cleanScr.append(np.append(d,crv))
        else:
            cleanScr.append(crv)
    return labels.astype(int),cleanScr,curves.astype(int)

def plotBehaviorN(labelX,dataY,labelCurves,axes=["x label","y label","title"],save="show"):
    plt.clf()
    indStyle=0
    indColor=0
    indLabel=0
    style=['s','^','o','*','+']
    color=['b', 'r', 'g', 'c', 'm', 'y', 'k', 'w']
    for curve in dataY:
        plt.plot(labelX, curve,'k',label="")
        plt.plot(labelX, curve,color[indColor]+style[indStyle],label=labelCurves[indLabel])
        indStyle+=1
        indColor+=1
        indLabel+=1
        if indStyle>4:
            indStyle=0
        if indColor>7:
            indColor=0
    plt.xticks(labelX, labelX)    
    #plt.axis([min(labelX)-1, max(labelX)+1, 0, 1])
    plt.xlabel(axes[0])
    plt.ylabel(axes[1])
    plt.title(axes[2])
    plt.legend()
    if(save!="show"):
        plt.savefig(save)
    else:
        plt.show()
    
#a=[[0.6,0.8,1,0.32],[None,0.5,.21,None]]
#b=[2007,2008,2009,2010]
#c=[2007,2008]
#x=["x label","y label","title"]
##
#plotBehaviorN(b,a,c,x)