#!/bin/sh

FIRST_STEP=$1
TEST_SET=$2
############################################
## Extract features, generate CSV file
############################################




if [ "$FIRST_STEP" -le 0 ]
  then
    
    sed -e "s/^\_[ \t]*//g" < test_blind.txt > test_blind_only_sentences.txt 
    exit 0
fi

if [ "$FIRST_STEP" -le 1 ]
  then
     
    ./preprocessing-test-21-3-2016.perl $TEST_SET
   
    mkdir -p "features_blind_test"

    python extract-features-blind-test.py $TEST_SET "blind_test_dataset/test_dataset_pos.txt"

fi
############################################


############################################
## Classify
############################################
if [ "$FIRST_STEP" -le 2 ]
  then
    python3 classify-blind-test.py "features_blind_test/features_test.csv"
    ./prepare_final_classifications.perl predictions.txt test_blind_only_sentences.txt final_test_predictions.txt
    #python3 evaluate-model.py "features/features_test.csv"
fi
############################################

