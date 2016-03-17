# -*- coding: utf-8 -*-
import os
import random
import sys
import subprocess


assert len(sys.argv) == 4
file_path = sys.argv[1]
file_path_pos = sys.argv[2]
h_mt = sys.argv[2]

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


def dataset_to_files(dataset, destination):

    with open(destination, 'w') as f:
        for line in dataset:
            f.write(line + '\n')


print("Reading datasets:" + file_path + "," + file_path_pos)
dataset, dataset_pos = read_datasets(file_path, file_path_pos)

print("Running rnnlm tool to obtain train scores")

for idx in range(len(dataset)):
    sentence = dataset[idx].replace('"', '\\\"')
    sentence = sentence.replace("'", "\\\'")
    
    command = ['/bin/zsh', 'time ./rnnlm-0.4b/rnnlm -model models/model_{} -test =(echo {})'.format(h_mt, dataset[idx])]

    print(' '.join(command))
    #proc = subprocess.Popen(command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    #stdout_value = proc.communicate()[0]

    #for line in stdout_value:
        #print(line)


