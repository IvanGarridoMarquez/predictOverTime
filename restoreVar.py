# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 20:53:28 2018

@author: ivan
"""

import cPickle
import plotOverTime as plOT

fileIn="../testing/test_correct_nologs/results/coupleofpixels_F1M_predTime.pkl"

output = open(fileIn)
restoredVar=cPickle.load(output)
print type(restoredVar)
#nyrs=[2009,2010,2011,2012,2013,2014,2015]
nyrs=4

xlb,dat_crv,lb_crv=plOT.getScoresCurves(restoredVar,nyrs)
print dat_crv
print xlb
#xlbWA,dat_crvWA,lb_crvWA=plOT.getScoresCurves(f1_curveWA,nyrs)
legends=["Years","f1-measure","F1-measure of predictions over time"]
plOT.plotBehaviorN(xlb,dat_crv,lb_crv,legends)
#plOT.plotBehaviorN(xlb,dat_crv,lb_crv,legends,"../plots/"+blog+"_f1_svc_ovrtm.png")
#plOT.plotBehaviorN(xlbWA,dat_crvWA,lb_crv,legends,"../plots/"+blog+"_f1WA_svc_ovrtm.png")