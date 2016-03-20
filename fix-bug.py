import csv
import os
import random
import numpy as np
import sys


def open_csv(file_path, to_write):
    # Input read as f_wh, f_wmt, f_posh, f_posmt, f_len, y

    assert os.path.isfile(file_path)

    raw_data = []
    with open(file_path, 'r') as fid:
        csv_reader = csv.reader(fid)
        for row in csv_reader:
            raw_data.append(row)
    header = raw_data[0]
    raw_data = raw_data[1:]
    with open(to_write, 'w') as csvfile:
        csv_file = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        csv_file.writerow(header)
        
        for elem in raw_data:
            tmp = elem[0]
            elem[0] = elem[1]
            elem[1] = tmp
                
            tmp = elem[2]
            elem[2] = elem[3]
            elem[3] = tmp

            csv_file.writerow(elem)

path = sys.argv[1]
other_path = sys.argv[2]
open_csv(path, other_path)
