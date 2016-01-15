"""
File Name: count_sum.py
Author   : William Patterson
Co-Author: Amie Romney
Email    : wpatt2@pdx.edu, arom2@pdx.edu

Description:
This script module provides functions to load, sum, and filter genetic count files
"""

import os
from collections import OrderedDict, namedtuple

def write_raw_sums(dir_path):
    """Sums and writes count file pairs"""
    write_files(get_file_data(dir_path))

def zero_all(dir_path, delete_flag=False):
    """Filters for zeros"""
    sumed_data = get_file_data(dir_path)

    for file_data in sumed_data:
        for name, value in file_data.data_set.items():
            if value == 0:
                for data in sumed_data:
                    if delete_flag is False:
                        data.data_set[name] = 0
                    else:
                        del data.data_set[name]

    return sumed_data

def less_than(dir_path, threshold, delete_flag=False):
    """Gets the total count for a gene and filters if its lower than threshold"""
    sumed_data = get_file_data(dir_path)
    for name, value in sumed_data[0].data_set.items():
        count_sum = value
        for file_data in sumed_data[1:]:
            count_sum += file_data.data_set[name]
        if count_sum < threshold:
            for file_data in sumed_data:
                if delete_flag is False:
                    file_data.data_set[name] = 0
                else:
                    del file_data.data_set[name]

    return sumed_data

def average_all(dir_path, threshold, delete_flag=False):
    """Gets the average count for a gene and filters if its lower than threshold"""
    sumed_data = get_file_data(dir_path)
    for name, value in sumed_data[0].data_set.items():
        count_sum = value
        count = 1
        for file_data in sumed_data[1:]:
            count_sum += file_data.data_set[name]
            count += 1
        average = count_sum/count
        if average < threshold:
            for file_data in sumed_data:
                if delete_flag is False:
                    file_data.data_set[name] = 0
                else:
                    del file_data.data_set[name]

    return sumed_data

def write_files(sumed_data):
    """Writes files data contained in an ordered dictionary"""
    out_path = os.path.join(os.getcwd(), 'cs_out')
    try:
        os.makedirs(out_path)
    except OSError:
        pass #fix this

    for file_data in sumed_data:
        with open(os.path.join(out_path, file_data.outfile), 'w') as wfile:
            for row in file_data.data_set.items():
                wfile.write("{n}\t{v}\n".format(n=row[0], v=row[1]))


def open_count_files(dir_path):
    """Generates file paths from the specified directory path"""
    dir_list = os.listdir(dir_path)
    for item in dir_list:
        item_path = os.path.join(dir_path, item)
        if os.path.isdir(item_path):
            count_files = os.listdir(item_path)
            if len(count_files) == 2:
                print("Opening {}...".format(item_path))
                yield (os.path.join(item_path, count_files[0]), os.path.join(item_path, count_files[1]))

def sum_files(file_1, file_2):
    """Sum every count value in the two files"""
    print("Summing files:")
    print("F1: {}".format(file_1))
    print("F2: {}".format(file_2))

    with open(file_1, 'r') as fone, open(file_2, 'r') as ftwo:
        gene_dict_one = OrderedDict()
        gene_dict_two = OrderedDict()
        for line in fone:
            split_line = line.split("\t")
            gene_dict_one[split_line[0]] = int(split_line[1])

        for tline in ftwo:
            split_line_two = tline.split("\t")
            gene_dict_two[split_line_two[0]] = int(split_line_two[1])

    DataRow = namedtuple('DataRow', ['name', 'count_val'])
    for name, value in gene_dict_one.items():
        yield (DataRow(name=name, count_val=value + gene_dict_two[name]))

def get_file_data(dir_path):
    """Yields FileData Named tuples with the outfile name and an ordered dict of the count data"""
    sumed_data = []
    FileData = namedtuple('FileData', ['outfile', 'data_set'])
    for file_1, file_2 in open_count_files(dir_path):
        ordered_data = OrderedDict()
        for name, value in sum_files(file_1, file_2):
            ordered_data[name] = value

        of1 = str(file_1)
        of1 = of1[of1.rfind('/')+1:]
        of2 = str(file_2)
        of2 = of2[of2.rfind('/')+1:]

        outfile_name = "{f1}__{f2}.out".format(f1=of1, f2=of2)
        file_data = FileData(outfile=outfile_name, data_set=ordered_data)
        sumed_data.append(file_data)

    return sumed_data

