## unbabel-challenge
This challenge consists of given a sentence detect whether the sentence is from a human or from a machine translation (mt). The approach we follow is similar to the one in [1], the bibliography suggested for this challenge.

## Our solution
Considering that the approach in [1] had sucess in the task we were presented, we decide that the best solution (in the time given) was to train different language models (lm) and use the scores as features, as suggested in the original article. Therefore, we use the scores of the language models as features (see __Method__ for more). To train the lm we used the rnnlm toolkit by Mikolov et al. [2] and our lm are: human words lm, mt words lm, human pos lm, and mt pos lm. The POS tagger we used was the stanford POS tagger, where the tags are the ones from AnCora [http://nlp.lsi.upc.edu/freeling/doc/tagsets/tagset-es.html]. Note that in order to achieve the max precision of correct tags the stanford-postagger looks at the first 2-4 codes of Ancora convention. However, this method is sufficient for the task we consider.

#Method
+ First we preprocess the dataset: divide into machine-translated and human datasets; then we use stanford-postagger with the spanish distsim model to get the POS tags, and, finally, we generate a processed file with the tags from the previous step. In this step, we shuffle the indexes of the sentences in the datasets in order to avoid, further, the overfit problem.
+ After the preprocessing, we divide further the datasets into train(80%), test(20%) and valid(20% of train set, only used for early stop in rnnlm).
+ Then, we train 4 language models using RNNLM toolkit [2], the lm features are the ones described in the suggested bibliography. We decided to use RNNLM due to the power of RNNs when modelling sequences arbitrarily long, we find reasonable to use this lm instead of the others. Therefore, our features consist of 4 scores: f\_wh, f\_wmt, f\_posh, f\_posmt; the length of the sentence, and number of prepositions.
+ Finally, we train our models using these features and test. Our models are built using multi-layer perceptrons in a deep architecture (keras and theano), svm (skicit) and decision trees (scikit). In our models we also use a standard normalization. In addition, the shuffling method previously mentioned and the dropout technique in the hidden layers are performed to avoid overfitting. To evaluate the models, we use the methods described in __Evaluation__.

#Experimental setup

Folders:
+ models: language models, h\_lm, mt\_lm, h\_pos\_lm, mt\_pos\_lm .
+ data: dataset divisions for h, mt, h\_pos, mt\_pos. Division: 80% train, 20% test (validation\_\*).
+ features: features files (train and test).
+ features\_syntactic: lm and syntactic features files (train and test).
+ feat\_synt\_83: lm and syntactic features files, bak of 83% scores.
+ features\_blind\_test: lm and syntactic features files for blind\_test.
+ blind\_test\_dataset:
+ rnnlm-04b: rnnlm tool
+ processed-dataset: division between h and mt from original training set. 

#Scripts:
+ data-handler.py: generate 80/20 datasets division, used.
+ train-rnnlm-parallel.py: train the rnnlm models, used.
+ classify.py: deprecated.
+ preprocessing.perl: divide train into h and mt set, extract pos taggs, used.
+ generate-csv.perl: generate a csv given 2 features files and 2 classes, used.
+ extract-features.py: extract scores from rnnlm, first experiment.
+ extract-features-parallel.py: deprecated.
+ extract-features-blind-test.py: extract scores and syntactic features for blind test (is equal to extract-features-syntactic-test.py), used.
+ extract-features-syntactic-test.py: extract scores and syntactic features for train and test set, used.
+ syntactic.py: extract syntactic features, deprecated.
+ fix-bug.py: a small script to fix a bug of extracting-features, solved, deprecated.
+ build-model.py: build our models (svm and deep mlp), used.
+ classify-blind-test.py: predictions for the blind test, used.
+ evaluate-model.py: predictions for our test set, used.
+ test-decision-trees.py: build our decision tree model and predict classes, used.
+ preprocessing-21-3-2016.perl: extract pos tags, used.
+ join-features.perl: small script for joining two files of features, deprecated.
+ prepare\_final\_classifications.perl: join sentences and predictions, used.
+ run.sh: run all steps for building models, used.
+ run-test.sh: run all steps for testing our models, used.
+ run-blind-test.sh: run all steps for blind test, used.


## Evaluation
We evaluate our models using the standard measurements accuracy, precision and recall.
+ With SVM we achieve 83% accuracy, precision and recall.
+ With Decision Trees we achieve 80% accuracy, precision and recall.
+ Unfortunately our deep MLP did not work as expected.

## Future work
+ Improve the feature set: use perplexity as a feature, from our observations the ppl scores maybe relevant; function word and gappy-phrase should also be considered. Another improvement is optimize the parameters of the rnnlm tool, currently we choose them ad hoc.
+ Use deep MLP, detect the problem in our solution which causes the model to do not work at all.

##Bibliography
* [1](http://www.aclweb.org/anthology/P13-1157) Arase, Yuki, and Ming Zhou. "Machine Translation Detection from Monolingual Web-Text."
* [2](http://www.fit.vutbr.cz/research/groups/speech/publi/2010/mikolov_interspeech2010_IS100722.pdf) Mikolov, Tomas, et al. "Recurrent neural network based language model." INTERSPEECH. Vol. 2. 20100.
+ [3](http://www.fit.vutbr.cz/research/groups/speech/publi/2011/mikolov_icassp2011_5528.pdf) Mikolov, Tomas et al. "Extensions of Recurrent Neural Network Language Model", In: Proceedings of the 2011 IEEE International Conference on Acoustics, Speech, and Signal Processing, ICASSP 2011, Prague, CZ
