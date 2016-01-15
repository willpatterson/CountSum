import argparse

import os, sys
sys.path.append(os.path.abspath(".."))

from count_sum import count_sum as count_sum

def description():
    return "Sums and preforms operations on count files with two rows when ROW_1 is the name and ROW_2 is the count value"

def main(args=None):
    if args is None:
        if (sys.argv[1] == "-h") or (sys.argv[1] == "--help"):
            print(description())
            print("""USAGE:
        sum       -- Sum count values in corresponding file pairs
        zero      -- Sum files, if a gene count is 0, set all congruent genes to 0 (or delete)
        average   -- Sum files, if the average count is below a threshold, set all congruent genes to 0 (or delete)
        less_than -- Sum files, if the total count is below a threshold, set all congruent genes to 0 (or delete)
        """)
            sys.exit(1)
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(description=description())

    subparsers = parser.add_subparsers()
    subparsers.required = True

    zero_parser = subparsers.add_parser("zero")
    zero_parser.set_defaults(which='zero')

    average_parser = subparsers.add_parser("average")
    average_parser.set_defaults(which="average")

    gt_parser = subparsers.add_parser("less_than")
    gt_parser.set_defaults(which="less_than")

    sum_parser = subparsers.add_parser("sum")
    sum_parser.set_defaults(which="sum")


    try:
        parsed_args = parser.parse_args([args[0]])

        if (parsed_args.which == "zero"):
            zero(args[1:])
        if (parsed_args.which == "average") or (parsed_args.which == "less_than"):
            threshold(args[1:], parsed_args.which)
        if parsed_args.which == "sum":
            raw_sum(args[1:])
    except IndexError as e:
        print("Usage: /path/to/dir {zero, sum, less_than, average}")

def common_args():
    parser = argparse.ArgumentParser(description=description())
    parser.add_argument("directory", help="Directory containing sub directories with count files")
    parser.add_argument("-d", "--delete", action="store_true", dest='del_flag', default=False, help="Deleted Flagged lines")
    return parser

def zero(args):
    parser = common_args()
    parsed_args = parser.parse_args(args)

    count_sum.write_files(count_sum.zero_all(parsed_args.directory, delete_flag=parsed_args.del_flag))

def threshold(args, which):
    parser = common_args()
    parser.add_argument("threshold", type=int, help="Count threshold")
    parsed_args = parser.parse_args(args)

    if which == "less_than":
        count_sum.write_files(count_sum.less_than(parsed_args.directory,
                                                  parsed_args.threshold,
                                                  delete_flag=parsed_args.del_flag))
    elif which == "average":
        count_sum.write_files(count_sum.average_all(parsed_args.directory,
                                                    parsed_args.threshold,
                                                    delete_flag=parsed_args.del_flag))

def raw_sum(args):
    parser = argparse.ArgumentParser(description=description())
    parser.add_argument("directory", help="Directory containing sub directories with count files")
    parsed_args = parser.parse_args(args)
    count_sum.write_files(count_sum.get_file_data(parsed_args.directory))


if __name__ == '__main__':
    main()
