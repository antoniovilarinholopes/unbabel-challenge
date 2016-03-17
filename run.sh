#!/bin/sh

if [ "$#" -ne 3 ]
  then
    echo "Usage: first-step training-set root-dir"
    exit 1 
fi

FIRST_STEP=$1
TRAINING_SET=$2
ROOT_DIR=$3


############################################
## Preprocessing dataset.
############################################

if [ "$FIRST_STEP" -eq 1 ]
  then
    ./preprocessing.perl $TRAINING_SET $ROOT_DIR
    python data-handler.py 
fi
############################################


############################################
## Training RNNLM. TODO Use condor?
############################################

if [ "$FIRST_STEP" -eq 2 ]
  then
    mkdir -p "models"
    datasets=("data/train_h.txt" "data/train_mt.txt" "data/train_h_pos.txt" "data/train_mt_pos.txt")
    h_mt=("h" "mt" "h_pos" "mt_pos")

    for idx in ${!datasets[*]}
      do
        #launch condor?
        python train-rnnlm-parallel.py ${datasets[$idx]} ${h_mt[$idx]}
    done
fi
############################################


############################################
## Extract features, generate CSV file
############################################

if [ "$FIRST_STEP" -eq 3 ]
  then
    datasets=("data/train_h.txt" "data/train_mt.txt" "data/train_h_pos.txt" "data/train_mt_pos.txt")
    h_mt=("h" "mt" "h_pos" "mt_pos")

    python extract-features.py ${datasets[0]} ${datasets[2]} ${h_mt[0]}
    #python extract-features.py ${datasets[1]} ${datasets[3]} ${h_mt[1]}

    #generate-csv.perl
fi
############################################


############################################
## Classify: SVM
############################################
if [ "$FIRST_STEP" -eq 4 ]
  then
    #classify.py
fi
############################################

