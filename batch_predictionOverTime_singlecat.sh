#!/bin/bash

params="-v -t"

python predictionOverTime.py bcommebon ../results/ $params > ../log/bcommebon_predTime.log.txt
echo "bcommebon"
python predictionOverTime.py beaualalouche ../results/ $params > ../log/beaualalouche_predTime.log.txt
echo "beaualalouche"
python predictionOverTime.py cleacuisine ../results/ $params > ../log/cleacuisine_predTime.log.txt
echo "cleacuisine"
python predictionOverTime.py desrecettesagogo ../results/ $params > ../log/desrecettesagogo_predTime.log.txt
echo "desrecettesagogo"
python predictionOverTime.py francoischarlet ../results/ $params > ../log/francoischarlet_predTime.log.txt
echo "francoischarlet"
python predictionOverTime.py journaldugamer ../results/ $params > ../log/journaldugamer_predTime.log.txt
echo "journaldugamer"
python predictionOverTime.py lagourmandiseselonangie ../results/ $params > ../log/lagourmandiseselonangie_predTime.log.txt
echo "lagourmandiseselonangie"
python predictionOverTime.py lesactualitesdudroit ../results/ $params > ../log/lesactualitesdudroit_predTime.log.txt
echo "lesactualitesdudroit"
python predictionOverTime.py pechedegourmand ../results/ $params > ../log/pechedegourmand_predTime.log.txt
echo "pechedegourmand"
python predictionOverTime.py toutchilink ../results/ $params > ../log/toutchilink_predTime.log.txt
echo "toutchilink"
