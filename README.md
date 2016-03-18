## unbabel-challenge
This challenge consists of given a sentence detect whether it is from a human or from MT. The approach we follow is similar to the one in [1].

## Our solution
Considering that the approach in [1] had sucess in the task we were presented, we decide that the best solution (in the time given) was to train different language models as suggested in the original article. Therefore, we use the scores of the language models as features (see __Method__ for more). To train the LMs we used the rnnlm toolkit by Mikolov [2] and our LMs are: human words lm, mt words lm, human pos lm, and mt pos lm. The POS tagger we used was the stanford POS tagger, where the tags are the ones from AnCora [http://nlp.lsi.upc.edu/freeling/doc/tagsets/tagset-es.html]. Note that in order to achieve the max precision of correct tags the stanford-postagger looks at the first 2-4 codes of Ancora convention. However, this method is sufficient for the task we consider.

#Method
+ First we preprocess the dataset: divide into machine-translated and human datasets; then we use stanford-postagger with the spanish distsim model to get the POS tags, and, finally, we generate a processed file with the tags from the previous step. In this step, we shuffle the indexes of the sentences in the datasets in order to avoid, further, the overfit problem.
+ After the preprocessing, we divide further the datasets into train(80%), test(20%) and valid(20% of train set)
+ we train 4 language models using RNNLM toolkit [2], the LM features are the ones described in the suggested bibliography. We decided to use RNNLM due to the power of RNNs when modelling sequences arbitrarily long, we find reasonable to use this LM instead of the others. Therefore, our features consist of 4 scores: f\_wh, f\_wmt, f\_posh, f\_posmt; the length of the sentence.
+ Finally, we train our models using these scores and test. Our models are built using multi-layer perceptrons in a deep architecture. In our models we also use standard normalization. In addition, the shuffling method previously mentioned andthe  dropout technique in the hidden layers to avoid overfitting. To evaluate the models, we use the methods described in __Evaluation__.

#Experimental setup

Folders:
+ models: language models, h\_lm, mt\_lm, h\_pos\_lm, mt\_pos\_lm .
+ data: dataset divisions for h, mt, h\_pos, mt\_pos. TODO, describe division.
+ features: features files.
+ rnnlm-04b: rnnlm tool
+ processed-dataset. division between h and mt from original training set. 

Scripts:
+ data-handler.py
+ train-rnnlm-parallel.py
+ classify.py
+ preprocessing.perl
+ generate-csv.perl
+ extract-features.py
+ extract-features-parallel.py


## Evaluation
We evaluate our models using the standard measurements accuracy, precision and recall.


##Bibliography
* [1](http://www.aclweb.org/anthology/P13-1157) Arase, Yuki, and Ming Zhou. "Machine Translation Detection from Monolingual Web-Text."
* [2](http://www.fit.vutbr.cz/research/groups/speech/publi/2010/mikolov_interspeech2010_IS100722.pdf) Mikolov, Tomas, et al. "Recurrent neural network based language model." INTERSPEECH. Vol. 2. 20100.


##TODO
+ Train our mlp/svm models
+ Test our models with test set

