# -*- coding: utf-8 -*-
import os
import random
import sys
import subprocess


assert len(sys.argv) == 6
file_path = sys.argv[1]
file_path_pos = sys.argv[2]
src = sys.argv[3]
other = sys.argv[4]
train_test = sys.argv[5]

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


def datasets_to_file(dataset, dataset2, dataset_pos, dataset_pos2, sentence_length, header, destination):
#def datasets_to_file(dataset, dataset_pos, header, destination):

    with open(destination, 'w') as f:
        f.write(header + '\n')
        for idx in range(len(dataset)):
            f.write(dataset[idx] + ',' + dataset2[idx] + ',' + dataset_pos[idx] + ',' + dataset_pos2[idx] + ',' + sentence_length[idx] + '\n')


print("Reading datasets:" + file_path + "," + file_path_pos)
dataset, dataset_pos = read_datasets(file_path, file_path_pos)

print("Running rnnlm tool to obtain train scores")

features = range(len(dataset))
features_pos = range(len(dataset_pos))
features_2 = range(len(dataset))
features_pos_2 = range(len(dataset_pos))
sentence_length = range(len(dataset_pos))


#TODO length of sentence

for idx in range(len(dataset)):
    sentence = dataset[idx]
    #sentence = dataset[idx].replace('"', '\\\"')
    #sentence = sentence.replace("'", "\\\'")
    sentence = sentence.split(' ')
    sentence_length[idx] = len(sentence)    
    import tempfile

    ############### For me vs me ############### 
    with tempfile.NamedTemporaryFile() as temp:
        temp.write(dataset[idx])
        temp.flush()    
        command = './rnnlm-0.4b/rnnlm -rnnlm models/model_{} -test {}'.format(src, temp.name)

        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        stdout_value = proc.communicate()[0]
        
        log_probability = stdout_value.split('\n')[3].split(':')[1]
        features[idx] = log_probability.strip()
        
    with tempfile.NamedTemporaryFile() as temp:
        temp.write(dataset_pos[idx])
        temp.flush()    
        command = './rnnlm-0.4b/rnnlm -rnnlm models/model_{}_pos -test {}'.format(src, temp.name)

        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        stdout_value = proc.communicate()[0]

        log_probability = stdout_value.split('\n')[3].split(':')[1]
        features_pos[idx] = log_probability.strip()

    ############### For me vs other ############### 
    with tempfile.NamedTemporaryFile() as temp:
        temp.write(dataset[idx])
        temp.flush()    
        command = './rnnlm-0.4b/rnnlm -rnnlm models/model_{} -test {}'.format(other, temp.name)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        stdout_value = proc.communicate()[0]
 
        log_probability = stdout_value.split('\n')[3].split(':')[1]
        features_2[idx] = log_probability.strip()

        
    with tempfile.NamedTemporaryFile() as temp:
        temp.write(dataset_pos[idx])
        temp.flush()    
        command = './rnnlm-0.4b/rnnlm -rnnlm models/model_{}_pos -test {}'.format(other, temp.name)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        stdout_value = proc.communicate()[0]
 
        log_probability = stdout_value.split('\n')[3].split(':')[1]
        features_pos_2[idx] = log_probability.strip()

#    print("Current index {}".format(idx))

file_to_write = 'features/{}_scores_feat_{}'.format(train_test, src)
header = 'f_wh,f_wmt,f_posh,f_posmt,length'
datasets_to_file(features, features_2, features_pos, features_pos_2, sentence_length, header, file_to_write)

