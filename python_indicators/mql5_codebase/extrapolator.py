"""extrapolator — converted from MQL5: MQL5 Indicators/Extrapolator/extrapolator.mq5

Copyright: Copyright © 2008, gpwr; Link: vlad1004@yahoo.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2008, gpwr', 'link': 'vlad1004@yahoo.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [255], 2: [16711680]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: '', 2: ''}, 'levels': [], 'description': [], 'name': 'extrapolator', 'source': 'MQL5 Indicators/Extrapolator/extrapolator.mq5', 'folder': 'Extrapolator', 'inputs': [{'mql': 'Method', 'py': 'Method', 'param': 'Method', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'LastBar', 'py': 'LastBar', 'param': 'LastBar', 'type': 'int', 'default': 30, 'label': '', 'sinput': False}, {'mql': 'PastBars', 'py': 'PastBars', 'param': 'PastBars', 'type': 'int', 'default': 300, 'label': '', 'sinput': False}, {'mql': 'LPOrder', 'py': 'LPOrder', 'param': 'LPOrder', 'type': 'double', 'default': 0.6, 'label': '', 'sinput': False}, {'mql': 'FutBars', 'py': 'FutBars', 'param': 'FutBars', 'type': 'int', 'default': 100, 'label': '', 'sinput': False}, {'mql': 'HarmNo', 'py': 'HarmNo', 'param': 'HarmNo', 'type': 'int', 'default': 20, 'label': '', 'sinput': False}, {'mql': 'FreqTOL', 'py': 'FreqTOL', 'param': 'FreqTOL', 'type': 'double', 'default': 0.0001, 'label': '', 'sinput': False}, {'mql': 'BurgWin', 'py': 'BurgWin', 'param': 'BurgWin', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Method_
Extrapolation = 1
Autocorrelation = 2
Weight = 3
Burg = 4
Itakura = 5
covariance = 6
_enum('Method_', {1: 'Extrapolation', 2: 'Autocorrelation', 3: 'Weight', 4: 'Burg', 5: 'Itakura', 6: 'covariance'})

# ---- inputs and global variables
Method = _input('Method', 1)
LastBar = _input('LastBar', 30)
PastBars = _input('PastBars', 300)
LPOrder = _input('LPOrder', 0.6)
FutBars = _input('FutBars', 100)
HarmNo = _input('HarmNo', 20)
FreqTOL = _input('FreqTOL', 0.0001)
BurgWin = _input('BurgWin', 0)
FV_Buffer = Arr(0, 0.0)
PV_Buffer = Arr(0, 0.0)
ETA = 0.0
INFTY = 0.0
SMNO = 0.0
np_v = 0
nf = 0
lb = 0
no = 0
it = 0
StartBar = 0

def OnInit():
    global StartBar, lb, nf, no, np_v
    lb = LastBar
    np_v = PastBars
    no = _int(LPOrder * PastBars)
    nf = FutBars
    if Method > 1:
        nf = np_v - no - 1
    StartBar = PastBars
    SetIndexBuffer(0, FV_Buffer, INDICATOR_DATA)
    PlotIndexSetString(0, PLOT_LABEL, '')
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, StartBar)
    ArraySetAsSeries(FV_Buffer, True)
    PlotIndexSetInteger(0, PLOT_SHIFT, nf - lb)
    SetIndexBuffer(1, PV_Buffer, INDICATOR_DATA)
    PlotIndexSetString(1, PLOT_LABEL, '')
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, StartBar)
    ArraySetAsSeries(PV_Buffer, True)
    PlotIndexSetInteger(1, PLOT_SHIFT, -lb)
    shortname = 'Extrapolator'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < StartBar:
        return 0
    ArrayInitialize(PV_Buffer, EMPTY_VALUE)
    ArrayInitialize(FV_Buffer, EMPTY_VALUE)
    ArraySetAsSeries(open, True)
    a = Arr(0, 0.0)
    x = Arr(0, 0.0)
    av = 0.0
    for i in range(0, np_v):
        av += open[i + lb]
    av = _fdiv(av, np_v)
    if Method == 1:
        for i in range(0, np_v):
            PV_Buffer[i] = av
            if i <= nf:
                FV_Buffer[i] = av
    else:
        ArrayResize(a, no + 1)
        ArrayResize(x, np_v)
        for i in range(0, np_v):
            x[np_v - 1 - i] = open[i + lb] - av
    _sw1 = Method
    if _sw1 == 1:
        w = Box(0.0)
        m = Box(0.0)
        c = Box(0.0)
        s = Box(0.0)
        for harm in range(0, HarmNo):
            Freq(w, m, c, s, open)
            for i in range(0, np_v):
                PV_Buffer[i] += m.v + (c.v * MathCos(w.v * i)) + (s.v * MathSin(w.v * i))
                if i <= nf:
                    FV_Buffer[i] += m.v + (c.v * MathCos(w.v * i)) - (s.v * MathSin(w.v * i))
    elif _sw1 == 2:
        ACF(x, no, a)
    elif _sw1 == 3:
        WBurg(x, no, BurgWin, a)
    elif _sw1 == 4:
        HNBurg(x, no, a)
    elif _sw1 == 5:
        Geom(x, no, a)
    elif _sw1 == 6:
        stop = Box((0 != 0))
        MCov(x, no, a, stop)
        if stop.v == 1:
            Print('OnCalculate', '(): Early stop')
            return 0
        for i in range(no, 1 - 1, -1):
            a[i] = a[i - 1]
    if Method > 1:
        for n in range(no, np_v + nf):
            sum_ = 0.0
            for i in range(1, no + 1):
                if (n - i) < np_v:
                    sum_ -= a[i] * x[n - i]
                else:
                    sum_ -= a[i] * FV_Buffer[n - i - np_v + 1]
            if n < np_v:
                PV_Buffer[np_v - 1 - n] = sum_
            else:
                FV_Buffer[n - np_v + 1] = sum_
        FV_Buffer[0] = PV_Buffer[0]
        for i in range(0, np_v - no):
            PV_Buffer[i] += av
            FV_Buffer[i] += av
    tmp = 0.0
    i = 0
    while i <= ((nf - 1) / 2.0):
        tmp = FV_Buffer[i]
        FV_Buffer[i] = FV_Buffer[nf - i]
        FV_Buffer[nf - i] = tmp
        i += 1
    return rates_total

def Freq(w, m, c, s, Open):
    z = Arr(0, 0.0)
    num = 0.0
    den = 0.0
    ArrayResize(z, np_v)
    a = 0.0
    b = 2.0
    z[0] = Open[lb] - PV_Buffer[0]
    while MathAbs(a - b) > FreqTOL:
        a = b
        z[1] = Open[1 + lb] - PV_Buffer[1] + (a * z[0])
        num = z[0] * z[1]
        den = z[0] * z[0]
        for i in range(2, np_v):
            z[i] = Open[i + lb] - PV_Buffer[i] + (a * z[i - 1]) - z[i - 2]
            num += z[i - 1] * (z[i] + z[i - 2])
            den += z[i - 1] * z[i - 1]
        b = _fdiv(num, den)
    w.v = MathArccos(b / 2.0)
    Fit(w.v, m, c, s, Open)
    return

def Fit(w, m, c, s, Open):
    Sc = 0.0
    Ss = 0.0
    Scc = 0.0
    Sss = 0.0
    Scs = 0.0
    Sx = 0.0
    Sxx = 0.0
    Sxc = 0.0
    Sxs = 0.0
    for i in range(0, np_v):
        cos_ = MathCos(w * i)
        sin_ = MathSin(w * i)
        Sc += cos_
        Ss += sin_
        Scc += cos_ * cos_
        Sss += sin_ * sin_
        Scs += cos_ * sin_
        Sx += Open[i + lb] - PV_Buffer[i]
        Sxx += MathPow(Open[i + lb] - PV_Buffer[i], 2)
        Sxc += (Open[i + lb] - PV_Buffer[i]) * cos_
        Sxs += (Open[i + lb] - PV_Buffer[i]) * sin_
    Sc = _fdiv(Sc, np_v)
    Ss = _fdiv(Ss, np_v)
    Scc = _fdiv(Scc, np_v)
    Sss = _fdiv(Sss, np_v)
    Scs = _fdiv(Scs, np_v)
    Sx = _fdiv(Sx, np_v)
    Sxx = _fdiv(Sxx, np_v)
    Sxc = _fdiv(Sxc, np_v)
    Sxs = _fdiv(Sxs, np_v)
    if w == 0.0:
        m.v = Sx
        c.v = 0.0
        s.v = 0.0
    else:
        den = MathPow(Scs - (Sc * Ss), 2) - ((Scc - (Sc * Sc)) * (Sss - (Ss * Ss)))
        c.v = _fdiv(((Sxs - (Sx * Ss)) * (Scs - (Sc * Ss))) - ((Sxc - (Sx * Sc)) * (Sss - (Ss * Ss))), den)
        s.v = _fdiv(((Sxc - (Sx * Sc)) * (Scs - (Sc * Ss))) - ((Sxs - (Sx * Ss)) * (Scc - (Sc * Sc))), den)
        m.v = Sx - (c.v * Sc) - (s.v * Ss)
    return

def ACF(x, p, a):
    n = ArraySize(x)
    rxx = Arr(0, 0.0)
    r = 0.0
    E = 0.0
    tmp = 0.0
    ArrayResize(rxx, p + 1)
    i = 0
    j = 0
    k = 0
    kh = 0
    ki = 0
    j = 0
    for j in range(j, p + 1):
        rxx[j] = 0.0
        i = j
        for i in range(i, n):
            rxx[j] += x[i] * x[i - j]
        else:
            i = _range_end(i, n, 1)
    else:
        j = _range_end(j, p + 1, 1)
    E = rxx[0]
    k = 1
    for k in range(k, p + 1):
        r = -rxx[k]
        i = 1
        for i in range(i, k):
            r -= a[i] * rxx[k - i]
        else:
            i = _range_end(i, k, 1)
        r = _fdiv(r, E)
        a[k] = r
        kh = _idiv(k, 2)
        i = 1
        for i in range(i, kh + 1):
            ki = k - i
            tmp = a[i]
            a[i] += r * a[ki]
            if i != ki:
                a[ki] += r * tmp
        else:
            i = _range_end(i, kh + 1, 1)
        E *= 1 - (r * r)
    else:
        k = _range_end(k, p + 1, 1)

def WBurg(x, p, w, a):
    n = ArraySize(x)
    df = Arr(0, 0.0)
    db = Arr(0, 0.0)
    ArrayResize(df, n)
    ArrayResize(db, n)
    i = 0
    k = 0
    kh = 0
    ki = 0
    tmp = 0.0
    num = 0.0
    den = 0.0
    r = 0.0
    i = 0
    for i in range(i, n):
        df[i] = x[i]
        db[i] = x[i]
    else:
        i = _range_end(i, n, 1)
    k = 1
    for k in range(k, p + 1):
        num = 0.0
        den = 0.0
        if k == 1:
            i = 2
            for i in range(i, n):
                num += win(i, 2, n, w) * x[i - 1] * (x[i] + x[i - 2])
                den += win(i, 2, n, w) * x[i - 1] * x[i - 1]
            else:
                i = _range_end(i, n, 1)
            r = _fdiv(-num, den) / 2.0
            if r > 1:
                r = 1.0
            if r < -1.0:
                r = -1.0
        else:
            i = k
            for i in range(i, n):
                num += win(i, k, n, w) * df[i] * db[i - 1]
                den += win(i, k, n, w) * ((df[i] * df[i]) + (db[i - 1] * db[i - 1]))
            else:
                i = _range_end(i, n, 1)
            r = _fdiv(-2.0 * num, den)
        a[k] = r
        kh = _idiv(k, 2)
        i = 1
        for i in range(i, kh + 1):
            ki = k - i
            tmp = a[i]
            a[i] += r * a[ki]
            if i != ki:
                a[ki] += r * tmp
        else:
            i = _range_end(i, kh + 1, 1)
        if k < p:
            i = n - 1
            for i in range(i, k - 1, -1):
                tmp = df[i]
                df[i] += r * db[i - 1]
                db[i] = db[i - 1] + (r * tmp)
            else:
                i = _range_end(i, k - 1, -1)
    else:
        k = _range_end(k, p + 1, 1)

def win(i, k, n, w):
    if w == 0:
        return 1.0
    if w == 1:
        return 0.54 - (0.46 * MathCos(_fdiv(3.141592653589793 * ((2.0 * (i - k)) + 1.0), n - k)))
    if w == 2:
        return _fdiv(_fdiv(_fdiv(6.0 * (i - k + 1.0) * (n - i), n - k), n - k + 1.0), n - k + 2.0)
    return 0.0

def HNBurg(x, p, a):
    n = ArraySize(x)
    df = Arr(0, 0.0)
    db = Arr(0, 0.0)
    ArrayResize(df, n)
    ArrayResize(db, n)
    i = 0
    k = 0
    kh = 0
    ki = 0
    w = 0.0
    tmp = 0.0
    num = 0.0
    den = 0.0
    r = 0.0
    i = 0
    for i in range(i, n):
        df[i] = x[i]
        db[i] = x[i]
    else:
        i = _range_end(i, n, 1)
    k = 1
    for k in range(k, p + 1):
        num = 0.0
        den = 0.0
        if k == 1:
            i = 2
            for i in range(i, n):
                w = x[i - 1] * x[i - 1]
                num += w * x[i - 1] * (x[i] + x[i - 2])
                den += w * x[i - 1] * x[i - 1]
            else:
                i = _range_end(i, n, 1)
            r = _fdiv(-num, den) / 2.0
            if r > 1:
                r = 1.0
            if r < -1.0:
                r = -1.0
        else:
            w = 0.0
            i = 1
            for i in range(i, k):
                w += x[i] * x[i]
            else:
                i = _range_end(i, k, 1)
            i = k
            for i in range(i, n):
                num += w * df[i] * db[i - 1]
                den += w * ((df[i] * df[i]) + (db[i - 1] * db[i - 1]))
                w = w + (x[i] * x[i]) - (x[i - k + 1] * x[i - k + 1])
            else:
                i = _range_end(i, n, 1)
            r = _fdiv(-2.0 * num, den)
        a[k] = r
        kh = _idiv(k, 2)
        i = 1
        for i in range(i, kh + 1):
            ki = k - i
            tmp = a[i]
            a[i] += r * a[ki]
            if i != ki:
                a[ki] += r * tmp
        else:
            i = _range_end(i, kh + 1, 1)
        if k < p:
            i = n - 1
            for i in range(i, k - 1, -1):
                tmp = df[i]
                df[i] += r * db[i - 1]
                db[i] = db[i - 1] + (r * tmp)
            else:
                i = _range_end(i, k - 1, -1)
    else:
        k = _range_end(k, p + 1, 1)

def Geom(x, p, a):
    n = ArraySize(x)
    df = Arr(0, 0.0)
    db = Arr(0, 0.0)
    ArrayResize(df, n)
    ArrayResize(db, n)
    i = 0
    k = 0
    kh = 0
    ki = 0
    tmp = 0.0
    num = 0.0
    denf = 0.0
    denb = 0.0
    r = 0.0
    i = 0
    for i in range(i, n):
        df[i] = x[i]
        db[i] = x[i]
    else:
        i = _range_end(i, n, 1)
    k = 1
    for k in range(k, p + 1):
        num = 0.0
        denf = 0.0
        denb = 0.0
        i = k
        for i in range(i, n):
            num += df[i] * db[i - 1]
            denf += df[i] * df[i]
            denb += db[i - 1] * db[i - 1]
        else:
            i = _range_end(i, n, 1)
        r = _fdiv(_fdiv(-num, MathSqrt(denf)), MathSqrt(denb))
        a[k] = r
        kh = _idiv(k, 2)
        i = 1
        for i in range(i, kh + 1):
            ki = k - i
            tmp = a[i]
            a[i] += r * a[ki]
            if i != ki:
                a[ki] += r * tmp
        else:
            i = _range_end(i, kh + 1, 1)
        if k < p:
            i = n - 1
            for i in range(i, k - 1, -1):
                tmp = df[i]
                df[i] += r * db[i - 1]
                db[i] = db[i - 1] + (r * tmp)
            else:
                i = _range_end(i, k - 1, -1)
    else:
        k = _range_end(k, p + 1, 1)

def MCov(x, ip, a, stop):
    n = ArraySize(x)
    c = Arr(0, 0.0)
    d = Arr(0, 0.0)
    r = Arr(0, 0.0)
    v = 0.0
    ArrayResize(c, ip + 1)
    ArrayResize(d, ip + 1)
    ArrayResize(r, ip)
    k = 0
    m = 0
    mk = 0
    r1 = 0.0
    r2 = 0.0
    r3 = 0.0
    r4 = 0.0
    r5 = 0.0
    delta = 0.0
    gamma = 0.0
    lambda_ = 0.0
    theta = 0.0
    psi = 0.0
    xi = 0.0
    save1 = 0.0
    save2 = 0.0
    save3 = 0.0
    save4 = 0.0
    c1 = 0.0
    c2 = 0.0
    c3 = 0.0
    c4 = 0.0
    ef = 0.0
    eb = 0.0
    r1 = 0.0
    k = 1
    for k in range(k, n - 1):
        r1 += 2.0 * x[k] * x[k]
    else:
        k = _range_end(k, n - 1, 1)
    r2 = x[n - 1] * x[n - 1]
    r3 = x[0] * x[0]
    r4 = _fdiv(1.0, r1 + (2.0 * (r2 + r3)))
    v = r1 + r2 + r3
    delta = 1.0 - (r2 * r4)
    gamma = 1.0 - (r3 * r4)
    lambda_ = x[0] * x[n - 1] * r4
    c[0] = x[0] * r4
    d[0] = x[n - 1] * r4
    m = 0
    while True:
        save1 = 0.0
        k = m + 1
        for k in range(k, n):
            save1 += x[n - 1 - k] * x[n - k + m]
        else:
            k = _range_end(k, n, 1)
        save1 *= 2.0
        r[m] = save1
        theta = x[0] * d[0]
        psi = x[0] * c[0]
        xi = x[n - 1] * d[0]
        if m > 0:
            k = 1
            for k in range(k, m + 1):
                theta += x[k] * d[k]
                psi += x[k] * c[k]
                xi += x[n - 1 - k] * d[k]
                r[k - 1] -= (x[m] * x[m - k]) + (x[n - 1 - m] * x[n - 1 - m + k])
                save1 += r[k - 1] * a[m - k]
            else:
                k = _range_end(k, m + 1, 1)
        c1 = _fdiv(-save1, v)
        a[m] = c1
        v *= 1.0 - (c1 * c1)
        if m > 0:
            k = 0
            for k in range(k, _idiv(m + 1, 2)):
                mk = m - k - 1
                save1 = a[k]
                a[k] = save1 + (c1 * a[mk])
                if k != mk:
                    a[mk] += c1 * save1
            else:
                k = _range_end(k, _idiv(m + 1, 2), 1)
        if m == (ip - 1):
            v *= _fdiv(0.5, n - 1 - m)
            break
        r1 = _fdiv(1.0, (delta * gamma) - (lambda_ * lambda_))
        c1 = ((theta * lambda_) + (psi * delta)) * r1
        c2 = ((psi * lambda_) + (theta * gamma)) * r1
        c3 = ((xi * lambda_) + (theta * delta)) * r1
        c4 = ((theta * lambda_) + (xi * gamma)) * r1
        k = 0
        for k in range(k, _idiv(m, 2) + 1):
            mk = m - k
            save1 = c[k]
            save2 = d[k]
            save3 = c[mk]
            save4 = d[mk]
            c[k] += (c1 * save3) + (c2 * save4)
            d[k] += (c3 * save3) + (c4 * save4)
            if k != mk:
                c[mk] += (c1 * save1) + (c2 * save2)
                d[mk] += (c3 * save1) + (c4 * save2)
        else:
            k = _range_end(k, _idiv(m, 2) + 1, 1)
        r2 = psi * psi
        r3 = theta * theta
        r4 = xi * xi
        r5 = gamma - (((r2 * delta) + (r3 * gamma) + (2.0 * psi * lambda_ * theta)) * r1)
        r2 = delta - (((r3 * delta) + (r4 * gamma) + (2.0 * theta * lambda_ * xi)) * r1)
        gamma = r5
        delta = r2
        lambda_ += (c3 * psi) + (c4 * theta)
        if v <= 0.0:
            Print('MCov', '(): Error! : Negative or zero value of the v variable')
            stop.v = True
            return
        if ((delta <= 0.0 or delta > 1.0) or gamma <= 0.0) or gamma > 1.0:
            Print('MCov', '(): (): Error! : delta and gamma variables values out of the range (0,1)')
            stop.v = True
            return
        r1 = _fdiv(1.0, v)
        r2 = _fdiv(1.0, (delta * gamma) - (lambda_ * lambda_))
        ef = x[n - m - 2]
        eb = x[m + 1]
        k = 0
        for k in range(k, m + 1):
            ef += a[k] * x[n - 1 - m + k]
            eb += a[k] * x[m - k]
        else:
            k = _range_end(k, m + 1, 1)
        c1 = eb * r1
        c2 = ef * r1
        c3 = ((eb * delta) + (ef * lambda_)) * r2
        c4 = ((ef * gamma) + (eb * lambda_)) * r2
        k = m
        for k in range(k, 0 - 1, -1):
            save1 = a[k]
            a[k] = save1 + (c3 * c[k]) + (c4 * d[k])
            c[k + 1] = c[k] + (c1 * save1)
            d[k + 1] = d[k] + (c2 * save1)
        else:
            k = _range_end(k, 0 - 1, -1)
        c[0] = c1
        d[0] = c2
        r3 = eb * eb
        r4 = ef * ef
        v -= ((r3 * delta) + (r4 * gamma) + (2.0 * ef * eb * lambda_)) * r2
        delta -= r4 * r1
        gamma -= r3 * r1
        lambda_ += ef * eb * r1
        if v <= 0.0:
            Print('MCov', '(): Error! : Negative or zero value of the v variable')
            stop.v = True
            return
        if ((delta <= 0.0 or delta > 1.0) or gamma <= 0.0) or gamma > 1.0:
            Print('MCov', '(): (): Error! : delta and gamma variables values out of the range (0,1)')
            stop.v = True
            return
        m += 1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Extrapolator(_MQL5Indicator):
    name = 'extrapolator'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'Method': _Choice({1: 'Extrapolation Method', 2: 'Autocorrelation Method', 3: 'Weighted Burg Method', 4: 'Burg Method with Helme-Nikias weighting function', 5: 'Itakura-Saito (geometric) method', 6: 'Modified covariance method'}, default=1),
        'LastBar': 30,
        'PastBars': 300,
        'LPOrder': 0.6,
        'FutBars': 100,
        'HarmNo': 20,
        'FreqTOL': 0.0001,
        'BurgWin': 0,
    }

