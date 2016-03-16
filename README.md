## unbabel-challenge
This challenge consists of given a sentence detect whether it is from a human or from MT. The approach we follow is similar to the one in [1].

## Our solution
As the suggested bibliography suggests, using POS LM and word LM achieve a very high accuracy. Our method is based on this assumption. Additionally, function words might be considered and we will use generic features: length of the sentence, number of prepositions, n of prepositions repeated. After, we might consider syntatic features.

The TAGS generated using stanford-postagger are the ones from AnCora[http://nlp.lsi.upc.edu/freeling/doc/tagsets/tagset-es.html]. Yes, it is wierd. stanford-postagger looks at the first 2-4 codes of Ancora convention, it is sufficient.

Maybe use: http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/?

#Method
+ First we preprocess the dataset: divide in machine-translated and human datasets, then we use stanford-postagger with the spanish distsim model to get the POS tags, and, finally, we generate a processed file with the tags from the previous step.
+ After the preprocessing, we train 4 language models using RNNLM toolkit [1], following then the LM features as described by the suggested bibliography. We decided to use RNNLM because due to the power of RNNs when modelling sequences arbitrarily long, we find it reasonable to use this LM instead of the others. Therefore, our features consist of 4 scores: f_wh, f_wmt, f_posh, fposmt; the length of the sentence.
+ Finally, we train our models using this information, testing the test set against these features. To evaluate we use the methods described in __Evaluation__.

#Experimental setup

Folders:
+ models: language models, h\_lm, mt\_lm, h\_pos\_lm, mt\_pos\_lm .
+ data: dataset divisions for h, mt, h\_pos, mt\_pos. TODO, describe division.
+ rnnlm-04b: rnnlm tool
+ processed-dataset. division between h and mt from original training set.

Scripts:
+ data-handler
+ train-rnnlm-parallel
+ classify
+ preprocessing


## Evaluation
10-fold cross evaluation. Measurement of accuracy, precision and recall. In addition, we will try to measure the BLEU score.


##Bibliography
* [1](http://www.aclweb.org/anthology/P13-1157) Arase, Yuki, and Ming Zhou. "Machine Translation Detection from Monolingual Web-Text."
* [2](http://www.fit.vutbr.cz/research/groups/speech/publi/2010/mikolov_interspeech2010_IS100722.pdf) Mikolov, Tomas, et al. "Recurrent neural network based language model." INTERSPEECH. Vol. 2. 20100.


##TODO
+ train-rnnlm:  finish script
+ extract-features: script
+ create-csv: script
+ classify: script

