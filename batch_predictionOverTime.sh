#!/bin/bash

params="$params"

#python predictionOverTime.py coupleofpixels ../results/ $params > ../log/coupleofpixels_predTime.log.txt
#echo "coupleofpixels"
#python predictionOverTime.py domadoo ../results/ $params > ../log/domadoo_predTime.log.txt
#echo "domadoo"
#python predictionOverTime.py domotique34 ../results/ $params > ../log/domotique34_predTime.log.txt
#echo "domotique34"
#python predictionOverTime.py johncouscous ../results/ $params > ../log/johncouscous_predTime.log.txt
#echo "johncouscous"
#python predictionOverTime.py josdblog ../results/ $params > ../log/josdblog_predTime.log.txt
#echo "josdblog"
python predictionOverTime.py julsa ../results/ $params > ../log/julsa_predTime.log.txt
echo "julsa"
python predictionOverTime.py jurilexblog ../results/ $params > ../log/jurilexblog_predTime.log.txt
echo "jurilexblog"
python predictionOverTime.py maisonetdomotique ../results/ $params > ../log/maisonetdomotique_predTime.log.txt
echo "maisonetdomotique"
python predictionOverTime.py paralipomenes ../results/ $params > ../log/paralipomenes_predTime.log.txt
echo "paralipomenes"
python predictionOverTime.py philippebilger ../results/ $params > ../log/philippebilger_predTime.log.txt
echo "philippebilger"
python predictionOverTime.py roxarmy ../results/ $params > ../log/roxarmy_predTime.log.txt
echo "roxarmy"
python predictionOverTime.py shots ../results/ $params > ../log/shots_predTime.log.txt
echo "shots"
