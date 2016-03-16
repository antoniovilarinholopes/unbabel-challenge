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
            f_train.write(dataset[idx]+'\n')

    with open(dest_val, 'w') as f_val:
        for idx in val_idx:
            f_val.write(dataset[idx]+'\n')


h, mt = read_datasets('processed_dataset/h_dataset.txt', 'processed_dataset/mt_dataset.txt')
t_h, v_h, t_mt, v_mt = divide_dataset_idx(h, mt)
dataset_to_files(h, t_h, v_h, 'data/train_h.txt', 'data/validation_h.txt')
dataset_to_files(mt, t_mt, v_mt, 'data/train_mt.txt', 'data/validation_mt.txt')

h_pos, mt_pos = read_datasets('processed_dataset/h_dataset_pos.txt', 'processed_dataset/mt_dataset_pos.txt')
t_h_pos, v_h_pos, t_mt_pos, v_mt_pos = divide_dataset_idx(h_pos, mt_pos)
dataset_to_files(h_pos, t_h_pos, v_h_pos, 'data/train_h_pos.txt', 'data/validation_h_pos.txt')
dataset_to_files(mt_pos, t_mt_pos, v_mt_pos, 'data/train_mt_pos.txt', 'data/validation_mt_pos.txt')
