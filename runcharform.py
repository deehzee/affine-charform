if __name__ == '__main__':
    from charform import *
    import argparse

    parser = argparse.ArgumentParser(
            description='Compute the principal specialization of the\
                    character of the vacuum space of a standard\
                    module for a affine Kac-Moody Lie algebra of\
                    type $X_n^{(r)}$.')

    parser.add_argument(
            'X',
            help='letter type for the affine Lie algebra\
                    (X = A, B, C, D, E, F or G)',
            type=str)

    parser.add_argument(
            'n',
            help='the subscript in the type of the affine Lie\
                    algebra (positive integer)',
            type=int)

    parser.add_argument(
            'r',
            help='the superscript in the type of the affine Lie\
                    algebra (r = 1, 2 or 3)',
            type=int)

    parser.add_argument(
            'S',
            help="the highest weight vector for the standard module\
                    (a list of nonnegative integers --\
                    quoted appropriately (e. g. '[0, 1]')).",
            type=str)

    args = parser.parse_args()
    # print args

    X, n, r, S = args.X, args.n, args.r, eval(args.S)
    L = charform(X, n, r, S)
    print L
    print len(L)
