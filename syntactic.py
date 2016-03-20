# -*- coding: utf-8 -*-
import os
import random
import sys
import subprocess


assert len(sys.argv) == 5
file_path = sys.argv[1]
file_path_pos = sys.argv[2]
src = sys.argv[3]
train_test = sys.argv[4]

def read_datasets(file_path_local, file_path_local_pos):

    # SANITY CHECK
    assert os.path.isfile(file_path_local) and os.path.isfile(file_path_local_pos)

    dataset = []
    with open(file_path_local, 'r') as f_p:
        for line in f_p:
            dataset.append(line.strip())
    
    dataset_pos = []
    with open(file_path_local_pos, 'r') as f_p:
        for line in f_p:
            dataset_pos.append(line.strip())

    return dataset, dataset_pos


def datasets_to_file(sentence_length, num_prep, header, destination):

    with open(destination, 'w') as f:
        f.write(header + '\n')
        for idx in range(len(sentence_length)):
            f.write('{},{}\n'.format(sentence_length[idx], num_prep[idx]))


print("Reading datasets:" + file_path + "," + file_path_pos)
dataset, dataset_pos = read_datasets(file_path, file_path_pos)

print("Extracting syntactic features")

sentence_length = range(len(dataset))
number_of_prep = range(len(dataset_pos))


for idx in range(len(dataset)):
    sentence = dataset[idx]
    import re
    sentence_length[idx] = len([word for word in sentence.split(' ') if re.match("\w+",word, re.U)])
    number_of_prep[idx] = len(re.findall('sp[0C][0M][0S]',dataset_pos[idx]))

file_to_write = 'features_syntactic/{}_synt_feat_{}'.format(train_test, src)
header = 'length,num_prep'
datasets_to_file(sentence_length, number_of_prep, header, file_to_write)

