#!/bin/bash

params="-v -t"

python predictionOverTimePrevYear.py coupleofpixels ../results/ $params > ../log/coupleofpixels_predTime.log.txt
echo "coupleofpixels"
python predictionOverTimePrevYear.py domadoo ../results/ $params > ../log/domadoo_predTime.log.txt
echo "domadoo"
python predictionOverTimePrevYear.py domotique34 ../results/ $params > ../log/domotique34_predTime.log.txt
echo "domotique34"
python predictionOverTimePrevYear.py johncouscous ../results/ $params > ../log/johncouscous_predTime.log.txt
echo "johncouscous"
python predictionOverTimePrevYear.py josdblog ../results/ $params > ../log/josdblog_predTime.log.txt
echo "josdblog"
python predictionOverTimePrevYear.py julsa ../results/ $params > ../log/julsa_predTime.log.txt
echo "julsa"
python predictionOverTimePrevYear.py jurilexblog ../results/ $params > ../log/jurilexblog_predTime.log.txt
echo "jurilexblog"
python predictionOverTimePrevYear.py maisonetdomotique ../results/ $params > ../log/maisonetdomotique_predTime.log.txt
echo "maisonetdomotique"
python predictionOverTimePrevYear.py paralipomenes ../results/ $params > ../log/paralipomenes_predTime.log.txt
echo "paralipomenes"
python predictionOverTimePrevYear.py philippebilger ../results/ $params > ../log/philippebilger_predTime.log.txt
echo "philippebilger"
python predictionOverTimePrevYear.py roxarmy ../results/ $params > ../log/roxarmy_predTime.log.txt
echo "roxarmy"
python predictionOverTimePrevYear.py shots ../results/ $params > ../log/shots_predTime.log.txt
echo "shots"
