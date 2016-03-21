#!/bin/sh

if [ "$#" -ne 1 ]
  then
    echo "Usage: first-step"
    exit 1
fi

FIRST_STEP=$1

############################################
## Extract features, generate CSV file
############################################

if [ "$FIRST_STEP" -le 1 ]
  then
    mkdir -p "features"
    datasets=("data/validation_h.txt" "data/validation_mt.txt" "data/validation_h_pos.txt" "data/validation_mt_pos.txt")
    h_mt=("h" "mt" "h_pos" "mt_pos")

#    python extract-features-parallel.py ${datasets[0]} ${h_mt[0]} ${h_mt[1]} "test" "w"
#    python extract-features-parallel.py ${datasets[1]} ${h_mt[1]} ${h_mt[0]} "test" "w"
#    python extract-features-parallel.py ${datasets[2]} ${h_mt[2]} ${h_mt[3]} "test" "pos"
#    python extract-features-parallel.py ${datasets[3]} ${h_mt[3]} ${h_mt[2]} "test" "pos"
    
#    python extract-features.py ${datasets[0]} ${datasets[2]} ${h_mt[0]} ${h_mt[1]} "test"
#    python extract-features.py ${datasets[1]} ${datasets[3]} ${h_mt[1]} ${h_mt[0]} "test"

#    ./generate-csv.perl "features/test_scores_feat_h" 1 "features/test_scores_feat_mt" 0 "features/" "test"

    python extract-features-syntactic.py ${datasets[0]} ${datasets[2]} ${h_mt[0]} ${h_mt[1]} "test"
    python extract-features-syntactic.py ${datasets[1]} ${datasets[3]} ${h_mt[1]} ${h_mt[0]} "test"

    ./generate-csv.perl "features_syntactic/test_scores_feat_h" 1 "features_syntactic/test_scores_feat_mt" 0 "features_syntactic/" "test"

fi
############################################


############################################
## Classify
############################################
if [ "$FIRST_STEP" -le 2 ]
  then
    python3 evaluate-model.py "features_syntactic/features_test.csv"
    #python3 evaluate-model.py "features/features_test.csv"
fi
############################################

