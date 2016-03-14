## unbabel-challenge
This challenge consists of given a sentence detect whether it is from a human or from MT. The approach we follow is similar to the one in http://www.aclweb.org/anthology/P13-1157.

## Our solution
As the suggested bibliography suggests, using POS LM and word LM achieve a very high accuracy. Our method is based on this assumption. Additionally, function words might be considered and we will use generic features: length of the sentence, number of prepositions, n of prepositions repeated, maybe verbs?. After we might consider syntatic features.

The TAGS generated using stanford-postagger are the ones from AnCora. Yes, it is wierd. stanford-postagger looks at the first 2-4 codes of Ancora convention, it is sufficient.

