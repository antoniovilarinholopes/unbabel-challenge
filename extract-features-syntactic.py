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


def datasets_to_file(dataset, dataset2, dataset_pos, dataset_pos2, sentence_length, num_prep, header, destination):
#def datasets_to_file(dataset, dataset_pos, header, destination):

    with open(destination, 'w') as f:
        f.write(header + '\n')
        for idx in range(len(dataset)):
            #f.write(dataset[idx] + ',' + dataset2[idx] + ',' + dataset_pos[idx] + ',' + dataset_pos2[idx] + ',' + sentence_length[idx] + ',' + num_prep +'\n')
            f.write('{},{},{},{},{},{}\n'.format(dataset[idx], dataset2[idx], dataset_pos[idx], dataset_pos2[idx], sentence_length[idx], num_prep[idx]))


print("Reading datasets:" + file_path + "," + file_path_pos)
dataset, dataset_pos = read_datasets(file_path, file_path_pos)

print("Extracting features")

f_wh = range(len(dataset))
f_posh = range(len(dataset_pos))
f_wmt = range(len(dataset))
f_posmt = range(len(dataset_pos))
sentence_length = range(len(dataset_pos))
number_of_prep = range(len(dataset_pos))


for idx in range(len(dataset)):
    sentence = dataset[idx]
    import re
    sentence_length[idx] = len([word for word in sentence.split(' ') if re.match("\w+",word, re.U)])
    number_of_prep[idx] = len(re.findall('sp[0C][0M][0S]',dataset_pos[idx]))
    import tempfile
    
    ############### For h ############### 
    with tempfile.NamedTemporaryFile() as temp:
        temp.write(dataset[idx])
        temp.flush()
        command = './rnnlm-0.4b/rnnlm -rnnlm models/model_h -test {}'.format(temp.name)

        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        stdout_value = proc.communicate()[0]

        log_probability = stdout_value.split('\n')[3].split(':')[1]
        f_wh[idx] = log_probability.strip()

    with tempfile.NamedTemporaryFile() as temp:
        temp.write(dataset_pos[idx])
        temp.flush()
        command = './rnnlm-0.4b/rnnlm -rnnlm models/model_h_pos -test {}'.format(temp.name)

        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        stdout_value = proc.communicate()[0]

        log_probability = stdout_value.split('\n')[3].split(':')[1]
        f_posh[idx] = log_probability.strip()
    ############### For mt ############### 
    with tempfile.NamedTemporaryFile() as temp:
        temp.write(dataset[idx])
        temp.flush()
        command = './rnnlm-0.4b/rnnlm -rnnlm models/model_mt -test {}'.format(temp.name)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        stdout_value = proc.communicate()[0]

        log_probability = stdout_value.split('\n')[3].split(':')[1]
        f_wmt[idx] = log_probability.strip()


    with tempfile.NamedTemporaryFile() as temp:
        temp.write(dataset_pos[idx])
        temp.flush()
        command = './rnnlm-0.4b/rnnlm -rnnlm models/model_mt_pos -test {}'.format(temp.name)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        stdout_value = proc.communicate()[0]

        log_probability = stdout_value.split('\n')[3].split(':')[1]
        f_posmt[idx] = log_probability.strip() 
 #    print("Current index {}".format(idx))


file_to_write = 'features_syntactic/{}_scores_feat_{}'.format(train_test, src)
header = 'f_wh,f_wmt,f_posh,f_posmt,length,num_prep'
datasets_to_file(f_wh, f_wmt, f_posh, f_posmt, sentence_length, number_of_prep, header, file_to_write)

