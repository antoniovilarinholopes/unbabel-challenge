import os
import random
import sys
import subprocess


assert len(sys.argv) == 3
file_path = sys.argv[1]
h_mt = sys.argv[2]
#test_path = sys.argv[3]

def read_dataset(file_path_local):

    # SANITY CHECK
    assert os.path.isfile(file_path_local)

    dataset = []
    with open(file_path_local, 'r') as f_p:
        for line in f_p:
            dataset.append(line.strip())
    
    return dataset


def dataset_to_files(dataset, destination):

    with open(destination, 'w') as f:
        for line in dataset:
            f.write(line + '\n')


print("Reading " + file_path)
dataset = read_dataset(file_path)
dataset = dataset[:int(len(dataset)*0.2)]

print("Writing valid file required by rnnlm tool: It is just 80% of each set :)")
file_valid_data = 'data/valid_train_' + h_mt + '.txt'
dataset_to_files(dataset, file_valid_data)

print("Running rnnlm tool")

command = 'time ./rnnlm-0.4b/rnnlm -train {} -valid {} -rnnlm models/model_{} -hidden 100 -rand-seed 1 -bptt 3 -direct-order 3 -class 31 -direct 2 -binary'.format(file_path, file_valid_data, h_mt)
print(command)

proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
stdout_value = proc.communicate()[0]

log_file = "log_file_{}.txt".format(h_mt)

with open(log_file, 'w') as log:
    for line in stdout_value:
        f.write(line+'\n')


#commad = 'ngram-count -text {} -order 5 -lm models/templm_{} -kndiscount -interpolate -gt3min 1 -gt4min 1'.format(file_path, h_mt)
#command = 'ngram -lm models/templm_{} -order 5 -ppl {} -debug 2 > models/temp_{}.ppl' .format(h_mt, test_path, h_mt)
