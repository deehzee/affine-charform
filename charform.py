# charform.py

# Compute the principal character formula.
def charform(X, n, r, S):
    nfin, rdual, imadim, Comat, delta = _init(X, n, r)
    if nfin + 1 != len(S):
        err_fmt = 'invalid spcialization - length should be {}.'
        raise ValueError(err_fmt.format(nfin + 1))
    if X == 'A' and n % 2 == 0 and r == 2:
        K = _genhitsA(Comat, S, rdual, delta, imadim, nfin)
    else:
        K = _genhits(Comat, S, rdual, delta, imadim, nfin)
    return _min_tile(K)

# What does it do?
# Raise ValueError for inapporpiate input
def _init(X, n, r):
    # Eror message if (X, n, r) isn't a valid affine Lie algebra
    error_msg = 'invalid affine Lie algebra ${}_{}^{{({})}}$'.\
            format(X, n, r)
    delta = []          # guard
    # Xfin = letter type for the semisimple Lie algebra corresponding
    #        to the dual of the given affine Lie algebra (i.e., the
    #        nodes labeled the same way, but the arrows are reversed)
    #
    # nfin = rank of the corresponding semisimple Lie algebra of the
    #        dual of the given affine Lie agebra
    #
    # ndual = the subscript for the dual of the given affine Lie
    #         algebra
    #
    # rdual = the superscript for the dual of the given affine Lie
    #         algebra
    #
    # imadim = ???
    #          dim of the root space for the imaginary root
    #          $s \delta$ where $s \not\equiv 0 \pmod{6}$
    #          for the dual of the given affine Lie algebra
    #        = (ndual - rk(dual(A))) / (rdual - 1)
    #        = (ndual - nfin) / (rdual - 1)
    #
    # Comat = coefficient matrix describing all the positive roots
    #         (with respect to the simple roots) of the semisimple
    #         Lie algebra corresponding to the dual of the given
    #         affine Lie algebra
    #
    # delta = delta of the dual of the given affine Lie algbra
    #
    # (See [Kac] for more details)
    if X == 'A':
        if r == 1:
            if n < 1:
                raise ValueError(error_msg)
            # Dual=(A, n, 1), DualFin=(A, n)
            nfin, rdual, imadim = n, 1, 0
            Comat = _comatA(nfin)
            delta = [1 for _ in range(nfin + 1)]
        elif r == 2:
            if n % 2 == 0:
                if n < 2:
                    raise ValueError(error_msg)
                # Dual=(A, n, 2)[opp], DualFin=(B, n/2)
                nfin, rdual, imadim = n/2, 2, n/2
                Comat = _comatA2(nfin)
                delta = [2 for _ in range(nfin + 1)]
                delta[0] = 1
            elif n % 2 == 1:
                if n < 5:
                    raise ValueError(error_msg)
                # Dual=(B, (n+1)/2, 1), DualFin=(B, (n+1)/2)
                nfin, rdual, imadim = (n+1)/2, 1, 0
                Comat = _comatB(nfin)
                delta = [2 for _ in range(nfin + 1)]
                delta[0] = delta[1] = 1
            else:
                raise ValueError(error_msg)
        else:
            raise ValueError(error_msg)
    elif X == 'B':
        if n < 3 or r != 1:
            raise ValueError(error_msg)
        # Dual=(A, 2*n-1, 2), DualFin=(C, n)
        nfin, rdual, imadim = n, 2, n-1
        Comat = _comatC(nfin)
        delta = [2 for _ in range(nfin + 1)]
        delta[0] = delta[1] = delta[nfin] = 1
    elif X == 'C':
        if n < 2 or r != 1:
            raise ValueError(error_msg)
        # Dual=(D, n+1, 2), DualFin=(B, n)
        nfin, rdual, imadim = n, 2, 1
        Comat = _comatB(nfin)
        delta = [1 for _ in range(nfin + 1)]
    elif X == 'D':
        if r == 1:
            if n < 4:
                raise ValueError(error_msg)
            # Dual=(D, n, 1), DualFin=(D, n)
            nfin, rdual, imadim = n, 1, 0
            Comat = _comatD(nfin)
            delta = [2 for _ in range(nfin + 1)]
            delta[0] = delta[1] = delta[nfin] = delta[nfin-1] = 1
        elif r == 2:
            if n < 3:
                raise ValueError(error_msg)
            # Dual=(C, n-1, 1), DualFin=(C, n-1)
            nfin, rdual, imadim = n-1, 1, 0
            Comat = _comatC(nfin)
            delta = [2 for _ in range(nfin + 1)]
            delta[0] = delta[nfin] = 1
        elif r == 3:
            if n != 4:
                raise ValueError(error_msg)
            # Dual=(G, 2, 1), DualFin=(G, 2)
            nfin, rdual, imadim = 2, 1, 0
            Comat = _CoeffG2
            delta = [1, 2, 3]
        else:
            raise ValueError(error_msg)
    elif X == 'E':
        if r == 1:
            if n == 6:
                Comat = _CoeffE6
                delta = [1, 1, 2, 3, 2, 1, 2]
            elif n == 7:
                Comat = _CoeffE7
                delta = [1, 2, 3, 4, 3, 2, 1, 2]
            elif n == 8:
                Comat = _CoeffE8
                delta = [1, 2, 3, 4, 5, 6, 4, 2, 3]
            else:
                raise ValueError(error_msg)
            # Dual=(E, n, 1), DualFin=(E, n)
            nfin, rdual, imadim = n, 1, 0
        elif r == 2:
            if n != 6:
                raise ValueError(error_msg)
            # Dual=(F, 4, 1), DualFin=(F, 4)
            nfin, rdual, imadim = 4, 1, 0
            Comat = _CoeffF4
            delta = [1, 2, 3, 4, 2]
        else:
            raise ValueError(error_msg)
    elif X == 'F':
        if n != 4 or r != 1:
            raise ValueError(error_msg)
        # Dual=(E, 6, 2), DualFin=(F, 4)[opp]
        nfin, rdual, imadim = 4, 2, 2
        Comat = _CoeffF4rev
        delta = [1, 2, 3, 2, 1]
    elif X == 'G':
        if n != 2 or r != 1:
            raise ValueError(error_msg)
        # Dual=(D, 4, 3), DualFin=(G, 2)[opp]
        nfin, rdual, imadim = 2, 3, 1
        Comat = _CoeffG2rev
        delta = [1, 2, 1]
    else:
        raise ValueError(error_msg)
    return nfin, rdual, imadim, Comat, delta

# What does it do:
def _genhitsA(C, S, rdual, delta, imadim, nfin):
    S1 = [s + 1 for s in S]
    # dotproduct of delta and S1:
    modulo = sum(d*s for d, s in zip(delta, S1))
    # powers = C * S1 (matrix times vector):
    powers = [sum(c*s for c, s in zip(R, S1)) for R in C]
    dim = modulo * rdual
    L = [0 for _ in xrange(dim)]
    L[dim - 1] = nfin
    for i in xrange(nfin * nfin):
        for j in (0, 1):
            p = j*modulo + powers[i]
            q = (j + 1)*modulo - powers[i]
            L[(p - 1) % dim] += 1  #[djn]
            L[(q - 1) % dim] += 1  #[djn]
    for i in xrange(nfin*nfin, nfin*(nfin + 1)):
        p = powers[i]
        q = dim - powers[i]
        L[(p - 1) % dim] += 1  #[djn]
        L[(q - 1) % dim] += 1  #[djn]
    L[modulo - 1] += imadim
    for i in xrange(dim):
        L[i] -= nfin
    return L

# What does it do:
def _genhits(C, S, rdual, delta, imadim, nfin):
    rows, cols = len(C), len(C[0])
    S1 = [s + 1 for s in S]
    # dotproduct of delta and S1:
    modulo = sum(d*s for d, s in zip(delta, S1))
    # powers = C * S1 (matrix times vector):
    # last column of C is long/short
    # augment 0 as the first column (effectively, the first entry
    # in S1 is ignored).
    powers = [sum(c*s for c, s in zip(R[:-1], S1[1:])) for R in C]
    dim = modulo * rdual
    L = [0 for _ in xrange(dim)]
    L[dim - 1] = nfin
    for i in xrange(rows):
        if C[i][cols - 1] == 'short':
            for j in range(rdual):
                p = j*modulo + powers[i]
                q = (j+1)*modulo - powers[i]
                L[(p - 1) % dim] += 1  #[djn]
                L[(q - 1) % dim] += 1  #[djn]
        else:
            p = powers[i]
            q = dim - powers[i]
            L[(p - 1) % dim] += 1  #[djn]
            L[(q - 1) % dim] += 1  #[djn]
    if rdual != 1:
        for i in range(1, rdual):
            L[modulo*i - 1] += imadim
    for i in range(dim):
        L[i] -= nfin
    return L

# Find the minimal tile that covers ``K``.
def _min_tile(K):
    A = []  # guard
    k = len(K)
    for i in [d for d in xrange(1, k+1) if k % d == 0]:
        A = K[:i]
        repeat = True
        for j in xrange(0, k, i):
            repeat = repeat and A == K[j:j+i]
            if not repeat: break
        if repeat: break
    return A

#
# NOTES:
#
# * Generate positive roots of various semisimple Lie algebras...
# * The body of the functions are opaque to me.
# * I don't understand what does _comatA2(n) does, or why it has
#   no short/long in the last column, unlike other similar functions.
#

def _comatA2(n):
    rows, cols = n*(n + 1), n + 1
    C = [[0 for _ in xrange(cols)] for _ in xrange(rows)]
    icur = 0
    for i in xrange(n):
        C[icur][i + 1] = 1
        icur += 1
    for i in xrange(n-1):
        for j in xrange(n-i):
            for k in xrange(i+2):
                C[icur][j + k] = 1
            icur += 1
    for i in xrange(n-2):
        for j in xrange(n-i-1, 1, -1):
            for k in xrange(n-i-1, 0, -1):
                if k >= j:
                    C[icur][k] = 1
                else:
                    C[icur][k] = 2
            C[icur][0] = 1
            icur += 1
    for i in xrange(n):
        for j in xrange(n-i-1):
            C[icur][j + 1] = 2
        C[icur][0] = 1
        icur += 1
    return C

def _comatA(n):
    rows, cols = (n*(n+1))/2, n+1
    C = [[0 for _ in xrange(cols)] for _ in xrange(rows)]
    icur = 0
    for i in xrange(n):
        for j in xrange(n-i):
            for k in xrange(i+1):
                C[icur][j + k] = 1
            icur += 1
    for i in xrange(rows):
        C[i][cols - 1] = 'long'
    return C

def _comatB(n):
    rows, cols = n*n, n+1
    C = [[0 for _ in xrange(cols)] for _ in xrange(rows)]
    icur = 0
    for i in xrange(n):
        for j in xrange(n-i):
            for k in xrange(i+1):
                C[icur][j + k] = 1
            icur += 1
    for i in xrange(n-1):
        for j in xrange(n-i-1):
            for k in xrange(i, n):
                if k <= i + j:
                    C[icur][k] = 1
                else:
                    C[icur][k] = 2
            icur += 1
    for i in xrange(rows):
        if C[i][cols - 2] == 1:
            C[i][cols - 1] = 'short'
        else:
            C[i][cols - 1] = 'long'
    return C

def _comatC(n):
    rows, cols = n*n, n+1
    C = [[0 for _ in xrange(cols)] for _ in xrange(rows)]
    icur = 0
    for i in xrange(n):
        for j in xrange(n-i):
            for k in xrange(i+1):
                C[icur][j + k] = 1
            icur += 1
    for i in xrange(n-1):
        for j in xrange(n-i-1):
            for k in xrange(i, n-1):
                if k < i + j:
                    C[icur][k] = 1
                else:
                    C[icur][k] = 2
            C[icur][n - 1] = 1
            icur += 1
    for i in xrange(rows):
        a = 0
        while C[i][a] == 0:
            a += 1
        if C[i][a] == 2 or a == n-1:
            C[i][cols - 1] = 'long'
        else:
            C[i][cols - 1] = 'short'
    return C

def _comatD(n):
    rows, cols = (n*n - n + 1), (n + 1)
    C = [[0 for _ in xrange(cols)] for _ in xrange(rows)]
    icur = 0
    for i in xrange(n):
        for j in xrange(n-i):
            for k in xrange(i+1):
                C[icur][j + k] = 1
            icur += 1
    for i in xrange(n-2):
        for j in xrange(i, n-2):
            C[icur][j] = 1
        C[icur][n - 1] = 1
        icur += 1
    for i in xrange(n-3):
        for j in xrange(n-i-3):
            for k in xrange(i, n-2):
                if k <= i + j:
                    C[icur][k] = 1
                else:
                    C[icur][k] = 2
            C[icur][n - 2] = 1
            C[icur][n - 1] = 1
            icur += 1
    del C[2*n - 2]
    for i in xrange(rows-1):
        C[i][cols - 1] = 'long'
    return C

_CoeffE6 = [[0, 0, 0, 0, 0, 1, "long"],
            [0, 0, 0, 0, 1, 0, "long"],
            [0, 0, 0, 1, 0, 0, "long"],
            [0, 0, 1, 0, 0, 0, "long"],
            [0, 1, 0, 0, 0, 0, "long"],
            [1, 0, 0, 0, 0, 0, "long"],
            [0, 0, 0, 1, 0, 1, "long"],
            [0, 0, 1, 0, 1, 0, "long"],
            [0, 0, 1, 1, 0, 0, "long"],
            [0, 1, 1, 0, 0, 0, "long"],
            [1, 1, 0, 0, 0, 0, "long"],
            [0, 0, 1, 1, 0, 1, "long"],
            [0, 0, 1, 1, 1, 0, "long"],
            [0, 1, 1, 0, 1, 0, "long"],
            [0, 1, 1, 1, 0, 0, "long"],
            [1, 1, 1, 0, 0, 0, "long"],
            [0, 0, 1, 1, 1, 1, "long"],
            [0, 1, 1, 1, 0, 1, "long"],
            [0, 1, 1, 1, 1, 0, "long"],
            [1, 1, 1, 0, 1, 0, "long"],
            [1, 1, 1, 1, 0, 0, "long"],
            [0, 1, 1, 1, 1, 1, "long"],
            [1, 1, 1, 1, 0, 1, "long"],
            [0, 1, 2, 1, 1, 0, "long"],
            [1, 1, 1, 1, 1, 0, "long"],
            [0, 1, 2, 1, 1, 1, "long"],
            [1, 1, 1, 1, 1, 1, "long"],
            [1, 1, 2, 1, 1, 0, "long"],
            [0, 1, 2, 2, 1, 1, "long"],
            [1, 1, 2, 1, 1, 1, "long"],
            [1, 2, 2, 1, 1, 0, "long"],
            [1, 1, 2, 2, 1, 1, "long"],
            [1, 2, 2, 1, 1, 1, "long"],
            [1, 2, 2, 2, 1, 1, "long"],
            [1, 2, 3, 2, 1, 1, "long"],
            [1, 2, 3, 2, 2, 1, "long"]]

_CoeffE7 = [[1, 0, 0, 0, 0, 0, 0, "long"],
            [0, 0, 0, 0, 0, 0, 1, "long"],
            [0, 1, 0, 0, 0, 0, 0, "long"],
            [0, 0, 1, 0, 0, 0, 0, "long"],
            [0, 0, 0, 1, 0, 0, 0, "long"],
            [0, 0, 0, 0, 1, 0, 0, "long"],
            [0, 0, 0, 0, 0, 1, 0, "long"],
            [1, 1, 0, 0, 0, 0, 0, "long"],
            [0, 0, 1, 0, 0, 0, 1, "long"],
            [0, 1, 1, 0, 0, 0, 0, "long"],
            [0, 0, 1, 1, 0, 0, 0, "long"],
            [0, 0, 0, 1, 1, 0, 0, "long"],
            [0, 0, 0, 0, 1, 1, 0, "long"],
            [1, 1, 1, 0, 0, 0, 0, "long"],
            [0, 1, 1, 0, 0, 0, 1, "long"],
            [0, 0, 1, 1, 0, 0, 1, "long"],
            [0, 1, 1, 1, 0, 0, 0, "long"],
            [0, 0, 1, 1, 1, 0, 0, "long"],
            [0, 0, 0, 1, 1, 1, 0, "long"],
            [1, 1, 1, 0, 0, 0, 1, "long"],
            [1, 1, 1, 1, 0, 0, 0, "long"],
            [0, 1, 1, 1, 0, 0, 1, "long"],
            [0, 0, 1, 1, 1, 0, 1, "long"],
            [0, 1, 1, 1, 1, 0, 0, "long"],
            [0, 0, 1, 1, 1, 1, 0, "long"],
            [1, 1, 1, 1, 0, 0, 1, "long"],
            [1, 1, 1, 1, 1, 0, 0, "long"],
            [0, 1, 2, 1, 0, 0, 1, "long"],
            [0, 1, 1, 1, 1, 0, 1, "long"],
            [0, 0, 1, 1, 1, 1, 1, "long"],
            [0, 1, 1, 1, 1, 1, 0, "long"],
            [1, 1, 2, 1, 0, 0, 1, "long"],
            [1, 1, 1, 1, 1, 0, 1, "long"],
            [1, 1, 1, 1, 1, 1, 0, "long"],
            [0, 1, 2, 1, 1, 0, 1, "long"],
            [0, 1, 1, 1, 1, 1, 1, "long"],
            [1, 2, 2, 1, 0, 0, 1, "long"],
            [1, 1, 2, 1, 1, 0, 1, "long"],
            [1, 1, 1, 1, 1, 1, 1, "long"],
            [0, 1, 2, 2, 1, 0, 1, "long"],
            [0, 1, 2, 1, 1, 1, 1, "long"],
            [1, 2, 2, 1, 1, 0, 1, "long"],
            [1, 1, 2, 2, 1, 0, 1, "long"],
            [1, 1, 2, 1, 1, 1, 1, "long"],
            [0, 1, 2, 2, 1, 1, 1, "long"],
            [1, 2, 2, 2, 1, 0, 1, "long"],
            [1, 2, 2, 1, 1, 1, 1, "long"],
            [1, 1, 2, 2, 1, 1, 1, "long"],
            [0, 1, 2, 2, 2, 1, 1, "long"],
            [1, 2, 3, 2, 1, 0, 1, "long"],
            [1, 2, 2, 2, 1, 1, 1, "long"],
            [1, 1, 2, 2, 2, 1, 1, "long"],
            [1, 2, 3, 2, 1, 0, 2, "long"],
            [1, 2, 3, 2, 1, 1, 1, "long"],
            [1, 2, 2, 2, 2, 1, 1, "long"],
            [1, 2, 3, 2, 1, 1, 2, "long"],
            [1, 2, 3, 2, 2, 1, 1, "long"],
            [1, 2, 3, 2, 2, 1, 2, "long"],
            [1, 2, 3, 3, 2, 1, 1, "long"],
            [1, 2, 3, 3, 2, 1, 2, "long"],
            [1, 2, 4, 3, 2, 1, 2, "long"],
            [1, 3, 4, 3, 2, 1, 2, "long"],
            [2, 3, 4, 3, 2, 1, 2, "long"]]

_CoeffE8 = [[0, 0, 0, 0, 0, 0, 1, 0, "long"],
            [0, 0, 0, 0, 0, 0, 0, 1, "long"],
            [0, 0, 0, 0, 0, 1, 0, 0, "long"],
            [0, 0, 0, 0, 1, 0, 0, 0, "long"],
            [0, 0, 0, 1, 0, 0, 0, 0, "long"],
            [0, 0, 1, 0, 0, 0, 0, 0, "long"],
            [0, 1, 0, 0, 0, 0, 0, 0, "long"],
            [1, 0, 0, 0, 0, 0, 0, 0, "long"],
            [0, 0, 0, 0, 0, 1, 1, 0, "long"],
            [0, 0, 0, 0, 1, 0, 0, 1, "long"],
            [0, 0, 0, 0, 1, 1, 0, 0, "long"],
            [0, 0, 0, 1, 1, 0, 0, 0, "long"],
            [0, 0, 1, 1, 0, 0, 0, 0, "long"],
            [0, 1, 1, 0, 0, 0, 0, 0, "long"],
            [1, 1, 0, 0, 0, 0, 0, 0, "long"],
            [0, 0, 0, 0, 1, 1, 1, 0, "long"],
            [0, 0, 0, 0, 1, 1, 0, 1, "long"],
            [0, 0, 0, 1, 1, 0, 0, 1, "long"],
            [0, 0, 0, 1, 1, 1, 0, 0, "long"],
            [0, 0, 1, 1, 1, 0, 0, 0, "long"],
            [0, 1, 1, 1, 0, 0, 0, 0, "long"],
            [1, 1, 1, 0, 0, 0, 0, 0, "long"],
            [0, 0, 0, 0, 1, 1, 1, 1, "long"],
            [0, 0, 0, 1, 1, 1, 1, 0, "long"],
            [0, 0, 0, 1, 1, 1, 0, 1, "long"],
            [0, 0, 1, 1, 1, 0, 0, 1, "long"],
            [0, 0, 1, 1, 1, 1, 0, 0, "long"],
            [0, 1, 1, 1, 1, 0, 0, 0, "long"],
            [1, 1, 1, 1, 0, 0, 0, 0, "long"],
            [0, 0, 0, 1, 1, 1, 1, 1, "long"],
            [0, 0, 1, 1, 1, 1, 1, 0, "long"],
            [0, 0, 0, 1, 2, 1, 0, 1, "long"],
            [0, 0, 1, 1, 1, 1, 0, 1, "long"],
            [0, 1, 1, 1, 1, 0, 0, 1, "long"],
            [0, 1, 1, 1, 1, 1, 0, 0, "long"],
            [1, 1, 1, 1, 1, 0, 0, 0, "long"],
            [0, 0, 0, 1, 2, 1, 1, 1, "long"],
            [0, 0, 1, 1, 1, 1, 1, 1, "long"],
            [0, 1, 1, 1, 1, 1, 1, 0, "long"],
            [0, 0, 1, 1, 2, 1, 0, 1, "long"],
            [0, 1, 1, 1, 1, 1, 0, 1, "long"],
            [1, 1, 1, 1, 1, 0, 0, 1, "long"],
            [1, 1, 1, 1, 1, 1, 0, 0, "long"],
            [0, 0, 0, 1, 2, 2, 1, 1, "long"],
            [0, 0, 1, 1, 2, 1, 1, 1, "long"],
            [0, 1, 1, 1, 1, 1, 1, 1, "long"],
            [1, 1, 1, 1, 1, 1, 1, 0, "long"],
            [0, 0, 1, 2, 2, 1, 0, 1, "long"],
            [0, 1, 1, 1, 2, 1, 0, 1, "long"],
            [1, 1, 1, 1, 1, 1, 0, 1, "long"],
            [0, 0, 1, 1, 2, 2, 1, 1, "long"],
            [0, 0, 1, 2, 2, 1, 1, 1, "long"],
            [0, 1, 1, 1, 2, 1, 1, 1, "long"],
            [1, 1, 1, 1, 1, 1, 1, 1, "long"],
            [0, 1, 1, 2, 2, 1, 0, 1, "long"],
            [1, 1, 1, 1, 2, 1, 0, 1, "long"],
            [0, 0, 1, 2, 2, 2, 1, 1, "long"],
            [0, 1, 1, 1, 2, 2, 1, 1, "long"],
            [0, 1, 1, 2, 2, 1, 1, 1, "long"],
            [1, 1, 1, 1, 2, 1, 1, 1, "long"],
            [0, 1, 2, 2, 2, 1, 0, 1, "long"],
            [1, 1, 1, 2, 2, 1, 0, 1, "long"],
            [0, 0, 1, 2, 3, 2, 1, 1, "long"],
            [0, 1, 1, 2, 2, 2, 1, 1, "long"],
            [1, 1, 1, 1, 2, 2, 1, 1, "long"],
            [0, 1, 2, 2, 2, 1, 1, 1, "long"],
            [1, 1, 1, 2, 2, 1, 1, 1, "long"],
            [1, 1, 2, 2, 2, 1, 0, 1, "long"],
            [0, 0, 1, 2, 3, 2, 1, 2, "long"],
            [0, 1, 1, 2, 3, 2, 1, 1, "long"],
            [0, 1, 2, 2, 2, 2, 1, 1, "long"],
            [1, 1, 1, 2, 2, 2, 1, 1, "long"],
            [1, 1, 2, 2, 2, 1, 1, 1, "long"],
            [1, 2, 2, 2, 2, 1, 0, 1, "long"],
            [0, 1, 1, 2, 3, 2, 1, 2, "long"],
            [0, 1, 2, 2, 3, 2, 1, 1, "long"],
            [1, 1, 1, 2, 3, 2, 1, 1, "long"],
            [1, 1, 2, 2, 2, 2, 1, 1, "long"],
            [1, 2, 2, 2, 2, 1, 1, 1, "long"],
            [0, 1, 2, 2, 3, 2, 1, 2, "long"],
            [1, 1, 1, 2, 3, 2, 1, 2, "long"],
            [0, 1, 2, 3, 3, 2, 1, 1, "long"],
            [1, 1, 2, 2, 3, 2, 1, 1, "long"],
            [1, 2, 2, 2, 2, 2, 1, 1, "long"],
            [0, 1, 2, 3, 3, 2, 1, 2, "long"],
            [1, 1, 2, 2, 3, 2, 1, 2, "long"],
            [1, 1, 2, 3, 3, 2, 1, 1, "long"],
            [1, 2, 2, 2, 3, 2, 1, 1, "long"],
            [0, 1, 2, 3, 4, 2, 1, 2, "long"],
            [1, 1, 2, 3, 3, 2, 1, 2, "long"],
            [1, 2, 2, 2, 3, 2, 1, 2, "long"],
            [1, 2, 2, 3, 3, 2, 1, 1, "long"],
            [0, 1, 2, 3, 4, 3, 1, 2, "long"],
            [1, 1, 2, 3, 4, 2, 1, 2, "long"],
            [1, 2, 2, 3, 3, 2, 1, 2, "long"],
            [1, 2, 3, 3, 3, 2, 1, 1, "long"],
            [0, 1, 2, 3, 4, 3, 2, 2, "long"],
            [1, 1, 2, 3, 4, 3, 1, 2, "long"],
            [1, 2, 2, 3, 4, 2, 1, 2, "long"],
            [1, 2, 3, 3, 3, 2, 1, 2, "long"],
            [1, 1, 2, 3, 4, 3, 2, 2, "long"],
            [1, 2, 2, 3, 4, 3, 1, 2, "long"],
            [1, 2, 3, 3, 4, 2, 1, 2, "long"],
            [1, 2, 2, 3, 4, 3, 2, 2, "long"],
            [1, 2, 3, 3, 4, 3, 1, 2, "long"],
            [1, 2, 3, 4, 4, 2, 1, 2, "long"],
            [1, 2, 3, 3, 4, 3, 2, 2, "long"],
            [1, 2, 3, 4, 4, 3, 1, 2, "long"],
            [1, 2, 3, 4, 4, 3, 2, 2, "long"],
            [1, 2, 3, 4, 5, 3, 1, 2, "long"],
            [1, 2, 3, 4, 5, 3, 2, 2, "long"],
            [1, 2, 3, 4, 5, 3, 1, 3, "long"],
            [1, 2, 3, 4, 5, 3, 2, 3, "long"],
            [1, 2, 3, 4, 5, 4, 2, 2, "long"],
            [1, 2, 3, 4, 5, 4, 2, 3, "long"],
            [1, 2, 3, 4, 6, 4, 2, 3, "long"],
            [1, 2, 3, 5, 6, 4, 2, 3, "long"],
            [1, 2, 4, 5, 6, 4, 2, 3, "long"],
            [1, 3, 4, 5, 6, 4, 2, 3, "long"],
            [2, 3, 4, 5, 6, 4, 2, 3, "long"]]

_CoeffF4 = [[0, 0, 0, 1, "short"],
            [0, 0, 1, 0, "short"],
            [0, 1, 0, 0, "long" ],
            [1, 0, 0, 0, "long" ],
            [0, 0, 1, 1, "short"],
            [0, 1, 1, 0, "short"],
            [0, 1, 2, 0, "long" ],
            [1, 1, 0, 0, "long" ],
            [0, 1, 1, 1, "short"],
            [1, 1, 1, 0, "short"],
            [0, 1, 2, 2, "long" ],
            [1, 1, 2, 0, "long" ],
            [0, 1, 2, 1, "short"],
            [1, 1, 1, 1, "short"],
            [1, 1, 2, 2, "long" ],
            [1, 2, 2, 0, "long" ],
            [1, 1, 2, 1, "short"],
            [1, 2, 2, 2, "long" ],
            [1, 2, 2, 1, "short"],
            [1, 2, 4, 2, "long" ],
            [1, 2, 3, 1, "short"],
            [1, 3, 4, 2, "long" ],
            [1, 2, 3, 2, "short"],
            [2, 3, 4, 2, "long" ]]

_CoeffF4rev = [[1, 0, 0, 0, "short"],
               [0, 1, 0, 0, "short"],
               [0, 0, 1, 0, "long" ],
               [0, 0, 0, 1, "long" ],
               [1, 1, 0, 0, "short"],
               [0, 1, 1, 0, "short"],
               [0, 2, 1, 0, "long" ],
               [0, 0, 1, 1, "long" ],
               [1, 1, 1, 0, "short"],
               [0, 1, 1, 1, "short"],
               [2, 2, 1, 0, "long" ],
               [0, 2, 1, 1, "long" ],
               [1, 2, 1, 0, "short"],
               [1, 1, 1, 1, "short"],
               [2, 2, 1, 1, "long" ],
               [0, 2, 2, 1, "long" ],
               [1, 2, 1, 1, "short"],
               [2, 2, 2, 1, "long" ],
               [1, 2, 2, 1, "short"],
               [2, 4, 2, 1, "long" ],
               [1, 3, 2, 1, "short"],
               [2, 4, 3, 1, "long" ],
               [2, 3, 2, 1, "short"],
               [2, 4, 3, 2, "long" ]]

_CoeffG2 = [[0, 1, "short"],
            [1, 0, "long" ],
            [1, 1, "short"],
            [1, 3, "long" ],
            [1, 2, "short"],
            [2, 3, "long" ]]

_CoeffG2rev = [[1, 0, "short"],
               [0, 1, "long" ],
               [1, 1, "short"],
               [3, 1, "long" ],
               [2, 1, "short"],
               [3, 2, "long" ]]
