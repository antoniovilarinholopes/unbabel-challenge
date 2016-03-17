# -*- coding: utf-8 -*-
import os
import random
import sys
import subprocess


assert len(sys.argv) == 6
file_path = sys.argv[1]
src = sys.argv[2]
other = sys.argv[3]
train_test = sys.argv[4]
score = sys.argv[5]

def read_datasets(file_path_local):

    # SANITY CHECK
    assert os.path.isfile(file_path_local)

    dataset = []
    with open(file_path_local, 'r') as f_p:
        for line in f_p:
            dataset.append(line.strip())
    
    return dataset


#def datasets_to_file(dataset, dataset2, dataset_pos, dataset_pos2, header, destination):
def datasets_to_file(score1_dataset, score2_dataset, header, destination):

    with open(destination, 'w') as f:
        f.write(header + '\n')
        for idx in range(len(dataset)):
            f.write(score1_dataset[idx] + ',' + score2_dataset[idx] + '\n')


print("Reading datasets:" + file_path)
dataset = read_datasets(file_path)

print("Running rnnlm tool to obtain train scores")

features = range(len(dataset))
features_2 = range(len(dataset))

#TODO length of sentence

for idx in range(len(dataset)):
    #sentence = dataset[idx].replace('"', '\\\"')
    #sentence = sentence.replace("'", "\\\'")
    import tempfile

    ############### For me vs me ############### 
    with tempfile.NamedTemporaryFile() as temp:
        temp.write(dataset[idx])
        temp.flush()    
        #temp.close()    
        command = './rnnlm-0.4b/rnnlm -rnnlm models/model_{} -test {}'.format(src, temp.name)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        stdout_value = proc.communicate()[0]
        line = ""
        for char in stdout_value:
            line += char
        
        log_probability = line.split('\n')[3].split(':')[1]
        features[idx] = log_probability

        
    ############### For me vs other ############### 
    with tempfile.NamedTemporaryFile() as temp:
        temp.write(dataset[idx])
        temp.flush()    
        #temp.close()    
        command = './rnnlm-0.4b/rnnlm -rnnlm models/model_{} -test {}'.format(other, temp.name)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        stdout_value = proc.communicate()[0]
        line = ""
        for char in stdout_value:
            line += char
        
        log_probability = line.split('\n')[3].split(':')[1]
        features_2[idx] = log_probability

file_to_write = 'features/{}_scores_feat_{}'.format(train_test, src)
header = 'f_{}, f_{}'.format(score + src, score + other)
datasets_to_file(features, features_2, header, file_to_write)

