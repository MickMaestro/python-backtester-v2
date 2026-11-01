"""``ssa.mqh`` (MetaQuotes, 2007) — singular spectrum analysis ("caterpillar")
on fixed-size arrays — line-by-line port.

``fastsingular(X, n, l, s, Y)`` reconstructs the series from its first ``s``
eigen-components with lag ``l``; ``singularPCA(X, n, l, s, Y)`` returns the
single component ``s``. Eigenvalues are found by bisection on a Gaussian-
elimination sign count (``gaussSn``/``gaussbisectionl``) and eigenvectors by
back-substitution (``svector``), exactly as in the source.

The source's fixed array sizes are kept (``MaxCatLag = 10`` lags,
``MaxCompCol = 20`` components, ``MaxLen = 300`` bars) together with its
clamping of ``l``, ``s`` and ``n``. Reading past them raises ``IndexError``
here where MQL5 stops the indicator with "array out of range".

Fidelity note: ``svector``'s column-swap loop is written
``for(i1=0;i<=n-1;i++)`` in the source — it tests and increments the *outer*
loop's ``i`` while always swapping row 0. It only runs when a pivot is
exactly zero; the port reproduces it as written.
"""

from __future__ import annotations

from .mql_runtime import MathAbs, MathSqrt, fdiv

MaxCompCol = 20
MaxCatLag = 10
MaxLen = 300


def _matrix(rows: int, cols: int) -> list:
    return [[0.0] * cols for _ in range(rows)]


def Equal(x1, x2, t) -> None:
    N = len(x1)
    M = len(x1[0])
    for i in range(N):
        for j in range(M):
            x1[i][j] = x2[j][i] if t else x2[i][j]


def gaussSn(A, l: float, n: int) -> float:
    """Number of negative pivots of ``A - l·I`` (an eigenvalue count below l)."""
    B = _matrix(MaxCatLag, MaxCatLag)
    w = [0.0] * n
    Equal(B, A, 0)
    for i in range(n):
        B[i][i] = B[i][i] - l
    cp = 0
    for k in range(0, n - 1):
        for i in range(k + 1, n):
            if B[k][k] == 0:
                for i1 in range(n):
                    w[i1] = B[i1][k]
                    B[i1][k] = B[i1][k + 1]
                    B[i1][k + 1] = w[i1]
                cp = cp + 1
            c = fdiv(B[i][k], B[k][k])
            for j in range(n):
                B[i][j] = B[i][j] - B[k][j] * c
    count = 0
    for i in range(n):
        s2 = B[i][i]
        if s2 < 0:
            count = count + 1
    return 1.0 * count


def gaussbisectionl(A, k: int, n: int) -> float:
    maxnorm = 0.0
    for i in range(n):
        cn = 0.0
        for j in range(n):
            cn += A[i][j]
        if maxnorm < cn:
            maxnorm = cn
    a1 = 0.0
    b1 = 10 * maxnorm
    e1 = 1.0 * maxnorm / 10000000
    while MathAbs(b1 - a1) > e1:
        c = 1.0 * (a1 + b1) / 2
        if gaussSn(A, c, n) < k:
            a1 = c
        else:
            b1 = c
    return (a1 + b1) / 2.0


def svector(A, l: float, n: int, V) -> None:
    B = _matrix(MaxCatLag, MaxCatLag)
    w = [0.0] * n
    Equal(B, A, 0)
    for i in range(n):
        B[i][i] -= l
    cp = 0
    for k in range(0, n - 1):
        i = k + 1
        while i <= n - 1:
            if not B[k][k]:
                i1 = 0
                while i <= n - 1:          # sic: tests/increments i, swaps row i1=0
                    w[i1] = B[i1][k]
                    B[i1][k] = B[i1][k + 1]
                    B[i1][k + 1] = w[i1]
                    i += 1
                cp += 1
            c = fdiv(1.0 * B[i][k], B[k][k])
            for j in range(n):
                B[i][j] -= B[k][j] * c
            i += 1
    V[n - 1] = 1
    c = 1.0
    for i in range(n - 2, -1, -1):
        V[i] = 0
        for j in range(i, n):
            V[i] -= B[i][j] * V[j]
        V[i] = fdiv(V[i], B[i][i])
        c += V[i] * V[i]
    for i in range(n):
        V[i] /= MathSqrt(c)


def _embed(X, n, l):
    A = _matrix(MaxCatLag, MaxCatLag)
    B = _matrix(MaxLen, MaxCatLag)
    k = n - l + 1
    for i in range(l):
        for j in range(l):
            A[i][j] = 0
            for m in range(k):
                A[i][j] += X[i + m] * X[m + j]
                B[m][j] = X[m + j]
    return A, B, k


def _diagonal_average(Yn, Bn, i1, n, l, k, strict_else: bool) -> None:
    kb = k
    lb = l
    for i in range(n):
        Yn[i1][i] = 0
        if i < lb - 1:
            for j in range(i + 1):
                if l <= k:
                    Yn[i1][i] += Bn[j][i - j]
                elif strict_else or l > k:
                    Yn[i1][i] += Bn[i - j][j]
            Yn[i1][i] /= (1.0 * (i + 1))
        if lb - 1 <= i < kb - 1:
            for j in range(lb):
                if l <= k:
                    Yn[i1][i] += Bn[j][i - j]
                elif strict_else or l > k:
                    Yn[i1][i] += Bn[i - j][j]
            Yn[i1][i] = Yn[i1][i] / (1.0 * lb)
        if kb - 1 <= i:
            for j in range(i - kb + 1, n - kb + 1):
                if l <= k:
                    Yn[i1][i] += Bn[j][i - j]
                elif strict_else or l > k:
                    Yn[i1][i] += Bn[i - j][j]
            Yn[i1][i] /= (1.0 * (n - i))


def fastsingular(X, n: int, l: int, s: int, Y) -> None:
    """Reconstruct ``n`` values of ``X`` from its first ``s`` SSA components."""
    if l > MaxCatLag:
        l = MaxCatLag
    if s > MaxCompCol:
        s = MaxCompCol
    if s > l:
        s = l
    if n > MaxLen:
        n = MaxLen
    Bn = _matrix(MaxCatLag, MaxLen)
    V = _matrix(MaxCatLag, MaxLen)
    Yn = _matrix(MaxCatLag, MaxLen)
    ls = [0.0] * MaxCatLag
    Vtemp = [0.0] * MaxCatLag
    A, B, k = _embed(X, n, l)
    for i in range(s):
        ls[i] = gaussbisectionl(A, l - i, l)
        svector(A, ls[i], l, Vtemp)
        for j in range(l):
            V[i][j] = Vtemp[j]
    for i1 in range(s):
        for i in range(k):
            Yn[i1][i] = 0
            for j in range(l):
                Yn[i1][i] += B[i][j] * V[i1][j]
        for i in range(l):
            for j in range(k):
                Bn[i][j] = V[i1][i] * Yn[i1][j]
        _diagonal_average(Yn, Bn, i1, n, l, k, strict_else=True)
    for i in range(n):
        Y[i] = 0
        for i1 in range(s):
            Y[i] += Yn[i1][i]


def singularPCA(X, n: int, l: int, s: int, Y) -> None:
    """Reconstruct ``n`` values of ``X`` from SSA component number ``s`` only."""
    if l > MaxCatLag:
        l = MaxCatLag
    if s > MaxCompCol:
        s = MaxCompCol
    if s > l:
        s = l
    if n > MaxLen:
        n = MaxLen
    Bn = _matrix(MaxCatLag, MaxLen)
    V = _matrix(MaxCatLag, MaxLen)
    Yn = _matrix(MaxCatLag, MaxLen)
    ls = [0.0] * MaxCatLag
    Vtemp = [0.0] * MaxCatLag
    A, B, k = _embed(X, n, l)
    ls[s] = gaussbisectionl(A, l - s, l)
    svector(A, ls[s], l, Vtemp)
    for j in range(l):
        V[s][j] = Vtemp[j]
    i1 = s
    for i in range(k):
        Yn[i1][i] = 0
        for j in range(l):
            Yn[i1][i] += B[i][j] * V[i1][j]
    for i in range(l):
        for j in range(k):
            Bn[i][j] = V[i1][i] * Yn[i1][j]
    _diagonal_average(Yn, Bn, i1, n, l, k, strict_else=False)
    for i in range(n):
        Y[i] = 0
        Y[i] = Yn[s][i]
