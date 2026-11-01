"""ssa.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *


def Equal(x1, x2, t):
    N = ArrayRange(x1, 0)
    M = ArrayRange(x1, 1)
    for i in range(0, N):
        for j in range(0, M):
            if t:
                x1[i][j] = x2[j][i]
            else:
                x1[i][j] = x2[i][j]

def gaussSn(A, l, n):
    count = 0
    cp = 0
    i1 = 0
    i = 0
    j = 0
    k = 0
    B = Arr.of([0.0], fill=0.0, dyn=False, size=10, dims=(10,))
    c = 0.0
    w = Arr(0, 0.0)
    ArrayResize(w, n)
    s1 = 0.0
    s2 = 0.0
    Equal(B, A, 0)
    i = 0
    for i in range(i, n):
        B[i][i] = B[i][i] - l
    else:
        i = _range_end(i, n, 1)
    cp = 0
    k = 0
    for k in range(k, n - 2 + 1):
        i = k + 1
        for i in range(i, n - 1 + 1):
            if B[k][k] == 0:
                i1 = 0
                for i1 in range(i1, n - 1 + 1):
                    w[i1] = B[i1][k]
                    B[i1][k] = B[i1][k + 1]
                    B[i1][k + 1] = w[i1]
                else:
                    i1 = _range_end(i1, n - 1 + 1, 1)
                cp = cp + 1
            c = _fdiv(B[i][k], B[k][k])
            j = 0
            for j in range(j, n - 1 + 1):
                B[i][j] = B[i][j] - (B[k][j] * c)
            else:
                j = _range_end(j, n - 1 + 1, 1)
        else:
            i = _range_end(i, n - 1 + 1, 1)
    else:
        k = _range_end(k, n - 2 + 1, 1)
    count = 0
    s1 = 1.0
    i = 0
    for i in range(i, n - 1 + 1):
        s2 = B[i][i]
        if s2 < 0:
            count = count + 1
    else:
        i = _range_end(i, n - 1 + 1, 1)
    ArrayFree(w)
    return 1.0 * count

def gaussbisectionl(A, k, n):
    e1 = 0.0
    maxnorm = 0.0
    cn = 0.0
    a1 = 0.0
    b1 = 0.0
    c = 0.0
    i = 0
    j = 0
    maxnorm = 0.0
    i = 0
    for i in range(i, n - 1 + 1):
        cn = 0.0
        j = 0
        for j in range(j, n - 1 + 1):
            cn += A[i][j]
        else:
            j = _range_end(j, n - 1 + 1, 1)
        if maxnorm < cn:
            maxnorm = cn
    else:
        i = _range_end(i, n - 1 + 1, 1)
    a1 = 0.0
    b1 = 10 * maxnorm
    e1 = (1.0 * maxnorm) / 10000000
    while MathAbs(b1 - a1) > e1:
        c = (1.0 * (a1 + b1)) / 2
        if gaussSn(A, c, n) < k:
            a1 = c
        else:
            b1 = c
    return (a1 + b1) / 2.0

def svector(A, l, n, V):
    cp = 0
    i1 = 0
    i = 0
    j = 0
    k = 0
    B = Arr.of([0.0], fill=0.0, dyn=False, size=10, dims=(10,))
    c = 0.0
    w = Arr(0, 0.0)
    ArrayResize(w, n)
    Equal(B, A, 0)
    i = 0
    for i in range(i, n - 1 + 1):
        B[i][i] -= l
    else:
        i = _range_end(i, n - 1 + 1, 1)
    cp = 0
    k = 0
    for k in range(k, n - 2 + 1):
        i = k + 1
        while i <= (n - 1):
            if not B[k][k]:
                i1 = 0
                while i <= (n - 1):
                    w[i1] = B[i1][k]
                    B[i1][k] = B[i1][k + 1]
                    B[i1][k + 1] = w[i1]
                    i += 1
                cp += 1
            c = _fdiv(1.0 * B[i][k], B[k][k])
            j = 0
            for j in range(j, n - 1 + 1):
                B[i][j] -= B[k][j] * c
            else:
                j = _range_end(j, n - 1 + 1, 1)
            i += 1
    else:
        k = _range_end(k, n - 2 + 1, 1)
    V[n - 1] = 1.0
    c = 1.0
    i = n - 2
    for i in range(i, 0 - 1, -1):
        V[i] = 0.0
        j = i
        for j in range(j, n - 1 + 1):
            V[i] -= B[i][j] * V[j]
        else:
            j = _range_end(j, n - 1 + 1, 1)
        V[i] = _fdiv(V[i], B[i][i])
        c += V[i] * V[i]
    else:
        i = _range_end(i, 0 - 1, -1)
    i = 0
    for i in range(i, n - 1 + 1):
        V[i] = _fdiv(V[i], MathSqrt(c))
    else:
        i = _range_end(i, n - 1 + 1, 1)
    ArrayFree(w)

def fastsingular(X, n, l, s, Y):
    if l > 10:
        l = 10
    if s > 20:
        s = 20
    if s > l:
        s = l
    if n > 300:
        n = 300
    A = Arr.of([0.0], fill=0.0, dyn=False, size=10, dims=(10,))
    B = Arr.of([0.0], fill=0.0, dyn=False, size=300, dims=(10,))
    Bn = Arr.of([0.0], fill=0.0, dyn=False, size=10, dims=(300,))
    kb = 0
    lb = 0
    m = 0
    k = 0
    i = 0
    j = 0
    i1 = 0
    V = Arr.of([0.0], fill=0.0, dyn=False, size=10, dims=(300,))
    Yn = Arr.of([0.0], fill=0.0, dyn=False, size=10, dims=(300,))
    ls = Arr.of([0.0], fill=0.0, dyn=False, size=10)
    Vtemp = Arr.of([0.0], fill=0.0, dyn=False, size=10)
    j = 0
    k = n - l + 1
    i = 0
    for i in range(i, l - 1 + 1):
        j = 0
        for j in range(j, l - 1 + 1):
            A[i][j] = 0.0
            m = 0
            for m in range(m, k - 1 + 1):
                A[i][j] += X[i + m] * X[m + j]
                B[m][j] = X[m + j]
            else:
                m = _range_end(m, k - 1 + 1, 1)
        else:
            j = _range_end(j, l - 1 + 1, 1)
    else:
        i = _range_end(i, l - 1 + 1, 1)
    i = 0
    for i in range(i, s - 1 + 1):
        ls[i] = gaussbisectionl(A, l - i, l)
        svector(A, ls[i], l, Vtemp)
        j = 0
        for j in range(j, l - 1 + 1):
            V[i][j] = Vtemp[j]
        else:
            j = _range_end(j, l - 1 + 1, 1)
    else:
        i = _range_end(i, s - 1 + 1, 1)
    i1 = 0
    for i1 in range(i1, s - 1 + 1):
        i = 0
        for i in range(i, k - 1 + 1):
            Yn[i1][i] = 0.0
            j = 0
            for j in range(j, l - 1 + 1):
                Yn[i1][i] += B[i][j] * V[i1][j]
            else:
                j = _range_end(j, l - 1 + 1, 1)
        else:
            i = _range_end(i, k - 1 + 1, 1)
        i = 0
        for i in range(i, l - 1 + 1):
            j = 0
            for j in range(j, k - 1 + 1):
                Bn[i][j] = V[i1][i] * Yn[i1][j]
            else:
                j = _range_end(j, k - 1 + 1, 1)
        else:
            i = _range_end(i, l - 1 + 1, 1)
        kb = k
        lb = l
        i = 0
        for i in range(i, n - 1 + 1):
            Yn[i1][i] = 0.0
            if i < (lb - 1):
                j = 0
                for j in range(j, i + 1):
                    if l <= k:
                        Yn[i1][i] += Bn[j][i - j]
                    else:
                        Yn[i1][i] += Bn[i - j][j]
                else:
                    j = _range_end(j, i + 1, 1)
                Yn[i1][i] = _fdiv(Yn[i1][i], 1.0 * (i + 1))
            if (lb - 1) <= i and i < (kb - 1):
                j = 0
                for j in range(j, lb - 1 + 1):
                    if l <= k:
                        Yn[i1][i] += Bn[j][i - j]
                    else:
                        Yn[i1][i] += Bn[i - j][j]
                else:
                    j = _range_end(j, lb - 1 + 1, 1)
                Yn[i1][i] = _fdiv(Yn[i1][i], 1.0 * lb)
            if (kb - 1) <= i:
                j = i - kb + 1
                for j in range(j, n - kb + 1):
                    if l <= k:
                        Yn[i1][i] += Bn[j][i - j]
                    else:
                        Yn[i1][i] += Bn[i - j][j]
                else:
                    j = _range_end(j, n - kb + 1, 1)
                Yn[i1][i] = _fdiv(Yn[i1][i], 1.0 * (n - i))
        else:
            i = _range_end(i, n - 1 + 1, 1)
    else:
        i1 = _range_end(i1, s - 1 + 1, 1)
    i = 0
    for i in range(i, n - 1 + 1):
        Y[i] = 0.0
        i1 = 0
        for i1 in range(i1, s - 1 + 1):
            Y[i] += Yn[i1][i]
        else:
            i1 = _range_end(i1, s - 1 + 1, 1)
    else:
        i = _range_end(i, n - 1 + 1, 1)

def singularPCA(X, n, l, s, Y):
    if l > 10:
        l = 10
    if s > 20:
        s = 20
    if s > l:
        s = l
    if n > 300:
        n = 300
    A = Arr.of([0.0], fill=0.0, dyn=False, size=10, dims=(10,))
    B = Arr.of([0.0], fill=0.0, dyn=False, size=300, dims=(10,))
    Bn = Arr.of([0.0], fill=0.0, dyn=False, size=10, dims=(300,))
    kb = 0
    lb = 0
    m = 0
    k = 0
    i = 0
    j = 0
    i1 = 0
    V = Arr.of([0.0], fill=0.0, dyn=False, size=10, dims=(300,))
    Yn = Arr.of([0.0], fill=0.0, dyn=False, size=10, dims=(300,))
    ls = Arr.of([0.0], fill=0.0, dyn=False, size=10)
    Vtemp = Arr.of([0.0], fill=0.0, dyn=False, size=10)
    j = 0
    k = n - l + 1
    i = 0
    for i in range(i, l - 1 + 1):
        j = 0
        for j in range(j, l - 1 + 1):
            A[i][j] = 0.0
            m = 0
            for m in range(m, k - 1 + 1):
                A[i][j] += X[i + m] * X[m + j]
                B[m][j] = X[m + j]
            else:
                m = _range_end(m, k - 1 + 1, 1)
        else:
            j = _range_end(j, l - 1 + 1, 1)
    else:
        i = _range_end(i, l - 1 + 1, 1)
    ls[s] = gaussbisectionl(A, l - s, l)
    svector(A, ls[s], l, Vtemp)
    j = 0
    for j in range(j, l - 1 + 1):
        V[s][j] = Vtemp[j]
    else:
        j = _range_end(j, l - 1 + 1, 1)
    i1 = s
    i = 0
    for i in range(i, k - 1 + 1):
        Yn[i1][i] = 0.0
        j = 0
        for j in range(j, l - 1 + 1):
            Yn[i1][i] += B[i][j] * V[i1][j]
        else:
            j = _range_end(j, l - 1 + 1, 1)
    else:
        i = _range_end(i, k - 1 + 1, 1)
    i = 0
    for i in range(i, l - 1 + 1):
        j = 0
        for j in range(j, k - 1 + 1):
            Bn[i][j] = V[i1][i] * Yn[i1][j]
        else:
            j = _range_end(j, k - 1 + 1, 1)
    else:
        i = _range_end(i, l - 1 + 1, 1)
    kb = k
    lb = l
    i = 0
    for i in range(i, n - 1 + 1):
        Yn[i1][i] = 0.0
        if i < (lb - 1):
            j = 0
            for j in range(j, i + 1):
                if l <= k:
                    Yn[i1][i] += Bn[j][i - j]
                if l > k:
                    Yn[i1][i] += Bn[i - j][j]
            else:
                j = _range_end(j, i + 1, 1)
            Yn[i1][i] = _fdiv(Yn[i1][i], 1.0 * (i + 1))
        if (lb - 1) <= i and i < (kb - 1):
            j = 0
            for j in range(j, lb - 1 + 1):
                if l <= k:
                    Yn[i1][i] += Bn[j][i - j]
                if l > k:
                    Yn[i1][i] += Bn[i - j][j]
            else:
                j = _range_end(j, lb - 1 + 1, 1)
            Yn[i1][i] = _fdiv(Yn[i1][i], 1.0 * lb)
        if (kb - 1) <= i:
            j = i - kb + 1
            for j in range(j, n - kb + 1):
                if l <= k:
                    Yn[i1][i] += Bn[j][i - j]
                if l > k:
                    Yn[i1][i] += Bn[i - j][j]
            else:
                j = _range_end(j, n - kb + 1, 1)
            Yn[i1][i] = _fdiv(Yn[i1][i], 1.0 * (n - i))
    else:
        i = _range_end(i, n - 1 + 1, 1)
    i = 0
    for i in range(i, n - 1 + 1):
        Y[i] = 0.0
        Y[i] = Yn[s][i]
    else:
        i = _range_end(i, n - 1 + 1, 1)

__all__ = ['Equal', 'gaussSn', 'gaussbisectionl', 'svector', 'fastsingular', 'singularPCA']
