# stdcp.py - Make standard copy

from parse import parse

if __name__ == '__main__':
    from sys import stderr
    import argparse

    parser = argparse.ArgumentParser(
            description="Make standardized copy onto stdout.",
            )
    parser.add_argument(
            'files',
            metavar = 'FILE',
            nargs='+',
            help='input file(s)',
            )
    args = parser.parse_args()
    # print args

    for in_file in args.files:
        lines = parse(in_file, linenum=False)
        for line in lines:
            print line
