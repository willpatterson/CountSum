"""
File Name: Count_sum.py
Author   : William Patterson
Email    : wpatt2@pdx.edu

Description:
"""
import os
import collections
import argparse

def sum_files(file_one, file_two):
    """Sum every count value in the two files"""
    with open(file_one, 'r') as fone, open(file_two, 'r') as ftwo:
        gene_dict_one = collections.OrderedDict()
        gene_dict_two = collections.OrderedDict()
        for line in fone:
            split_line = line.split("\t")
            gene_dict_one[split_line[0]] = int(split_line[1])

        for tline in ftwo:
            split_line_two = tline.split("\t")
            gene_dict_two[split_line_two[0]] = int(split_line_two[1])

    #master = collections.OrderedDict()
    DataRow = namedtuple('DataRow', ['name', 'count_val'])
    for name, value in gene_dict_one.items():
        #yield "{name}\t{sum}\n".format(name=name, sum= value+ gene_dict_two[name])
        yield (DataRow(name=name, count_val=value + gene_dict_two[name]))

    """
    raw_file_name_one = os.path.basename(file_one)
    raw_file_name_two = os.path.basename(file_two)
    for name,
    return (raw_file_name_one + raw_file_name_two + "_counts.txt" , master)
    """



def zero_all(dir_path):
    sumed_data = get_file_data(dir_path)

    for file_data in sumed_data:
        for name, value in file_data.data_set.items():
            if value == 0:
                for data in sumed_data:
                    data[name] = 0

    write_file(sumed_data)

def average_all(dir_path, threshold):
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
                file_data.data_set[name] = 0

    write_file(sumed_data)

def open_count_files(dir_path):
    """Generates files from dirpath"""
    dir_list = os.listdir(dir_path)
    for item in dir_list:
        item_path = dir_path + '/' + item
        if os.path.isdir(item_path):
            count_files = os.listdir(item_path)
            if len(count_files) == 2:
                yield (os.path.join(item_path, count_files[0]), os.path.join(item_path, count_files[1]))

def write_file(sumed_data):
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


def count_comparison(dir_path):
    sumed_data = []
    for file_set in open_count_files(dir_path):
        ordered_data = collections.OrderedDict()
        for name, value in sum_files(file_set[1], file_set[2]):
            ordered_data[name] = value
        sumed_data.append(ordered_data)

    #get the average of all of the lines in every file 
    #If it is under a cirtain threshold, replace with zeros

    #Zero All data
    for data_set in sumed_data:
        for item in data_set[1].items():
            if item[1] == 0: #
                for data in sumed_data:
                    data[1][item[0]] = 0

    out_path = dir_path + '/out'
    try:
        os.makedirs(out_path)
    except OSError:
        pass #fix this

    for data_set in sumed_data:
        with open(out_path + '/' + data_set[0], 'w') as wfile:
            for line in data_set[1].items():
                wfile.write(line[0] + '\t' + str(line[1]) + '\n')

def get_args():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-d", '--directory', dest="dir_path", required=True, help="Directories containing sub directories with count files")
    return parser.parse_args()

def main():
    args = get_args()
    if os.path.exists(args.dir_path):
        count_comparison(args.dir_path)
    else:
        print "Could not find directory {d}".format(d=args.dir_path)

if __name__ == "__main__":
    #count_comparison('/disk/efscratch/Will')
    main()
