import os
import random


def read_datasets(file_h, file_mt):

    # SANITY CHECK
    assert os.path.isfile(file_h) and os.path.isfile(file_mt)

    h = []
    mt = []

    with open(file_h, 'r') as f_h:
        for line in f_h:
            h.append(line.strip())

    with open(file_mt, 'r') as f_mt:
        for line in f_mt:
            mt.append(line.strip())

    return h, mt


def divide_dataset_idx(h, mt, valid=0.2):

    idx_h = range(len(h))
    idx_mt = range(len(mt))

    random.shuffle(idx_h)
    random.shuffle(idx_mt)

    limit_h = int(len(idx_h)*(1-valid))
    limit_mt = int(len(idx_mt)*(1-valid))

    train_h = idx_h[:limit_h]
    val_h = idx_h[limit_h:]

    train_mt = idx_mt[:limit_mt]
    val_mt = idx_mt[limit_mt:]

    return train_h, val_h, train_mt, val_mt


def dataset_to_files(dataset, train_idx, val_idx, dest_train, dest_val):

    with open(dest_train, 'w') as f_train:
        for idx in train_idx:
            f_train.write(dataset[idx] + '\n')

    with open(dest_val, 'w') as f_val:
        for idx in val_idx:
            f_val.write(dataset[idx] + '\n')

print("Reading h and mt datasets")
h, mt = read_datasets('processed_dataset/h_dataset.txt', 'processed_dataset/mt_dataset.txt')
t_h, v_h, t_mt, v_mt = divide_dataset_idx(h, mt)

print("Writiing h datasets: train and valid")
dataset_to_files(h, t_h, v_h, 'data/train_h.txt', 'data/validation_h.txt')
print("Writiing mt datasets: train and valid")
dataset_to_files(mt, t_mt, v_mt, 'data/train_mt.txt', 'data/validation_mt.txt')

print("Reading h and mt POS datasets")
h_pos, mt_pos = read_datasets('processed_dataset/h_dataset_pos.txt', 'processed_dataset/mt_dataset_pos.txt')

print("Writiing h POS datasets: train and valid")
dataset_to_files(h_pos, t_h, v_h, 'data/train_h_pos.txt', 'data/validation_h_pos.txt')
print("Writiing mt POS datasets: train and valid")
dataset_to_files(mt_pos, t_mt, v_mt, 'data/train_mt_pos.txt', 'data/validation_mt_pos.txt')

print("Saving indexes")
with open('data/train_mt_idx.txt', 'w') as index_train:
    for idx in t_mt:
        index_train.write('{}\n'.format(idx))

with open('data/train_h_idx.txt', 'w') as index_train:
    for idx in t_h:
        index_train.write('{}\n'.format(idx))

with open('data/valid_mt_idx.txt', 'w') as index_valid:
    for idx in v_mt:
        index_valid.write('{}\n'.format(idx))

with open('data/valid_h_idx.txt', 'w') as index_valid:
    for idx in v_h:
        index_valid.write('{}\n'.format(idx))

