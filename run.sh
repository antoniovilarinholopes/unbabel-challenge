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

if [ "$FIRST_STEP" -le 1 ]
  then
    ./preprocessing.perl $TRAINING_SET $ROOT_DIR
    python data-handler.py 
fi
############################################


############################################
## Training RNNLM. TODO Use condor?
############################################

if [ "$FIRST_STEP" -le 2 ]
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

if [ "$FIRST_STEP" -le 3 ]
  then
    mkdir -p "features"
    datasets=("data/train_h.txt" "data/train_mt.txt" "data/train_h_pos.txt" "data/train_mt_pos.txt")
    h_mt=("h" "mt" "h_pos" "mt_pos")

#    python extract-features-parallel.py ${datasets[0]} ${h_mt[0]} ${h_mt[1]} "train" "w"
#    python extract-features-parallel.py ${datasets[1]} ${h_mt[1]} ${h_mt[0]} "train" "w"
#    python extract-features-parallel.py ${datasets[2]} ${h_mt[2]} ${h_mt[3]} "train" "pos"
#    python extract-features-parallel.py ${datasets[3]} ${h_mt[3]} ${h_mt[2]} "train" "pos"
    
    python extract-features-syntactic.py ${datasets[0]} ${datasets[2]} ${h_mt[0]} ${h_mt[1]} "train"
    python extract-features-syntactic.py ${datasets[1]} ${datasets[3]} ${h_mt[1]} ${h_mt[0]} "train"

    ./generate-csv.perl "features_syntactic/train_scores_feat_h" 1 "features_syntactic/train_scores_feat_mt" 0 "features_syntactic/" "train"
    #./generate-csv.perl "features/train_scores_feat_h" 1 "features/train_scores_feat_mt" 0 "features/" "train"
fi
############################################


############################################
## Build model: MLP
############################################
if [ "$FIRST_STEP" -le 4 ]
  then
    python3 build-model.py "features/features_train.csv"
fi
############################################

############################################
## Classify
############################################
#if [ "$FIRST_STEP" -le 5 ]
#  then
#    python3 classify.py "features/features_test.csv"
#fi
############################################

