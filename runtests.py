
if __name__ == '__main__':
    from charform import charform
    from parse import parse
    from sys import stderr, exit
    import argparse

    parser = argparse.ArgumentParser(
            description='Test charform.py on input file(s).')
    parser.add_argument(
            'files',
            metavar = 'FILE',
            nargs='+',
            help='input file(s)',
            )
    args = parser.parse_args()

    hdr_fmt = '# Outputs from charform.py on {}.'
    for in_file in args.files:
        print hdr_fmt.format(in_file)
        inputs = parse(in_file)
        for lineno, data in inputs:
            try:
                L = charform(*data)
                print (L, len(L))
            except Exception as e:
                print >> stderr, '--> [{}:{}] {}'.format(
                        args.file, lineno, data)
                raise e
