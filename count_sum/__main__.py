import argparse

import os, sys
sys.path.append(os.path.abspath(".."))

import count_sum.count_sum

def main(args=None):
    if args is None:
        if (sys.argv[1] == "-h") or (sys.argv[1] == "--help"):
            print(description())
            print("""USAGE:""")
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(description())
    parser.add_argument("directory", help="Directorie containing sub directories with count files")

    subparsers = parser.add_subparsers()

    zero_parser = subparsers.add_parser("zero")
    zero_parser.set_defaults(which='zero')

    average_parser = subparsers.add_parser("average")
    average_parser.set_defaults(which="average")

    gt_parser = subparsers.add_parser("greater_than")
    gt_parser.set_defaults(which="greater_than")

    sum_parser = subparsers.add_parser("sum")
    sum_parser.set_defaults(which="sum")

    try:
        parsed_args = parser.parse_args([args[:1]])

        if parsed_args.which == "zero":
            zero(parsed_args.directory, args[1:])
        if (parsed_args.which == "average") or (parsed_args.which == "greater_than"):
            threshold(parsed_args.directory, args[1:], parsed_args.which)
        if parsed_args.which == "sum":
            raw_sum(parsed_args.directory)
    except:
        pass

def zero(directory, args):
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--delete", action="store_true", dest=del_flag, default=False, help="Deleted Flagged lines")
    parsed_args = parser.parse_args(args)

    count_sum.write_files(count_sum.zero_all(directory), delete_flag=parsed_args.del_flag)

def threshold(directory, args, which):
    parser = argparse.ArgumentParser()
    parser.add_argument("threshold", type=int, help="Count threshold")
    parser.add_argument("-d", "--delete", action="store_true", dest=del_flag, default=False, help="Deleted Flagged lines")
    parsed_args = parser.parse_args(args)

    if which == "greater_than":
        count_sum.write_files(count_sum.sum_greater_than(directory, delete_flag=parse_args.del_flag))
    elif which == "average":
        count_sum.write_files(count_sum.average_all(directory, delete_flag=parse_args.del_flag))

def raw_sum(directory):
    count_sum.write_files(count_sum.get_file_data(directory))
