"""``dt_FFT.mqh`` (klot, 2006 — ALGLIB's FFT routines for MQL) — line-by-line port.

All routines work **in place** on a list (or float numpy array) exactly like
the originals, with the same packed layouts:

- ``fastfouriertransform(a, nn, inverse)``: complex FFT of ``nn`` points stored
  as ``[re0, im0, re1, im1, …]``; ``nn`` must be a power of two.
- ``realfastfouriertransform(a, tnn, inverse)``: real FFT of ``tnn`` points;
  output ``[F0, F(n/2), re1, im1, re2, im2, …]``.
- ``fastsinetransform`` / ``fastcosinetransform``: the discrete sine/cosine
  transforms (``fastcosinetransform`` takes ``tnn+1`` values). This is the one
  the i-SpectrAnalysis family uses.
- ``fastcorellation`` / ``fastconvolution`` / ``tworealffts``.

Quirks kept for fidelity:

- ``fastfouriertransform`` (the complex one) has a transcription bug in the
  MQL source: its butterfly does ``a[j-1]-=tempr`` where ALGLIB has
  ``a[j-1]=a[i-1]-tempr``, so it does **not** compute a correct FFT (and its
  inverse does not round-trip). The port reproduces the MQL5 output. Use
  :func:`numpy.fft.fft` if you need a real FFT. No Codebase indicator calls
  it; the routines they do call (the real FFT and the sine/cosine transforms)
  are correct and verified against direct sums.
- the inverse sine transform scales by ``2/tnn`` in
**integer** arithmetic in the source (``a[j-1]*=2/tnn``), which is 0 for any
``tnn > 2`` — so ``fastsinetransform(a, n, True)`` zeroes the array in MQL5,
and does here too. The cosine transform's inverse (``a[j]*2/tnn``) is
evaluated left to right in floating point and is correct.
"""

from __future__ import annotations

import math

from .mql_runtime import idiv

pi = 3.14159265358979323846


def _sin2(x: float) -> float:
    s = math.sin(x)
    return s * s


def _bit_reverse(a, nn: int, n: int) -> None:
    j = 1
    for ii in range(1, nn + 1):
        i = 2 * ii - 1
        if j > i:
            tempr = a[j - 1]
            tempi = a[j]
            a[j - 1] = a[i - 1]
            a[j] = a[i]
            a[i - 1] = tempr
            a[i] = tempi
        m = idiv(n, 2)
        while m >= 2 and j > m:
            j -= m
            m = idiv(m, 2)
        j += m


def _danielson_lanczos(a, n: int, isign: int, subtract_from_i: bool) -> None:
    """The butterfly passes. ``fastfouriertransform`` updates ``a[j]`` with
    ``-=``; the other routines assign ``a[j] = a[i] - temp`` — identical
    results, kept separate to mirror each source routine."""
    mmax = 2
    while n > mmax:
        istep = 2 * mmax
        theta = 2.0 * pi / (isign * mmax)
        wpr = -2.0 * _sin2(0.5 * theta)
        wpi = math.sin(theta)
        wr = 1.0
        wi = 0.0
        for ii in range(1, idiv(mmax, 2) + 1):
            m = 2 * ii - 1
            for jj in range(0, idiv(n - m, istep) + 1):
                i = m + jj * istep
                j = i + mmax
                tempr = wr * a[j - 1] - wi * a[j]
                tempi = wr * a[j] + wi * a[j - 1]
                if subtract_from_i:
                    a[j - 1] = a[i - 1] - tempr
                    a[j] = a[i] - tempi
                else:
                    a[j - 1] -= tempr
                    a[j] -= tempi
                a[i - 1] += tempr
                a[i] += tempi
            wtemp = wr
            wr = wr * wpr - wi * wpi + wr
            wi = wi * wpr + wtemp * wpi + wi
        mmax = istep


def _real_twiddle(a, tnn: int, ttheta: float, c1: float, c2: float) -> None:
    twpr = -2.0 * _sin2(0.5 * ttheta)
    twpi = math.sin(ttheta)
    twr = 1.0 + twpr
    twi = twpi
    for i in range(2, idiv(tnn, 4) + 2):
        i1 = i + i - 2
        i2 = i1 + 1
        i3 = tnn + 1 - i2
        i4 = i3 + 1
        wrs = twr
        wis = twi
        h1r = c1 * (a[i1] + a[i3])
        h1i = c1 * (a[i2] - a[i4])
        h2r = -c2 * (a[i2] + a[i4])
        h2i = c2 * (a[i1] - a[i3])
        a[i1] = h1r + wrs * h2r - wis * h2i
        a[i2] = h1i + wrs * h2i + wis * h2r
        a[i3] = h1r - wrs * h2r + wis * h2i
        a[i4] = -h1i + wrs * h2i + wis * h2r
        twtemp = twr
        twr = twr * twpr - twi * twpi + twr
        twi = twi * twpr + twtemp * twpi + twi


def fastfouriertransform(a, nn: int, inversefft: bool) -> None:
    isign = -1 if inversefft else 1
    n = 2 * nn
    _bit_reverse(a, nn, n)
    _danielson_lanczos(a, n, isign, subtract_from_i=False)
    if inversefft:
        for i in range(1, 2 * nn + 1):
            a[i - 1] /= nn


def realfastfouriertransform(a, tnn: int, inversefft: bool) -> None:
    if tnn == 1:
        return
    ttheta = 2.0 * pi / tnn
    if not inversefft:
        c1 = 0.5
        c2 = -0.5
    else:
        c1 = 0.5
        c2 = 0.5
        ttheta = -ttheta
        _real_twiddle(a, tnn, ttheta, c1, c2)
        h1r = a[0]
        a[0] = c1 * (h1r + a[1])
        a[1] = c1 * (h1r - a[1])
    isign = -1 if inversefft else 1
    n = tnn
    nn = idiv(tnn, 2)
    _bit_reverse(a, nn, n)
    _danielson_lanczos(a, n, isign, subtract_from_i=True)
    if inversefft:
        for i in range(1, 2 * nn + 1):
            a[i - 1] /= nn
    if not inversefft:
        _real_twiddle(a, tnn, ttheta, c1, c2)
        h1r = a[0]
        a[0] = h1r + a[1]
        a[1] = h1r - a[1]


def _next_pow2(n: int) -> int:
    i = 1
    while i < n:
        i *= 2
    return i


def fastcorellation(signal, signallen: int, pattern, patternlen: int) -> None:
    """Cross-correlation of ``signal`` with ``pattern``; result in ``signal``."""
    nl = _next_pow2(signallen + patternlen)
    a1 = [0.0] * nl
    a2 = [0.0] * nl
    for i in range(signallen):
        a1[i] = signal[i]
    for i in range(patternlen):
        a2[i] = pattern[i]
    realfastfouriertransform(a1, nl, False)
    realfastfouriertransform(a2, nl, False)
    a1[0] *= a2[0]
    a1[1] *= a2[1]
    for i in range(1, idiv(nl, 2)):
        t1 = a1[2 * i]
        t2 = a1[2 * i + 1]
        a1[2 * i] = t1 * a2[2 * i] + t2 * a2[2 * i + 1]
        a1[2 * i + 1] = t2 * a2[2 * i] - t1 * a2[2 * i + 1]
    realfastfouriertransform(a1, nl, True)
    for i in range(signallen):
        signal[i] = a1[i]


def fastconvolution(signal, signallen: int, response, negativelen: int, positivelen: int) -> None:
    """Convolution with a response defined on ``[-negativelen, positivelen]``;
    result in ``signal``. (The source fills only the negative-lag part of the
    padded response, as ALGLIB's original does.)"""
    nl = signallen
    nl += negativelen if negativelen > positivelen else positivelen
    if negativelen + 1 + positivelen > nl:
        nl = negativelen + 1 + positivelen
    nl = _next_pow2(nl)
    a1 = [0.0] * nl
    a2 = [0.0] * nl
    for i in range(signallen):
        a1[i] = signal[i]
    for i in range(1, negativelen + 1):
        a2[nl - i] = response[negativelen - i]
    realfastfouriertransform(a1, nl, False)
    realfastfouriertransform(a2, nl, False)
    a1[0] *= a2[0]
    a1[1] *= a2[1]
    for i in range(1, idiv(nl, 2)):
        t1 = a1[2 * i]
        t2 = a1[2 * i + 1]
        a1[2 * i] = t1 * a2[2 * i] - t2 * a2[2 * i + 1]
        a1[2 * i + 1] = t2 * a2[2 * i] + t1 * a2[2 * i + 1]
    realfastfouriertransform(a1, nl, True)
    for i in range(signallen):
        signal[i] = a1[i]


def fastsinetransform(a, tnn: int, inversefst: bool) -> None:
    if tnn == 1:
        a[0] = 0
        return
    theta = pi / tnn
    wr = 1.0
    wi = 0.0
    wpr = -2.0 * _sin2(0.5 * theta)
    wpi = math.sin(theta)
    a[0] = 0.0
    tm = idiv(tnn, 2)
    n2 = tnn + 2
    for j in range(2, tm + 2):
        wtemp = wr
        wr = wr * wpr - wi * wpi + wr
        wi = wi * wpr + wtemp * wpi + wi
        y1 = wi * (a[j - 1] + a[n2 - j - 1])
        y2 = 0.5 * (a[j - 1] - a[n2 - j - 1])
        a[j - 1] = y1 + y2
        a[n2 - j - 1] = y1 - y2
    ttheta = 2.0 * pi / tnn
    c1 = 0.5
    c2 = -0.5
    n = tnn
    nn = idiv(tnn, 2)
    _bit_reverse(a, nn, n)
    _danielson_lanczos(a, n, 1, subtract_from_i=True)
    _real_twiddle(a, tnn, ttheta, c1, c2)
    h1r = a[0]
    a[0] = h1r + a[1]
    a[1] = h1r - a[1]
    total = 0.0
    a[0] *= 0.5
    a[1] = 0.0
    for jj in range(tm):
        j = 2 * jj + 1
        total += a[j - 1]
        a[j - 1] = a[j]
        a[j] = total
    if inversefst:
        scale = idiv(2, tnn)          # integer division in the source
        for j in range(1, tnn + 1):
            a[j - 1] *= scale


def fastcosinetransform(a, tnn: int, inversefct: bool) -> None:
    """Discrete cosine transform of the ``tnn+1`` values in ``a`` (in place)."""
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
    theta = pi / tnn
    wtemp = math.sin(theta * 0.5)
    wpr = -2.0 * wtemp * wtemp
    wpi = math.sin(theta)
    total = 0.5 * (a[0] - a[tnn])
    a[0] = 0.5 * (a[0] + a[tnn])
    n2 = tnn + 2
    for j in range(2, idiv(tnn, 2) + 1):
        wtemp = wr
        wr = wtemp * wpr - wi * wpi + wtemp
        wi = wi * wpr + wtemp * wpi + wi
        y1 = 0.5 * (a[j - 1] + a[n2 - j - 1])
        y2 = a[j - 1] - a[n2 - j - 1]
        a[j - 1] = y1 - wi * y2
        a[n2 - j - 1] = y1 + wi * y2
        total = total + wr * y2
    ttheta = 2.0 * pi / tnn
    c1 = 0.5
    c2 = -0.5
    n = tnn
    nn = idiv(tnn, 2)
    _bit_reverse(a, nn, n)
    _danielson_lanczos(a, n, 1, subtract_from_i=True)
    _real_twiddle(a, tnn, ttheta, c1, c2)
    h1r = a[0]
    a[0] = h1r + a[1]
    a[1] = h1r - a[1]
    a[tnn] = a[1]
    a[1] = total
    j = 4
    while j <= tnn:
        total = total + a[j - 1]
        a[j - 1] = total
        j += 2
    if inversefct:
        for j in range(tnn + 1):
            a[j] = a[j] * 2 / tnn


def tworealffts(a1, a2, a, b, tn: int) -> None:
    """FFTs of two real sequences at once; ``a``/``b`` (lists) are resized to
    ``2*tn`` and receive the two complex spectra."""
    nn = tn
    del a[:]
    a.extend([0.0] * (2 * tn))
    del b[:]
    b.extend([0.0] * (2 * tn))
    for j in range(1, tn + 1):
        jj = j + j
        a[jj - 2] = a1[j - 1]
        a[jj - 1] = a2[j - 1]
    n = 2 * nn
    _bit_reverse(a, nn, n)
    _danielson_lanczos(a, n, 1, subtract_from_i=True)
    b[0] = a[1]
    a[1] = 0.0
    b[1] = 0.0
    for jj in range(1, idiv(tn, 2) + 1):
        j = 2 * jj + 1
        rep = 0.5 * (a[j - 1] + a[2 * tn + 1 - j])
        rem = 0.5 * (a[j - 1] - a[2 * tn + 1 - j])
        aip = 0.5 * (a[j] + a[2 * tn + 2 - j])
        aim = 0.5 * (a[j] - a[2 * tn + 2 - j])
        a[j - 1] = rep
        a[j] = aim
        a[2 * tn + 1 - j] = rep
        a[2 * tn + 2 - j] = -aim
        b[j - 1] = aip
        b[j] = -rem
        b[2 * tn + 1 - j] = aip
        b[2 * tn + 2 - j] = rem
