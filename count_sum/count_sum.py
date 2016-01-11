"""
File Name: Count_sum.py
Author   : William Patterson
Email    : wpatt2@pdx.edu

Description:
"""
import os
import collections
import argparse

def sum_files(file_1, file_2):
    """Sum every count value in the two files"""
    with open(file_1, 'r') as fone, open(file_2, 'r') as ftwo:
        gene_dict_one = collections.OrderedDict()
        gene_dict_two = collections.OrderedDict()
        for line in fone:
            split_line = line.split("\t")
            gene_dict_one[split_line[0]] = int(split_line[1])

        for tline in ftwo:
            split_line_two = tline.split("\t")
            gene_dict_two[split_line_two[0]] = int(split_line_two[1])

    DataRow = namedtuple('DataRow', ['name', 'count_val'])
    for name, value in gene_dict_one.items():
        yield (DataRow(name=name, count_val=value + gene_dict_two[name]))

def write_raw_sums(dir_path):
    write_files(get_file_data(dir_path))

def zero_all(dir_path, delete_flag=False):
    sumed_data = get_file_data(dir_path)

    for file_data in sumed_data:
        for name, value in file_data.data_set.items():
            if value == 0:
                for data in sumed_data:
                    if delete_flag is False:
                        data.data_set[name] = 0
                    else:
                        del data.data_set[name]

    write_files(sumed_data)

def sum_greater_than(dir_path, threshold, delete_flag=False):
    sumed_data = get_file_data(dir_path)
    for name, value in sumed_data[0].data_set.items():
        count_sum = value
        for file_data in sumed_data[1:]:
            count_sum += file_data.data_set[name]
            count += 1
        if count_sum < threshold:
            for file_data in sumed_data:
                if delete_flag is False:
                    file_data.data_set[name] = 0
                else:
                    del file_data.data_set[name]

    write_files(sumed_data)

def average_all(dir_path, threshold, delete_flag=False):
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

    write_files(sumed_data)

def open_count_files(dir_path):
    """Generates file paths from the specified directory path"""
    dir_list = os.listdir(dir_path)
    for item in dir_list:
        item_path = os.path.join(dir_path, item)
        if os.path.isdir(item_path):
            count_files = os.listdir(item_path)
            if len(count_files) == 2:
                yield (os.path.join(item_path, count_files[0]), os.path.join(item_path, count_files[1]))

def write_files(sumed_data):
    out_path = os.path.join(dir_path, 'out')
    try:
        os.makedirs(out_path)
    except OSError:
        pass #fix this

    for file_data in sumed_data:
        with open(os.path.join(out_path, file_data.outfile), 'w') as wfile:
            for row in file_data.data_set.items():
                wfile.write("{name}\t{value}\n".format(name=row.name[0], value=row.count_val))

def get_file_data(dir_path):
    sumed_data = []
    FileData = namedtuple('FileData', ['outfile', 'data_set'])
    for file_1, file_2 in open_count_files(dir_path):
        ordered_data = collections.OrderedDict()
        for name, value in sum_files(file_1, file_2):
            ordered_data[name] = value

        outfile_name = "{f1}__{f2}.out".format(f1=file_1, f2=file_2)
        file_data = FileData(outfile=outfile_name, data_set=ordered_data)
        yield file_data


if __name__ == "__main__":
    pass
