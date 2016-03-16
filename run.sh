#!/bin/sh

TRAINING_SET=$1
ROOT_DIR=$2


############################################
## Preprocessing dataset.
############################################

./preprocessing.perl $TRAINING_SET $ROOT_DIR
python data-handler.py 

############################################


############################################
## Training RNNLM. TODO Use condor?
############################################
mkdir "models"
datasets=("data/train_h.txt" "data/train_mt.txt" "data/train_h_pos.txt" "data/train_mt_pos.txt")
h_mt=("h" "mt" "h_pos" "mt_pos")

for idx in ${!datasets[*]}
do
#launch condor?
python train-rnnlm-parallel.py ${datasets[$idx]} ${h_mt[$idx]} "test"
done

############################################


############################################
## Extract features, generate CSV file
############################################

#extract-features.py
#generate-csv.perl

############################################


############################################
## Classify: SVM
############################################

#classify.py

############################################

