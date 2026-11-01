"""dt_fft.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *


def fastfouriertransform(a, nn, inversefft):
    ii = 0
    jj = 0
    n = 0
    mmax = 0
    m = 0
    j = 0
    istep = 0
    i = 0
    isign = 0
    wtemp = 0.0
    wr = 0.0
    wpr = 0.0
    wpi = 0.0
    wi = 0.0
    theta = 0.0
    tempr = 0.0
    tempi = 0.0
    if inversefft:
        isign = -1
    else:
        isign = 1
    n = 2 * nn
    j = 1
    ii = 1
    for ii in range(ii, nn + 1):
        i = (2 * ii) - 1
        if j > i:
            tempr = a[j - 1]
            tempi = a[j]
            a[j - 1] = a[i - 1]
            a[j] = a[i]
            a[i - 1] = tempr
            a[i] = tempi
        m = _idiv(n, 2)
        while m >= 2 and j > m:
            j -= m
            m = _idiv(m, 2)
        j += m
    else:
        ii = _range_end(ii, nn + 1, 1)
    mmax = 2
    while n > mmax:
        istep = 2 * mmax
        theta = _fdiv(2.0 * 3.141592653589793, isign * mmax)
        wpr = -2.0 * MathPow(MathSin(0.5 * theta), 2)
        wpi = MathSin(theta)
        wr = 1.0
        wi = 0.0
        ii = 1
        for ii in range(ii, _idiv(mmax, 2) + 1):
            m = (2 * ii) - 1
            jj = 0
            for jj in range(jj, _idiv(n - m, istep) + 1):
                i = m + (jj * istep)
                j = i + mmax
                tempr = (wr * a[j - 1]) - (wi * a[j])
                tempi = (wr * a[j]) + (wi * a[j - 1])
                a[j - 1] -= tempr
                a[j] -= tempi
                a[i - 1] += tempr
                a[i] += tempi
            else:
                jj = _range_end(jj, _idiv(n - m, istep) + 1, 1)
            wtemp = wr
            wr = (wr * wpr) - (wi * wpi) + wr
            wi = (wi * wpr) + (wtemp * wpi) + wi
        else:
            ii = _range_end(ii, _idiv(mmax, 2) + 1, 1)
        mmax = istep
    if inversefft:
        i = 1
        for i in range(i, 2 * nn + 1):
            a[i - 1] = _fdiv(a[i - 1], nn)
        else:
            i = _range_end(i, 2 * nn + 1, 1)
    return

def realfastfouriertransform(a, tnn, inversefft):
    twr = 0.0
    twi = 0.0
    twpr = 0.0
    twpi = 0.0
    twtemp = 0.0
    ttheta = 0.0
    i = 0
    i1 = 0
    i2 = 0
    i3 = 0
    i4 = 0
    c1 = 0.0
    c2 = 0.0
    h1r = 0.0
    h1i = 0.0
    h2r = 0.0
    h2i = 0.0
    wrs = 0.0
    wis = 0.0
    nn = 0
    ii = 0
    jj = 0
    n = 0
    mmax = 0
    m = 0
    j = 0
    istep = 0
    isign = 0
    wtemp = 0.0
    wr = 0.0
    wpr = 0.0
    wpi = 0.0
    wi = 0.0
    theta = 0.0
    tempr = 0.0
    tempi = 0.0
    if tnn == 1:
        return
    if not inversefft:
        ttheta = _fdiv(2.0 * 3.141592653589793, tnn)
        c1 = 0.5
        c2 = -0.5
    else:
        ttheta = _fdiv(2.0 * 3.141592653589793, tnn)
        c1 = 0.5
        c2 = 0.5
        ttheta = -ttheta
        twpr = -2.0 * MathPow(MathSin(0.5 * ttheta), 2)
        twpi = MathSin(ttheta)
        twr = 1.0 + twpr
        twi = twpi
        i = 2
        for i in range(i, _idiv(tnn, 4) + 1 + 1):
            i1 = i + i - 2
            i2 = i1 + 1
            i3 = tnn + 1 - i2
            i4 = i3 + 1
            wrs = twr
            wis = twi
            h1r = c1 * (a[i1] + a[i3])
            h1i = c1 * (a[i2] - a[i4])
            h2r = (-c2) * (a[i2] + a[i4])
            h2i = c2 * (a[i1] - a[i3])
            a[i1] = h1r + (wrs * h2r) - (wis * h2i)
            a[i2] = h1i + (wrs * h2i) + (wis * h2r)
            a[i3] = h1r - (wrs * h2r) + (wis * h2i)
            a[i4] = (-h1i) + (wrs * h2i) + (wis * h2r)
            twtemp = twr
            twr = (twr * twpr) - (twi * twpi) + twr
            twi = (twi * twpr) + (twtemp * twpi) + twi
        else:
            i = _range_end(i, _idiv(tnn, 4) + 1 + 1, 1)
        h1r = a[0]
        a[0] = c1 * (h1r + a[1])
        a[1] = c1 * (h1r - a[1])
    if inversefft:
        isign = -1
    else:
        isign = 1
    n = tnn
    nn = _idiv(tnn, 2)
    j = 1
    ii = 1
    for ii in range(ii, nn + 1):
        i = (2 * ii) - 1
        if j > i:
            tempr = a[j - 1]
            tempi = a[j]
            a[j - 1] = a[i - 1]
            a[j] = a[i]
            a[i - 1] = tempr
            a[i] = tempi
        m = _idiv(n, 2)
        while m >= 2 and j > m:
            j -= m
            m = _idiv(m, 2)
        j += m
    else:
        ii = _range_end(ii, nn + 1, 1)
    mmax = 2
    while n > mmax:
        istep = 2 * mmax
        theta = _fdiv(2.0 * 3.141592653589793, isign * mmax)
        wpr = -2.0 * MathPow(MathSin(0.5 * theta), 2)
        wpi = MathSin(theta)
        wr = 1.0
        wi = 0.0
        ii = 1
        for ii in range(ii, _idiv(mmax, 2) + 1):
            m = (2 * ii) - 1
            jj = 0
            for jj in range(jj, _idiv(n - m, istep) + 1):
                i = m + (jj * istep)
                j = i + mmax
                tempr = (wr * a[j - 1]) - (wi * a[j])
                tempi = (wr * a[j]) + (wi * a[j - 1])
                a[j - 1] = a[i - 1] - tempr
                a[j] = a[i] - tempi
                a[i - 1] += tempr
                a[i] += tempi
            else:
                jj = _range_end(jj, _idiv(n - m, istep) + 1, 1)
            wtemp = wr
            wr = (wr * wpr) - (wi * wpi) + wr
            wi = (wi * wpr) + (wtemp * wpi) + wi
        else:
            ii = _range_end(ii, _idiv(mmax, 2) + 1, 1)
        mmax = istep
    if inversefft:
        i = 1
        for i in range(i, 2 * nn + 1):
            a[i - 1] = _fdiv(a[i - 1], nn)
        else:
            i = _range_end(i, 2 * nn + 1, 1)
    if not inversefft:
        twpr = -2.0 * MathPow(MathSin(0.5 * ttheta), 2)
        twpi = MathSin(ttheta)
        twr = 1.0 + twpr
        twi = twpi
        i = 2
        for i in range(i, _idiv(tnn, 4) + 1 + 1):
            i1 = i + i - 2
            i2 = i1 + 1
            i3 = tnn + 1 - i2
            i4 = i3 + 1
            wrs = twr
            wis = twi
            h1r = c1 * (a[i1] + a[i3])
            h1i = c1 * (a[i2] - a[i4])
            h2r = (-c2) * (a[i2] + a[i4])
            h2i = c2 * (a[i1] - a[i3])
            a[i1] = h1r + (wrs * h2r) - (wis * h2i)
            a[i2] = h1i + (wrs * h2i) + (wis * h2r)
            a[i3] = h1r - (wrs * h2r) + (wis * h2i)
            a[i4] = (-h1i) + (wrs * h2i) + (wis * h2r)
            twtemp = twr
            twr = (twr * twpr) - (twi * twpi) + twr
            twi = (twi * twpr) + (twtemp * twpi) + twi
        else:
            i = _range_end(i, _idiv(tnn, 4) + 1 + 1, 1)
        h1r = a[0]
        a[0] = h1r + a[1]
        a[1] = h1r - a[1]
    return

def fastcorellation(signal, signallen, pattern, patternlen):
    a1 = Arr(0, 0.0)
    a2 = Arr(0, 0.0)
    nl = 0
    i = 0
    t1 = 0.0
    t2 = 0.0
    nl = signallen + patternlen
    i = 1
    while i < nl:
        i = i * 2
    nl = i
    ArrayResize(a1, nl)
    ArrayResize(a2, nl)
    i = 0
    for i in range(i, signallen - 1 + 1):
        a1[i] = signal[i]
    else:
        i = _range_end(i, signallen - 1 + 1, 1)
    i = signallen
    for i in range(i, nl - 1 + 1):
        a1[i] = 0.0
    else:
        i = _range_end(i, nl - 1 + 1, 1)
    i = 0
    for i in range(i, patternlen - 1 + 1):
        a2[i] = pattern[i]
    else:
        i = _range_end(i, patternlen - 1 + 1, 1)
    i = patternlen
    for i in range(i, nl - 1 + 1):
        a2[i] = 0.0
    else:
        i = _range_end(i, nl - 1 + 1, 1)
    realfastfouriertransform(a1, nl, False)
    realfastfouriertransform(a2, nl, False)
    a1[0] *= a2[0]
    a1[1] *= a2[1]
    i = 1
    for i in range(i, _idiv(nl, 2) - 1 + 1):
        t1 = a1[2 * i]
        t2 = a1[(2 * i) + 1]
        a1[2 * i] = (t1 * a2[2 * i]) + (t2 * a2[(2 * i) + 1])
        a1[(2 * i) + 1] = (t2 * a2[2 * i]) - (t1 * a2[(2 * i) + 1])
    else:
        i = _range_end(i, _idiv(nl, 2) - 1 + 1, 1)
    realfastfouriertransform(a1, nl, True)
    i = 0
    for i in range(i, signallen - 1 + 1):
        signal[i] = a1[i]
    else:
        i = _range_end(i, signallen - 1 + 1, 1)
    return

def fastconvolution(signal, signallen, response, negativelen, positivelen):
    a1 = Arr(0, 0.0)
    a2 = Arr(0, 0.0)
    nl = 0
    i = 0
    t1 = 0.0
    t2 = 0.0
    nl = signallen
    if negativelen > positivelen:
        nl += negativelen
    else:
        nl += positivelen
    if (negativelen + 1 + positivelen) > nl:
        nl = negativelen + 1 + positivelen
    i = 1
    while i < nl:
        i = i * 2
    nl = i
    ArrayResize(a1, nl)
    ArrayResize(a2, nl)
    i = 0
    for i in range(i, signallen - 1 + 1):
        a1[i] = signal[i]
    else:
        i = _range_end(i, signallen - 1 + 1, 1)
    i = signallen
    for i in range(i, nl - 1 + 1):
        a1[i] = 0.0
    else:
        i = _range_end(i, nl - 1 + 1, 1)
    i = 0
    for i in range(i, nl - 1 + 1):
        a2[i] = 0.0
    else:
        i = _range_end(i, nl - 1 + 1, 1)
    i = 1
    for i in range(i, negativelen + 1):
        a2[nl - i] = response[negativelen - i]
    else:
        i = _range_end(i, negativelen + 1, 1)
    realfastfouriertransform(a1, nl, False)
    realfastfouriertransform(a2, nl, False)
    a1[0] *= a2[0]
    a1[1] *= a2[1]
    i = 1
    for i in range(i, _idiv(nl, 2) - 1 + 1):
        t1 = a1[2 * i]
        t2 = a1[(2 * i) + 1]
        a1[2 * i] = (t1 * a2[2 * i]) - (t2 * a2[(2 * i) + 1])
        a1[(2 * i) + 1] = (t2 * a2[2 * i]) + (t1 * a2[(2 * i) + 1])
    else:
        i = _range_end(i, _idiv(nl, 2) - 1 + 1, 1)
    realfastfouriertransform(a1, nl, True)
    i = 0
    for i in range(i, signallen - 1 + 1):
        signal[i] = a1[i]
    else:
        i = _range_end(i, signallen - 1 + 1, 1)
    return

def fastsinetransform(a, tnn, inversefst):
    jj = 0
    j = 0
    tm = 0
    n2 = 0
    sum_ = 0.0
    y1 = 0.0
    y2 = 0.0
    theta = 0.0
    wi = 0.0
    wr = 0.0
    wpi = 0.0
    wpr = 0.0
    wtemp = 0.0
    twr = 0.0
    twi = 0.0
    twpr = 0.0
    twpi = 0.0
    twtemp = 0.0
    ttheta = 0.0
    i = 0
    i1 = 0
    i2 = 0
    i3 = 0
    i4 = 0
    c1 = 0.0
    c2 = 0.0
    h1r = 0.0
    h1i = 0.0
    h2r = 0.0
    h2i = 0.0
    wrs = 0.0
    wis = 0.0
    nn = 0
    ii = 0
    n = 0
    mmax = 0
    m = 0
    istep = 0
    isign = 0
    tempr = 0.0
    tempi = 0.0
    if tnn == 1:
        a[0] = 0.0
        return
    theta = _fdiv(3.141592653589793, tnn)
    wr = 1.0
    wi = 0.0
    wpr = -2.0 * MathPow(MathSin(0.5 * theta), 2)
    wpi = MathSin(theta)
    a[0] = 0.0
    tm = _idiv(tnn, 2)
    n2 = tnn + 2
    j = 2
    for j in range(j, tm + 1 + 1):
        wtemp = wr
        wr = (wr * wpr) - (wi * wpi) + wr
        wi = (wi * wpr) + (wtemp * wpi) + wi
        y1 = wi * (a[j - 1] + a[n2 - j - 1])
        y2 = 0.5 * (a[j - 1] - a[n2 - j - 1])
        a[j - 1] = y1 + y2
        a[n2 - j - 1] = y1 - y2
    else:
        j = _range_end(j, tm + 1 + 1, 1)
    ttheta = _fdiv(2.0 * 3.141592653589793, tnn)
    c1 = 0.5
    c2 = -0.5
    isign = 1
    n = tnn
    nn = _idiv(tnn, 2)
    j = 1
    ii = 1
    for ii in range(ii, nn + 1):
        i = (2 * ii) - 1
        if j > i:
            tempr = a[j - 1]
            tempi = a[j]
            a[j - 1] = a[i - 1]
            a[j] = a[i]
            a[i - 1] = tempr
            a[i] = tempi
        m = _idiv(n, 2)
        while m >= 2 and j > m:
            j = j - m
            m = _idiv(m, 2)
        j = j + m
    else:
        ii = _range_end(ii, nn + 1, 1)
    mmax = 2
    while n > mmax:
        istep = 2 * mmax
        theta = _fdiv(2.0 * 3.141592653589793, isign * mmax)
        wpr = -2.0 * MathPow(MathSin(0.5 * theta), 2)
        wpi = MathSin(theta)
        wr = 1.0
        wi = 0.0
        ii = 1
        for ii in range(ii, _idiv(mmax, 2) + 1):
            m = (2 * ii) - 1
            jj = 0
            for jj in range(jj, _idiv(n - m, istep) + 1):
                i = m + (jj * istep)
                j = i + mmax
                tempr = (wr * a[j - 1]) - (wi * a[j])
                tempi = (wr * a[j]) + (wi * a[j - 1])
                a[j - 1] = a[i - 1] - tempr
                a[j] = a[i] - tempi
                a[i - 1] += tempr
                a[i] += tempi
            else:
                jj = _range_end(jj, _idiv(n - m, istep) + 1, 1)
            wtemp = wr
            wr = (wr * wpr) - (wi * wpi) + wr
            wi = (wi * wpr) + (wtemp * wpi) + wi
        else:
            ii = _range_end(ii, _idiv(mmax, 2) + 1, 1)
        mmax = istep
    twpr = -2.0 * MathPow(MathSin(0.5 * ttheta), 2)
    twpi = MathSin(ttheta)
    twr = 1.0 + twpr
    twi = twpi
    i = 2
    for i in range(i, _idiv(tnn, 4) + 1 + 1):
        i1 = i + i - 2
        i2 = i1 + 1
        i3 = tnn + 1 - i2
        i4 = i3 + 1
        wrs = twr
        wis = twi
        h1r = c1 * (a[i1] + a[i3])
        h1i = c1 * (a[i2] - a[i4])
        h2r = (-c2) * (a[i2] + a[i4])
        h2i = c2 * (a[i1] - a[i3])
        a[i1] = h1r + (wrs * h2r) - (wis * h2i)
        a[i2] = h1i + (wrs * h2i) + (wis * h2r)
        a[i3] = h1r - (wrs * h2r) + (wis * h2i)
        a[i4] = (-h1i) + (wrs * h2i) + (wis * h2r)
        twtemp = twr
        twr = (twr * twpr) - (twi * twpi) + twr
        twi = (twi * twpr) + (twtemp * twpi) + twi
    else:
        i = _range_end(i, _idiv(tnn, 4) + 1 + 1, 1)
    h1r = a[0]
    a[0] = h1r + a[1]
    a[1] = h1r - a[1]
    sum_ = 0.0
    a[0] *= 0.5
    a[1] = 0.0
    jj = 0
    for jj in range(jj, tm - 1 + 1):
        j = (2 * jj) + 1
        sum_ += a[j - 1]
        a[j - 1] = a[j]
        a[j] = sum_
    else:
        jj = _range_end(jj, tm - 1 + 1, 1)
    if inversefst:
        j = 1
        for j in range(j, tnn + 1):
            a[j - 1] *= _idiv(2, tnn)
        else:
            j = _range_end(j, tnn + 1, 1)
    return

def fastcosinetransform(a, tnn, inversefct):
    j = 0
    n2 = 0
    sum_ = 0.0
    y1 = 0.0
    y2 = 0.0
    theta = 0.0
    wi = 0.0
    wpi = 0.0
    wr = 0.0
    wpr = 0.0
    wtemp = 0.0
    twr = 0.0
    twi = 0.0
    twpr = 0.0
    twpi = 0.0
    twtemp = 0.0
    ttheta = 0.0
    i = 0
    i1 = 0
    i2 = 0
    i3 = 0
    i4 = 0
    c1 = 0.0
    c2 = 0.0
    h1r = 0.0
    h1i = 0.0
    h2r = 0.0
    h2i = 0.0
    wrs = 0.0
    wis = 0.0
    nn = 0
    ii = 0
    jj = 0
    n = 0
    mmax = 0
    m = 0
    istep = 0
    isign = 0
    tempr = 0.0
    tempi = 0.0
    if tnn == 1:
        y1 = a[0]
        y2 = a[1]
        a[0] = 0.5 * (y1 + y2)
        a[1] = 0.5 * (y1 - y2)
        if inversefct:
            a[0] *= 2
            a[1] *= 2
        return
    wi = 0.0
    wr = 1.0
    theta = _fdiv(3.141592653589793, tnn)
    wtemp = MathSin(theta * 0.5)
    wpr = -2.0 * wtemp * wtemp
    wpi = MathSin(theta)
    sum_ = 0.5 * (a[0] - a[tnn])
    a[0] = 0.5 * (a[0] + a[tnn])
    n2 = tnn + 2
    j = 2
    for j in range(j, _idiv(tnn, 2) + 1):
        wtemp = wr
        wr = (wtemp * wpr) - (wi * wpi) + wtemp
        wi = (wi * wpr) + (wtemp * wpi) + wi
        y1 = 0.5 * (a[j - 1] + a[n2 - j - 1])
        y2 = a[j - 1] - a[n2 - j - 1]
        a[j - 1] = y1 - (wi * y2)
        a[n2 - j - 1] = y1 + (wi * y2)
        sum_ = sum_ + (wr * y2)
    else:
        j = _range_end(j, _idiv(tnn, 2) + 1, 1)
    ttheta = _fdiv(2.0 * 3.141592653589793, tnn)
    c1 = 0.5
    c2 = -0.5
    isign = 1
    n = tnn
    nn = _idiv(tnn, 2)
    j = 1
    ii = 1
    for ii in range(ii, nn + 1):
        i = (2 * ii) - 1
        if j > i:
            tempr = a[j - 1]
            tempi = a[j]
            a[j - 1] = a[i - 1]
            a[j] = a[i]
            a[i - 1] = tempr
            a[i] = tempi
        m = _idiv(n, 2)
        while m >= 2 and j > m:
            j = j - m
            m = _idiv(m, 2)
        j = j + m
    else:
        ii = _range_end(ii, nn + 1, 1)
    mmax = 2
    while n > mmax:
        istep = 2 * mmax
        theta = _fdiv(2.0 * 3.141592653589793, isign * mmax)
        wpr = -2.0 * MathPow(MathSin(0.5 * theta), 2)
        wpi = MathSin(theta)
        wr = 1.0
        wi = 0.0
        ii = 1
        for ii in range(ii, _idiv(mmax, 2) + 1):
            m = (2 * ii) - 1
            jj = 0
            for jj in range(jj, _idiv(n - m, istep) + 1):
                i = m + (jj * istep)
                j = i + mmax
                tempr = (wr * a[j - 1]) - (wi * a[j])
                tempi = (wr * a[j]) + (wi * a[j - 1])
                a[j - 1] = a[i - 1] - tempr
                a[j] = a[i] - tempi
                a[i - 1] += tempr
                a[i] += tempi
            else:
                jj = _range_end(jj, _idiv(n - m, istep) + 1, 1)
            wtemp = wr
            wr = (wr * wpr) - (wi * wpi) + wr
            wi = (wi * wpr) + (wtemp * wpi) + wi
        else:
            ii = _range_end(ii, _idiv(mmax, 2) + 1, 1)
        mmax = istep
    twpr = -2.0 * MathPow(MathSin(0.5 * ttheta), 2)
    twpi = MathSin(ttheta)
    twr = 1.0 + twpr
    twi = twpi
    i = 2
    for i in range(i, _idiv(tnn, 4) + 1 + 1):
        i1 = i + i - 2
        i2 = i1 + 1
        i3 = tnn + 1 - i2
        i4 = i3 + 1
        wrs = twr
        wis = twi
        h1r = c1 * (a[i1] + a[i3])
        h1i = c1 * (a[i2] - a[i4])
        h2r = (-c2) * (a[i2] + a[i4])
        h2i = c2 * (a[i1] - a[i3])
        a[i1] = h1r + (wrs * h2r) - (wis * h2i)
        a[i2] = h1i + (wrs * h2i) + (wis * h2r)
        a[i3] = h1r - (wrs * h2r) + (wis * h2i)
        a[i4] = (-h1i) + (wrs * h2i) + (wis * h2r)
        twtemp = twr
        twr = (twr * twpr) - (twi * twpi) + twr
        twi = (twi * twpr) + (twtemp * twpi) + twi
    else:
        i = _range_end(i, _idiv(tnn, 4) + 1 + 1, 1)
    h1r = a[0]
    a[0] = h1r + a[1]
    a[1] = h1r - a[1]
    a[tnn] = a[1]
    a[1] = sum_
    j = 4
    while j <= tnn:
        sum_ = sum_ + a[j - 1]
        a[j - 1] = sum_
        j = j + 2
    if inversefct:
        j = 0
        for j in range(j, tnn + 1):
            a[j] = _fdiv(a[j] * 2, tnn)
        else:
            j = _range_end(j, tnn + 1, 1)
    return

def tworealffts(a1, a2, a, b, tn):
    jj = 0
    j = 0
    rep = 0.0
    rem = 0.0
    aip = 0.0
    aim = 0.0
    ii = 0
    n = 0
    nn = 0
    mmax = 0
    m = 0
    istep = 0
    i = 0
    isign = 0
    wtemp = 0.0
    wr = 0.0
    wpr = 0.0
    wpi = 0.0
    wi = 0.0
    theta = 0.0
    tempr = 0.0
    tempi = 0.0
    nn = tn
    ArrayResize(a, 2 * tn)
    ArrayResize(b, 2 * tn)
    j = 1
    for j in range(j, tn + 1):
        jj = j + j
        a[jj - 2] = a1[j - 1]
        a[jj - 1] = a2[j - 1]
    else:
        j = _range_end(j, tn + 1, 1)
    isign = 1
    n = 2 * nn
    j = 1
    ii = 1
    for ii in range(ii, nn + 1):
        i = (2 * ii) - 1
        if j > i:
            tempr = a[j - 1]
            tempi = a[j]
            a[j - 1] = a[i - 1]
            a[j] = a[i]
            a[i - 1] = tempr
            a[i] = tempi
        m = _idiv(n, 2)
        while m >= 2 and j > m:
            j = j - m
            m = _idiv(m, 2)
        j = j + m
    else:
        ii = _range_end(ii, nn + 1, 1)
    mmax = 2
    while n > mmax:
        istep = 2 * mmax
        theta = _fdiv(2.0 * 3.141592653589793, isign * mmax)
        wpr = -2.0 * MathPow(MathSin(0.5 * theta), 2)
        wpi = MathSin(theta)
        wr = 1.0
        wi = 0.0
        ii = 1
        for ii in range(ii, _idiv(mmax, 2) + 1):
            m = (2 * ii) - 1
            jj = 0
            for jj in range(jj, _idiv(n - m, istep) + 1):
                i = m + (jj * istep)
                j = i + mmax
                tempr = (wr * a[j - 1]) - (wi * a[j])
                tempi = (wr * a[j]) + (wi * a[j - 1])
                a[j - 1] = a[i - 1] - tempr
                a[j] = a[i] - tempi
                a[i - 1] += tempr
                a[i] += tempi
            else:
                jj = _range_end(jj, _idiv(n - m, istep) + 1, 1)
            wtemp = wr
            wr = (wr * wpr) - (wi * wpi) + wr
            wi = (wi * wpr) + (wtemp * wpi) + wi
        else:
            ii = _range_end(ii, _idiv(mmax, 2) + 1, 1)
        mmax = istep
    b[0] = a[1]
    a[1] = 0.0
    b[1] = 0.0
    jj = 1
    for jj in range(jj, _idiv(tn, 2) + 1):
        j = (2 * jj) + 1
        rep = 0.5 * (a[j - 1] + a[(2 * tn) + 1 - j])
        rem = 0.5 * (a[j - 1] - a[(2 * tn) + 1 - j])
        aip = 0.5 * (a[j] + a[(2 * tn) + 2 - j])
        aim = 0.5 * (a[j] - a[(2 * tn) + 2 - j])
        a[j - 1] = rep
        a[j] = aim
        a[(2 * tn) + 1 - j] = rep
        a[(2 * tn) + 2 - j] = -aim
        b[j - 1] = aip
        b[j] = -rem
        b[(2 * tn) + 1 - j] = aip
        b[(2 * tn) + 2 - j] = rem
    else:
        jj = _range_end(jj, _idiv(tn, 2) + 1, 1)
    return

__all__ = ['fastfouriertransform', 'realfastfouriertransform', 'fastcorellation', 'fastconvolution', 'fastsinetransform', 'fastcosinetransform', 'tworealffts']
