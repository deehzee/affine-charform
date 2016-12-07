# check.py - Check if the outputs pass/fail the tests
# Usage: check.py (-i FILE | -c FILE1 FILE2)

from sys import stderr
from parse import parse

def integrity_check(filename):
    passed, total = 0, 0
    data = parse(filename)
    for lineno, value in data:
        total += 1
        try:
            L, d = value
            if len(L) != d:
                raise Exception('length does not match')
            passed += 1
        except Exception as e:
            print >> stderr, '--> [{}:{}] {}'.format(
                    filename, lineno, value)
            print >> stderr, e
    return passed, total

def compare_tests(file0, file1):
    passed, total = 0, 0
    data0, data1 = parse(file0), parse(file1)
    # Assuming that file0 and file1 have passed integrity_check()
    for (line0, value0), (line1, value1) in zip(data0, data1):
        total += 1
        try:
            if value0 != value1:
                raise Exception('values are not equal')
            passed += 1
        except Exception as e:
            print >> stderr, '--> [{}:{}] {}'.format(
                    file0, line0, value0)
            print >> stderr, '--> [{}:{}] {}'.format(
                    file1, line1, value1)
            print >> stderr, e
    return passed, total


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
            description='Check if the output file pass/fail the\
                    tests.'
            )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
            '-i',
            metavar='FILE',
            help="check integrity of the outputs in FILE",
            )
    group.add_argument(
            '-c',
            nargs=2,
            metavar='FILE',
            help="check FILE2 against FILE1 (line by line as python \
                    objects)",
            )
    args = parser.parse_args()
    # print args

    if args.i:
        # Do integrity check
        in_file = args.i
        print "Checking self-integrity of {}...".format(in_file)
        passed, total = integrity_check(in_file)
        print 'Passed {} of {}.'.format(passed, total)
    elif args.c:
        # Compare two output files
        in_file0, in_file1 = args.c
        print 'Comparing the outputs of {} and {}...'.format(
                in_file0, in_file1)
        passed, total = compare_tests(in_file0, in_file1)
        print 'Passed {} of {}.'.format(passed, total)
