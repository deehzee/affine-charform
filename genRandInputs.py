# genRandInput.py - Generate ranodom input

def random_inputs(N = 5, maxvarn = 4, maxs = 3):
    # N = size of each sample size for each kind
    # maxvarn = maximum variation for n
    # maxs = maximum value for s_i
    # X = type (A, B, C, D, E or F)
    # n = subscript
    # r = superscript
    # S = specialization
    # in $X_n^{(r)}$
    # k = number of nodes (GCM A is (k x k) matrix)

    import random
    sfrom = range(maxs + 1)

    #
    # Aff-1: r=1
    #
    r = 1

    # Type $A_n^{(1)}$
    X = "A"
    nfrom = range(1, maxvarn + 1)
    for _ in range(N):
        n = random.choice(nfrom)
        k = n + 1
        S = [random.choice(sfrom) for i in range(k)]
        print(X, n, r, S)

    # Type $B_n^{(1)}$
    X = "B"
    nfrom = range(3, maxvarn + 3)
    for _ in range(N):
        n = random.choice(nfrom)
        k = n + 1
        S = [random.choice(sfrom) for i in range(k)]
        print(X, n, r, S)

    # Type $C_n^{(1)}$
    X = "C"
    nfrom = range(2, maxvarn + 2)
    for _ in range(N):
        n = random.choice(nfrom)
        k = n + 1
        S = [random.choice(sfrom) for i in range(k)]
        print(X, n, r, S)

    # Type $D_n^{(1)}$
    X = "D"
    nfrom = range(4, maxvarn + 4)
    for _ in range(N):
        n = random.choice(nfrom)
        k = n + 1
        S = [random.choice(sfrom) for i in range(k)]
        print(X, n, r, S)

    # Type $E_n^{(1)}$
    X = "E"
    nfrom = [6, 7, 8]
    for _ in range(N):
        n = random.choice(nfrom)
        k = n + 1
        S = [random.choice(sfrom) for i in range(k)]
        print(X, n, r, S)

    # Type $F_n^{(1)}$
    X, n = "F", 4
    k = n + 1
    for _ in range(N):
        S = [random.choice(sfrom) for i in range(k)]
        print(X, n, r, S)

    # Type $G_n^{(1)}$
    X, n = "G", 2
    k = n + 1
    for _ in range(N):
        S = [random.choice(sfrom) for i in range(k)]
        print(X, n, r, S)

    #
    # Aff-2
    #
    r = 2

    # Type $A_n^{(2)}:
    X = "A"
    ## n is even
    nfrom = range(2, 2 + 2*maxvarn, 2)
    for _ in range(N):
        n = random.choice(nfrom)
        k = n/2 + 1
        S = [random.choice(sfrom) for i in range(k)]
        print(X, n, r, S)
    ## n is odd
    nfrom = range(5, 5 + 2*maxvarn, 2)
    for _ in range(N):
        n = random.choice(nfrom)
        k = (n + 1)/2 + 1
        S = [random.choice(sfrom) for i in range(k)]
        print(X, n, r, S)

    # Type $D_n^{(2)}
    X = "D"
    nfrom = range(3, 3 + maxvarn)
    for _ in range(N):
        n = random.choice(nfrom)
        k = n
        S = [random.choice(sfrom) for i in range(k)]
        print(X, n, r, S)

    # Type $E_n^{(2)}$
    X, n = "E", 6
    k = n - 1
    for _ in range(N):
        S = [random.choice(sfrom) for i in range(k)]
        print(X, n, r, S)

    #
    # Aff-3
    #
    r = 3

    # Type $D_n^{(3)}
    X, n = "D", 4
    k = n - 1
    for _ in range(N):
        S = [random.choice(sfrom) for i in range(k)]
        print(X, n, r, S)

    # End of random_inputs(...)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
            description='Generate random inputs.'
            )
    parser.add_argument(
            '-N',
            metavar='NRAND',
            help='the number of inputs per test cases (default 5)',
            action='store',
            #dest='N',
            type=int,
            default=5,
            )
    parser.add_argument(
            '-n', '--varn',
            metavar='VARN',
            help="the variability range for the parameter 'n' \
                    (default 4)",
            action='store',
            type=int,
            default=4,
            )
    parser.add_argument(
            '-s', '--maxs',
            metavar='MAXS',
            help="the max value for each 's_i's (default 3)",
            action='store',
            type=int,
            default=3,
            )
    parser.add_argument(
            '-m', '--message',
            metavar='HDR_MSG',
            help='the header message at the top',
            action='store',
            type=str,
            default=None,
            )
    args = parser.parse_args();
    # print args
    if args.message:
        print '# {}'.format(args.message)
    random_inputs(args.N, args.varn, args.maxs)
