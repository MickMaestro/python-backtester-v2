"""cointegration_indicator — converted from MQL5: MQL5 Indicators/Cointegration/cointegration_indicator.mq5


Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Missing include files: Math\\Alglib\\alglib.mqh
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'window': 'separate', 'indicator_buffers': 30, 'indicator_plots': 30}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1, 16: 1, 17: 1, 18: 1, 19: 1, 20: 1, 21: 1, 22: 1, 23: 1, 24: 1, 25: 1, 26: 1, 27: 1, 28: 1, 29: 1, 30: 1}, 'colors': {1: [128], 2: [32768], 3: [36095], 4: [7346457], 5: [32896], 6: [14822282], 7: [9109643], 8: [65407], 9: [16711680], 10: [14822282], 11: [2763429], 12: [8894686], 13: [65407], 14: [1993170], 15: [5275647], 16: [15570276], 17: [14481663], 18: [3937500], 19: [16776960], 20: [9109504], 21: [9109504], 22: [9109504], 23: [9109504], 24: [9109504], 25: [9109504], 26: [9109504], 27: [9109504], 28: [9109504], 29: [9109504], 30: [9109504]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'cointegration_indicator', 'source': 'MQL5 Indicators/Cointegration/cointegration_indicator.mq5', 'folder': 'Cointegration', 'inputs': [{'mql': 'learning_depth', 'py': 'learning_depth', 'param': 'learning_depth', 'type': 'int', 'default': 500, 'label': '', 'sinput': False}, {'mql': 'SymbolsList', 'py': 'SymbolsList', 'param': None, 'type': 'string', 'default': 'AUDUSD,GBPUSD,NZDUSD', 'label': '', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': ['Math\\Alglib\\alglib.mqh'], 'imports': [], 'libraries': []}

# ---- inputs and global variables
FactorialsTable = Arr.of([1.0, 1.0, 2.0, 6.0, 24.0, 120.0, 720.0, 5040.0, 40320.0, 362880.0, 3628800.0, 39916800.0, 479001600.0, 6227020800.0, 87178291200.0, 1307674368000.0, 20922789888000.0, 355687428096000.0, 6402373705728000.0, 121645100408832000.0, 2432902008176640000.0], fill=0.0, dyn=False, size=21)
retcode = 0
learning_depth = _input('learning_depth', 500)
SymbolsList = _input('SymbolsList', 'AUDUSD,GBPUSD,NZDUSD')
mainsynthetic = Arr(0, 0.0)
zscore = Arr(0, 0.0)
splittedPairsNumber = 0
splittedPairs = Arr(0, "")
last_time = 0
second_call = False

class spreads(MqlObject):
    _q_fields = ('symbol', 'spreadBuffer', 'pricesBuffer', 'zscore', 'weights')
    def __init__(self, *args):
        self.symbol = ""
        self.spreadBuffer = Arr(0, 0.0)
        self.pricesBuffer = Arr(0, 0.0)
        self.zscore = Arr(0, 0.0)
        self.weights = Arr(0, 0.0)

def MathRandomNonZero():
    rnd = 0.0
    while rnd == 0.0 or rnd == 1.0:
        rnd = MathRand() / 32767.0
    return rnd

def MathMoments(array, mean, variance, skewness, kurtosis, start=0, count=WHOLE_ARRAY):
    mean.v = 0.0
    variance.v = 0.0
    skewness.v = 0.0
    kurtosis.v = 0.0
    size = ArraySize(array)
    data_count = 0
    if count == WHOLE_ARRAY:
        data_count = size
    else:
        data_count = count
    if data_count == 0:
        return False
    if (start + data_count) > size:
        return False
    ind1 = start
    ind2 = ind1 + data_count - 1
    for i in range(ind1, ind2 + 1):
        mean.v += array[i]
    mean.v = _fdiv(mean.v, data_count)
    S = 0.0
    if data_count > 1:
        for i in range(ind1, ind2 + 1):
            variance.v += MathPow_u_2(array[i] - mean.v, 2.0)
        variance.v = _fdiv(variance.v, data_count - 1)
        S = MathSqrt_u_2(variance.v)
    else:
        variance.v = QNaN
    if data_count > 2 and S > 0.0:
        for i in range(ind1, ind2 + 1):
            skewness.v += MathPow_u_2(array[i] - mean.v, 3.0)
        skewness.v = _fdiv(skewness.v, data_count * MathPow_u_2(S, 3.0))
    else:
        skewness.v = QNaN
    if data_count > 3 and S > 0.0:
        for i in range(ind1, ind2 + 1):
            kurtosis.v += MathPow_u_2(array[i] - mean.v, 4.0)
        kurtosis.v = _fdiv(kurtosis.v, data_count * MathPow_u_2(S, 4.0))
        kurtosis.v -= 3
    else:
        kurtosis.v = QNaN
    if ((not MathIsValidNumber(variance.v)) or (not MathIsValidNumber(skewness.v))) or (not MathIsValidNumber(kurtosis.v)):
        return False
    else:
        return True

def MathPowInt(x, power):
    if power == 0:
        return 1.0
    if power < 0:
        return 0.0
    val = x
    for i in range(2, power + 1):
        val *= x
    return val

def MathFactorial(n):
    if n < 0:
        return 0.0
    if n <= 20:
        return FactorialsTable[n]
    else:
        val = FactorialsTable[20]
        for i in range(21, n + 1):
            val *= i
        return val

def MathTrunc_1(x):
    if x >= 0:
        return MathFloor_u_2(x)
    else:
        return MathCeil_u_2(x)

def MathTrunc_2(array, result):
    size = ArraySize(array)
    if size == 0:
        return False
    if ArraySize(result) < size:
        if ArrayResize(result, size) != size:
            return False
    for i in range(0, size):
        if array[i] >= 0:
            result[i] = MathFloor_u_2(array[i])
        else:
            result[i] = MathCeil_u_2(array[i])
    return True

def MathTrunc_3(array):
    size = ArraySize(array)
    if size == 0:
        return False
    for i in range(0, size):
        if array[i] >= 0:
            array[i] = MathFloor_u_2(array[i])
        else:
            array[i] = MathCeil_u_2(array[i])
    return True

def MathRound_u_1(x, digits):
    if not MathIsValidNumber(x):
        return QNaN
    if x == 0.0:
        return x
    if digits > 0:
        sign = 1.0
        xx = x
        if xx < 0.0:
            xx = -xx
            sign = -1.0
        pwr_factor = MathPow_u_2(10, digits)
        int_value = MathFloor_u_2(xx)
        res = (xx - int_value) * pwr_factor
        res = MathFloor_u_2(MathAbs_u_2(res) + 0.5)
        return sign * (int_value + _fdiv(res, pwr_factor))
    elif digits == 0:
        return MathRound(x)
    return 0.0

def MathRound_u_2(array, digits, result):
    size = ArraySize(array)
    if size == 0:
        return False
    if digits < 0:
        return False
    if ArraySize(result) < size:
        if ArrayResize(result, size) != size:
            return False
    for i in range(0, size):
        result[i] = MathRound_u_1(array[i], digits)
    return True

def MathRound_u_3(array, digits):
    size = ArraySize(array)
    if size == 0:
        return False
    if digits < 0:
        return False
    for i in range(0, size):
        array[i] = MathRound_u_1(array[i], digits)
    return True

def MathGamma(x):
    logsqrt2pi = MathLog_u_2(MathSqrt_u_2(2 * M_PI))
    xminin = 2.23e-308
    xbig = 171.624
    eps = 2.22e-16
    p = Arr.of([-1.716185138865495, 24.76565080557592, -379.80425647094563, 629.3311553128184, 866.9662027904133, -31451.272968848367, -36144.413418691176, 66456.14382024054], fill=0.0, dyn=False, size=8)
    q = Arr.of([-30.840230011973897, 315.35062697960416, -1015.1563674902192, -3107.771671572311, 22538.11842098015, 4755.846277527881, -134659.9598649693, -115132.25967555349], fill=0.0, dyn=False, size=8)
    c = Arr.of([-0.001910444077728, 0.00084171387781295, -0.0005952379913043012, 0.0007936507935003503, -0.0027777777777776816, 0.08333333333333333, 0.0057083835261], fill=0.0, dyn=False, size=7)
    parity = 0
    fact = 1.0
    n = 0
    y = x
    y1 = 0.0
    res = 0.0
    z = 0.0
    xnum = 0.0
    xden = 0.0
    ysq = 0.0
    sum_ = 0.0
    if y <= 0.0:
        y = -x
        y1 = MathTrunc_1(y)
        res = y - y1
        if res != 0.0:
            if y1 != (MathTrunc_1(y1 * 0.5) * 2.0):
                parity = 1
            fact = _fdiv(-M_PI, MathSin_u_2(M_PI * res))
            y = y + 1.0
        else:
            return QPOSINF
    if y < eps:
        if y >= xminin:
            res = _fdiv(1.0, y)
        else:
            return QPOSINF
    elif y < 12.0:
        y1 = y
        if y < 1.0:
            z = y
            y = y + 1.0
        else:
            n = _int(y) - 1
            y = y - float(n)
            z = y - 1.0
        xnum = 0.0
        xden = 1.0
        for i in range(0, 8):
            xnum = (xnum + p[i]) * z
            xden = (xden * z) + q[i]
        res = _fdiv(xnum, xden) + 1.0
        if y1 < y:
            res = _fdiv(res, y1)
        elif y1 > y:
            for i in range(0, n):
                res = res * y
                y = y + 1.0
    else:
        if y <= xbig:
            ysq = y * y
            sum_ = c[6]
            for i in range(0, 6):
                sum_ = _fdiv(sum_, ysq) + c[i]
            sum_ = _fdiv(sum_, y) - y + logsqrt2pi
            sum_ = sum_ + ((y - 0.5) * MathLog_u_2(y))
            res = MathExp_u_2(sum_)
        else:
            return QPOSINF
    if parity == 1:
        res = -res
    if fact != 1.0:
        res = _fdiv(fact, res)
    return res

def MathGammaLog(x):
    pnt68 = 0.6796875
    sqrtpi = 0.9189385332046728
    xbig = 2.55e+305
    xinf = 1.79e+308
    eps = 2.22e-16
    frtbig = 2.25e+76
    d1 = -0.5772156649015329
    p1 = Arr.of([4.945235359296727, 201.8112620856775, 2290.8383738313464, 11319.672059033808, 28557.246356716354, 38484.962284437934, 26377.487876241954, 7225.813979700288], fill=0.0, dyn=False, size=8)
    q1 = Arr.of([67.48212550303778, 1113.3323938571993, 7738.757056935398, 27639.870744033407, 54993.102062261576, 61611.22180066002, 36351.2759150194, 8785.536302431014], fill=0.0, dyn=False, size=8)
    d2 = 0.42278433509846713
    p2 = Arr.of([4.974607845568932, 542.4138599891071, 15506.93864978365, 184793.29044456323, 1088204.7694688288, 3338152.96798703, 5106661.678927353, 3074109.0548505397], fill=0.0, dyn=False, size=8)
    q2 = Arr.of([183.03283993705926, 7765.049321445006, 133190.38279660742, 1136705.8213219696, 5267964.117437947, 13467014.543111017, 17827365.303532742, 9533095.591844354], fill=0.0, dyn=False, size=8)
    d4 = 1.791759469228055
    p4 = Arr.of([14745.0216605994, 2426813.3694867045, 121475557.40450932, 2663432449.630977, 29403789566.34554, 170266573776.5399, 492612579337.7431, 560625185622.3951], fill=0.0, dyn=False, size=8)
    q4 = Arr.of([2690.5301758708993, 639388.5654300093, 41355999.30241388, 1120872109.616148, 14886137286.788137, 101680358627.24382, 341747634550.73773, 446315818741.9713], fill=0.0, dyn=False, size=8)
    c = Arr.of([-0.001910444077728, 0.00084171387781295, -0.0005952379913043012, 0.0007936507935003503, -0.0027777777777776816, 0.08333333333333333, 0.0057083835261], fill=0.0, dyn=False, size=7)
    y = x
    res = 0.0
    corr = 0.0
    xm1 = 0.0
    xm2 = 0.0
    xm4 = 0.0
    xden = 0.0
    xnum = 0.0
    ysq = 0.0
    if y > 0 and y <= xbig:
        if y <= eps:
            res = -MathLog_u_2(y)
        else:
            if y <= 1.5:
                if y < pnt68:
                    corr = -MathLog_u_2(y)
                    xm1 = y
                else:
                    corr = 0.0
                    xm1 = y - 0.5 - 0.5
                if y <= 0.5 or y >= pnt68:
                    xden = 1.0
                    xnum = 0.0
                    for i in range(0, 8):
                        xnum = (xnum * xm1) + p1[i]
                        xden = (xden * xm1) + q1[i]
                    res = corr + (xm1 * (d1 + (xm1 * _fdiv(xnum, xden))))
                else:
                    xm2 = y - 0.5 - 0.5
                    xden = 1.0
                    xnum = 0.0
                    for i in range(0, 8):
                        xnum = (xnum * xm2) + p2[i]
                        xden = (xden * xm2) + q2[i]
                    res = corr + (xm2 * (d2 + (xm2 * _fdiv(xnum, xden))))
            else:
                if y <= 4.0:
                    xm2 = y - 2.0
                    xden = 1.0
                    xnum = 0.0
                    for i in range(0, 8):
                        xnum = (xnum * xm2) + p2[i]
                        xden = (xden * xm2) + q2[i]
                    res = xm2 * (d2 + (xm2 * _fdiv(xnum, xden)))
                else:
                    if y <= 12.0:
                        xm4 = y - 4.0
                        xden = -1.0
                        xnum = 0.0
                        for i in range(0, 8):
                            xnum = (xnum * xm4) + p4[i]
                            xden = (xden * xm4) + q4[i]
                        res = d4 + (xm4 * _fdiv(xnum, xden))
                    else:
                        res = 0.0
                        if y <= frtbig:
                            res = c[6]
                            ysq = y * y
                            for i in range(0, 6):
                                res = _fdiv(res, ysq) + c[i]
                        res = _fdiv(res, y)
                        corr = MathLog_u_2(y)
                        res = res + sqrtpi - (0.5 * corr)
                        res = res + (y * (corr - 1.0))
    else:
        if y < 0 and MathFloor_u_2(y) != y:
            if y > -1e-100:
                res = (-2 * MathLog_u_2(MathAbs_u_2(y))) - MathGammaLog(-y)
            else:
                res = MathLog_u_2(_fdiv(M_PI, MathAbs_u_2(y * MathSin_u_2(M_PI * y)))) - MathGammaLog(-y)
        else:
            res = QPOSINF
    return res

def MathBeta(a, b):
    return MathExp_u_2(MathBetaLog(a, b))

def MathBetaLog(a, b):
    return MathGammaLog(a) + MathGammaLog(b) - MathGammaLog(a + b)

def MathBetaIncomplete(x, p, q):
    acu = 1e-17
    pp = 0.0
    qq = 0.0
    xx = 0.0
    ifault = 0
    value = x
    if p <= 0.0 or q <= 0.0:
        ifault = 1
        return value
    if x < 0.0 or 1.0 < x:
        ifault = 2
        return value
    if x == 0.0 or x == 1.0:
        return value
    beta_log = MathGammaLog(p) + MathGammaLog(q) - MathGammaLog(p + q)
    psq = p + q
    cx = 1.0 - x
    indx = 0
    if p < (psq * x):
        xx = cx
        cx = x
        pp = q
        qq = p
        indx = 1
    else:
        xx = x
        pp = p
        qq = q
        indx = 0
    value = 1.0
    term = 1.0
    ai = 1.0
    ns = _int(qq + (cx * psq))
    rx = _fdiv(xx, cx)
    temp = qq - ai
    if ns == 0.0:
        rx = xx
    while True:
        term = _fdiv(term * temp * rx, pp + ai)
        value = value + term
        temp = MathAbs_u_2(term)
        if temp <= acu and temp <= (acu * value):
            value = _fdiv(value * MathExp_u_2((pp * MathLog_u_2(xx)) + ((qq - 1.0) * MathLog_u_2(cx)) - beta_log), pp)
            if indx:
                value = 1.0 - value
            break
        ai = ai + 1.0
        ns -= 1
        if 0 <= ns:
            temp = qq - ai
            if ns == 0:
                rx = xx
        else:
            temp = psq
            psq = psq + 1.0
    return value

def MathGammaIncomplete(x, alpha):
    eps = 1e-19
    iflag = 0
    ll = False
    imax = 5000
    uflo = 1e-100
    cdfx = 0.0
    k = 0
    if alpha <= uflo or eps <= uflo:
        iflag = 1
        return QNaN
    iflag = 0
    if x <= 0.0:
        return QNaN
    dx = x
    pdfl = ((alpha - 1.0) * MathLog_u_2(dx)) - dx - MathGammaLog(alpha)
    if pdfl < MathLog_u_2(uflo):
        if x >= alpha:
            cdfx = 1.0
    else:
        p = alpha
        u = MathExp_u_2(pdfl)
        ll = True
        if x >= p:
            k = _int(p)
            if p <= float(k):
                k = k - 1
            eta = p - float(k)
            bl = ((eta - 1.0) * MathLog_u_2(dx)) - dx - MathGammaLog(eta)
            ll = bl > MathLog_u_2(eps)
        epsx = _fdiv(eps, x)
        if ll == True:
            for i in range(0, imax + 1):
                if u <= (epsx * (p - x)):
                    return cdfx
                u = _fdiv(x * u, p)
                cdfx = cdfx + u
                p = p + 1.0
            iflag = 2
        else:
            for j in range(1, k + 1):
                p = p - 1.0
                if u <= (epsx * (x - p)):
                    break
                cdfx = cdfx + u
                u = _fdiv(p * u, x)
            cdfx = 1.0 - cdfx
    return cdfx

def MathBinomialCoefficient(n, k):
    mn = 0
    mx = 0
    value = 0
    n_k = n - k
    if k < n_k:
        mn = k
        mx = n_k
    else:
        mn = n_k
        mx = k
    if mn > 0:
        value = mx + 1
        for i in range(2, mn + 1):
            value = _idiv(value * (mx + i), i)
    else:
        if mn < 0:
            return 0
        if mn == 0:
            return 1
    return value

def MathBinomialCoefficientLog_1(n, k):
    mn = 0
    mx = 0
    value = 0
    n_k = n - k
    if k < n_k:
        mn = k
        mx = n_k
    else:
        mn = n_k
        mx = k
    if mn > 0:
        value = mx + 1
        for i in range(2, mn + 1):
            value = _idiv(value * (mx + i), i)
    else:
        if mn < 0:
            return QNEGINF
        if mn == 0:
            return 0.0
    return MathLog_u_2(value)

def MathBinomialCoefficientLog_2(n, k):
    return MathGammaLog(n + 1) - MathGammaLog(k + 1) - MathGammaLog(n - k + 1)

def MathHypergeometric2F2(a, b, c, d, z):
    a1 = 1.0
    b1 = 1.0
    tol = 1e-09
    for j in range(1, 500 + 1):
        a1 = _fdiv(_fdiv(_fdiv((a + j - 1) * (b + j - 1), c + j - 1), d + j - 1) * z, j) * a1
        b1 = b1 + a1
        if _idiv(MathAbs_u_2(a1), MathAbs_u_2(b1)) < tol:
            return b1
    return QNaN

def TailLog0(tail, log_mode):
    if tail == True:
        if log_mode == True:
            return QNEGINF
        else:
            return 0.0
    else:
        if log_mode == True:
            return 0.0
        else:
            return 1.0

def TailLog1(tail, log_mode):
    if tail == True:
        if log_mode == True:
            return 0.0
        else:
            return 1.0
    else:
        if log_mode == True:
            return 1.0
        else:
            return 0.0

def TailLogValue(value, tail, log_mode):
    if tail == True:
        if log_mode:
            return MathLog_u_2(MathAbs_u_2(value))
        else:
            return value
    else:
        if log_mode:
            return MathLog_u_2(MathAbs_u_2(1.0 - value))
        else:
            return 1.0 - value

def TailLogProbability(probability, tail, log_mode):
    if tail == True:
        if log_mode:
            return MathExp_u_2(probability)
        else:
            return probability
    else:
        if log_mode:
            return 1.0 - MathExp_u_2(probability)
        else:
            return 1.0 - probability

def MathSequence_1(from_, to, step, result):
    if ((not MathIsValidNumber(from_)) or (not MathIsValidNumber(to))) or (not MathIsValidNumber(step)):
        return False
    if to < from_:
        return False
    count = 1 + _int(_fdiv(to - from_, step))
    if ArraySize(result) < count:
        if ArrayResize(result, count) != count:
            return False
    for i in range(0, count):
        result[i] = from_ + (i * step)
    return True

def MathSequence_2(from_, to, step, result):
    if to < from_:
        return False
    count = 1 + _idiv(to - from_, step)
    if ArraySize(result) < count:
        if ArrayResize(result, count) != count:
            return False
    for i in range(0, count):
        result[i] = from_ + (i * step)
    return True

def MathSequenceByCount_1(from_, to, count, result):
    if (not MathIsValidNumber(from_)) or (not MathIsValidNumber(to)):
        return False
    if to < from_ or count <= 0:
        return False
    if ArraySize(result) < count:
        if ArrayResize(result, count) != count:
            return False
    step = (0 if (count == 1) else _fdiv(to - from_, count - 1))
    for i in range(0, count):
        result[i] = from_ + (i * step)
    return True

def MathSequenceByCount_2(from_, to, count, result):
    if to < from_ or count <= 0:
        return False
    if ArraySize(result) < count:
        if ArrayResize(result, count) != count:
            return False
    step = (0 if (count == 1) else _idiv(to - from_, count - 1))
    for i in range(0, count):
        result[i] = from_ + (i * step)
    return True

def MathReplicate_1(array, count, result):
    size = ArraySize(array)
    if size == 0:
        return False
    if count <= 0:
        return False
    target_size = size * count
    if ArraySize(result) < target_size:
        if ArrayResize(result, target_size) != target_size:
            return False
    for i in range(0, count):
        ArrayCopy(result, array, i * size, 0, WHOLE_ARRAY)
    return True

def MathReplicate_2(array, count, result):
    size = ArraySize(array)
    if size == 0:
        return False
    if count <= 0:
        return False
    target_size = size * count
    if ArraySize(result) < target_size:
        if ArrayResize(result, target_size) != target_size:
            return False
    for i in range(0, count):
        ArrayCopy(result, array, i * size, 0, WHOLE_ARRAY)
    return True

def MathReverse_1(array, result):
    size = ArraySize(array)
    if size == 0:
        return False
    if ArraySize(result) < size:
        if ArrayResize(result, size) != size:
            return False
    for i in range(0, size):
        idx = size - 1 - i
        result[idx] = array[i]
    return True

def MathReverse_2(array, result):
    size = ArraySize(array)
    if size == 0:
        return False
    if ArraySize(result) < size:
        if ArrayResize(result, size) != size:
            return False
    for i in range(0, size):
        idx = size - 1 - i
        result[idx] = array[i]
    return True

def MathReverse_3(array):
    size = ArraySize(array)
    if size == 0:
        return False
    count = _idiv(size, 2)
    for i in range(0, count):
        idx = size - 1 - i
        t = array[i]
        array[i] = array[idx]
        array[idx] = t
    return True

def MathReverse_4(array):
    size = ArraySize(array)
    if size == 0:
        return False
    count = _idiv(size, 2)
    for i in range(0, count):
        idx = size - 1 - i
        t = array[i]
        array[i] = array[idx]
        array[idx] = t
    return True

def MathIdentical_1(array1, array2):
    size1 = ArraySize(array1)
    size2 = ArraySize(array1)
    if size1 != size2:
        return False
    if size1 == 0:
        return False
    for i in range(0, size1):
        if array1[i] != array2[i]:
            return False
    return True

def MathIdentical_2(array1, array2):
    size1 = ArraySize(array1)
    size2 = ArraySize(array1)
    if size1 != size2:
        return False
    if size1 == 0:
        return False
    for i in range(0, size1):
        if array1[i] != array2[i]:
            return False
    return True

def MathUnique_1(array, result):
    size = ArraySize(array)
    if size == 0:
        return False
    checked = Arr(0, False)
    if ArrayResize(checked, size) != size:
        return False
    ArrayFill(checked, 0, size, False)
    if ArraySize(result) < size:
        if ArrayResize(result, size) != size:
            return False
    unique_count = 0
    value = 0.0
    while True:
        flag = False
        for i in range(unique_count, size):
            if (not flag) and (not checked[i]):
                value = array[i]
                result[unique_count] = array[i]
                unique_count += 1
                checked[i] = True
                flag = True
            elif flag and value == array[i]:
                checked[i] = True
        if not flag:
            break
    ArrayResize(result, unique_count)
    return True

def MathUnique_2(array, result):
    size = ArraySize(array)
    if size == 0:
        return False
    checked = Arr(0, False)
    if ArrayResize(checked, size) != size:
        return False
    ArrayFill(checked, 0, size, False)
    if ArraySize(result) < size:
        if ArrayResize(result, size) != size:
            return False
    unique_count = 0
    value = 0
    while True:
        flag = False
        for i in range(unique_count, size):
            if (not flag) and (not checked[i]):
                value = array[i]
                result[unique_count] = array[i]
                unique_count += 1
                checked[i] = True
                flag = True
            elif flag and value == array[i]:
                checked[i] = True
        if not flag:
            break
    ArrayResize(result, unique_count)
    return True

def MathQuickSortAscending(array, indices, first, last):
    i = 0
    j = 0
    t_int = 0
    p_double = 0.0
    t_double = 0.0
    if first < 0 or last < 0:
        return
    i = first
    j = last
    while i < last:
        p_double = array[(first + last) >> 1]
        while i < j:
            while array[i] < p_double:
                if i == (ArraySize(array) - 1):
                    break
                i += 1
            while array[j] > p_double:
                if j == 0:
                    break
                j -= 1
            if i <= j:
                t_double = array[i]
                array[i] = array[j]
                array[j] = t_double
                t_int = indices[i]
                indices[i] = indices[j]
                indices[j] = t_int
                i += 1
                if j == 0:
                    break
                j -= 1
        if first < j:
            MathQuickSortAscending(array, indices, first, j)
        first = i
        j = last

def MathQuickSortDescending(array, indices, first, last):
    i = 0
    j = 0
    t_int = 0
    p_double = 0.0
    t_double = 0.0
    if first < 0 or last < 0:
        return
    i = first
    j = last
    while i < last:
        p_double = array[(first + last) >> 1]
        while i < j:
            while array[i] > p_double:
                if i == (ArraySize(array) - 1):
                    break
                i += 1
            while array[j] < p_double:
                if j == 0:
                    break
                j -= 1
            if i <= j:
                t_double = array[i]
                array[i] = array[j]
                array[j] = t_double
                t_int = indices[i]
                indices[i] = indices[j]
                indices[j] = t_int
                i += 1
                if j == 0:
                    break
                j -= 1
        if first < j:
            MathQuickSortDescending(array, indices, first, j)
        first = i
        j = last

def MathQuickSort(array, indices, first, last, mode):
    if mode > 0:
        MathQuickSortAscending(array, indices, first, last)
    else:
        MathQuickSortDescending(array, indices, first, last)

def MathOrder_1(array, result):
    size = ArraySize(array)
    if size == 0:
        return False
    tmp_array = Arr(0, 0.0)
    ArrayCopy(tmp_array, array, 0, 0, WHOLE_ARRAY)
    if ArraySize(result) < size:
        if ArrayResize(result, size) != size:
            return False
    for i in range(0, size):
        result[i] = i + 1
    MathQuickSortAscending(tmp_array, result, 0, size - 1)
    return True

def MathOrder_2(array, result):
    size = ArraySize(array)
    if size == 0:
        return False
    tmp_array = Arr(0, 0.0)
    if ArrayResize(tmp_array, size) != size:
        return False
    for i in range(0, size):
        tmp_array[i] = array[i]
    if ArraySize(result) < size:
        if ArrayResize(result, size) != size:
            return False
    for i in range(0, size):
        result[i] = i + 1
    MathQuickSortAscending(tmp_array, result, 0, size - 1)
    return True

def MathBitwiseNot_1(array, result):
    size = ArraySize(array)
    if size == 0:
        return False
    if ArraySize(result) < size:
        if ArrayResize(result, size) != size:
            return False
    for i in range(0, size):
        result[i] = ~array[i]
    return True

def MathBitwiseNot_2(array):
    size = ArraySize(array)
    if size == 0:
        return False
    for i in range(0, size):
        array[i] = ~array[i]
    return True

def MathBitwiseAnd(array1, array2, result):
    size1 = ArraySize(array1)
    size2 = ArraySize(array2)
    if (size1 == 0 or size2 == 0) or size1 != size2:
        return False
    if ArraySize(result) < size1:
        if ArrayResize(result, size1) != size1:
            return False
    for i in range(0, size1):
        result[i] = array1[i] & array2[i]
    return True

def MathBitwiseOr(array1, array2, result):
    size1 = ArraySize(array1)
    size2 = ArraySize(array2)
    if (size1 == 0 or size2 == 0) or size1 != size2:
        return False
    if ArraySize(result) < size1:
        if ArrayResize(result, size1) != size1:
            return False
    for i in range(0, size1):
        result[i] = array1[i] | array2[i]
    return True

def MathBitwiseXor(array1, array2, result):
    size1 = ArraySize(array1)
    size2 = ArraySize(array2)
    if (size1 == 0 or size2 == 0) or size1 != size2:
        return False
    if ArraySize(result) < size1:
        if ArrayResize(result, size1) != size1:
            return False
    for i in range(0, size1):
        result[i] = array1[i] ^ array2[i]
    return True

def MathBitwiseShiftL_1(array, n, result):
    size = ArraySize(array)
    if size == 0:
        return False
    if ArraySize(result) < size:
        if ArrayResize(result, size) != size:
            return False
    for i in range(0, size):
        result[i] = _int(array[i] << n)
    return True

def MathBitwiseShiftL_2(array, n):
    size = ArraySize(array)
    if size == 0:
        return False
    for i in range(0, size):
        array[i] = _int(array[i] << n)
    return True

def MathBitwiseShiftR_1(array, n, result):
    size = ArraySize(array)
    if size == 0:
        return False
    if ArraySize(result) < size:
        if ArrayResize(result, size) != size:
            return False
    for i in range(0, size):
        result[i] = array[i] >> n
    return True

def MathBitwiseShiftR_2(array, n):
    size = ArraySize(array)
    if size == 0:
        return False
    for i in range(0, size):
        array[i] = array[i] >> n
    return True

def MathCumulativeSum_1(array, result):
    size = ArraySize(array)
    if size == 0:
        return False
    if ArraySize(result) < size:
        if ArrayResize(result, size) != size:
            return False
    sum_ = 0.0
    for i in range(0, size):
        if not MathIsValidNumber(array[i]):
            return False
        sum_ += array[i]
        result[i] = sum_
    return True

def MathCumulativeSum_2(array):
    size = ArraySize(array)
    if size == 0:
        return False
    sum_ = 0.0
    for i in range(0, size):
        if not MathIsValidNumber(array[i]):
            return False
        sum_ += array[i]
        array[i] = sum_
    return True

def MathCumulativeProduct_1(array, result):
    size = ArraySize(array)
    if size == 0:
        return False
    if ArraySize(result) < size:
        if ArrayResize(result, size) != size:
            return False
    product = 1.0
    for i in range(0, size):
        if not MathIsValidNumber(array[i]):
            return False
        product *= array[i]
        result[i] = product
    return True

def MathCumulativeProduct_2(array):
    size = ArraySize(array)
    if size == 0:
        return False
    product = 1.0
    for i in range(0, size):
        if not MathIsValidNumber(array[i]):
            return False
        product *= array[i]
        array[i] = product
    return True

def MathCumulativeMin_1(array, result):
    size = ArraySize(array)
    if size == 0:
        return False
    if ArraySize(result) < size:
        if ArrayResize(result, size) != size:
            return False
    min_ = QPOSINF
    for i in range(0, size):
        if (not MathIsValidNumber(array[i])) or (not MathIsValidNumber(min_)):
            min_ += array[i]
        else:
            min_ = MathMin(min_, array[i])
        result[i] = min_
    return True

def MathCumulativeMin_2(array):
    size = ArraySize(array)
    if size == 0:
        return False
    min_ = QPOSINF
    for i in range(0, size):
        if (not MathIsValidNumber(array[i])) or (not MathIsValidNumber(min_)):
            min_ += array[i]
        else:
            min_ = MathMin(min_, array[i])
        array[i] = min_
    return True

def MathCumulativeMax_1(array, result):
    size = ArraySize(array)
    if size == 0:
        return False
    if ArraySize(result) < size:
        if ArrayResize(result, size) != size:
            return False
    max_ = QNEGINF
    for i in range(0, size):
        if (not MathIsValidNumber(array[i])) or (not MathIsValidNumber(max_)):
            max_ += array[i]
        else:
            max_ = MathMax(max_, array[i])
        result[i] = max_
    return True

def MathCumulativeMax_2(array):
    size = ArraySize(array)
    if size == 0:
        return False
    max_ = QNEGINF
    for i in range(0, size):
        if (not MathIsValidNumber(array[i])) or (not MathIsValidNumber(max_)):
            max_ += array[i]
        else:
            max_ = MathMax(max_, array[i])
        array[i] = max_
    return True

def MathSin_u_1(array, result):
    size = ArraySize(array)
    if size == 0:
        return False
    if ArraySize(result) < size:
        if ArrayResize(result, size) != size:
            return False
    for i in range(0, size):
        result[i] = MathSin_u_2(array[i])
    return True

def MathSin_u_2(array):
    size = ArraySize(array)
    if size == 0:
        return False
    for i in range(0, size):
        array[i] = MathSin_u_2(array[i])
    return True

def MathCos_u_1(array, result):
    size = ArraySize(array)
    if size == 0:
        return False
    if ArraySize(result) < size:
        if ArrayResize(result, size) != size:
            return False
    for i in range(0, size):
        result[i] = MathCos_u_2(array[i])
    return True

def MathCos_u_2(array):
    size = ArraySize(array)
    if size == 0:
        return False
    for i in range(0, size):
        array[i] = MathCos_u_2(array[i])
    return True

def MathTan_u_1(array, result):
    size = ArraySize(array)
    if size == 0:
        return False
    if ArraySize(result) < size:
        if ArrayResize(result, size) != size:
            return False
    for i in range(0, size):
        result[i] = MathTan_u_2(array[i])
    return True

def MathTan_u_2(array):
    size = ArraySize(array)
    if size == 0:
        return False
    for i in range(0, size):
        array[i] = MathTan_u_2(array[i])
    return True

def MathArcsin_u_1(array, result):
    size = ArraySize(array)
    if size == 0:
        return False
    if ArraySize(result) < size:
        if ArrayResize(result, size) != size:
            return False
    for i in range(0, size):
        result[i] = MathArcsin_u_2(array[i])
    return True

def MathArcsin_u_2(array):
    size = ArraySize(array)
    if size == 0:
        return False
    for i in range(0, size):
        array[i] = MathArcsin_u_2(array[i])
    return True

def MathArccos_u_1(array, result):
    size = ArraySize(array)
    if size == 0:
        return False
    if ArraySize(result) < size:
        if ArrayResize(result, size) != size:
            return False
    for i in range(0, size):
        result[i] = MathArccos_u_2(array[i])
    return True

def MathArccos_u_2(array):
    size = ArraySize(array)
    if size == 0:
        return False
    for i in range(0, size):
        array[i] = MathArccos_u_2(array[i])
    return True

def MathArctan_u_1(array, result):
    size = ArraySize(array)
    if size == 0:
        return False
    if ArraySize(result) < size:
        if ArrayResize(result, size) != size:
            return False
    for i in range(0, size):
        result[i] = MathArctan_u_2(array[i])
    return True

def MathArctan_u_2(array):
    size = ArraySize(array)
    if size == 0:
        return False
    for i in range(0, size):
        array[i] = MathArctan_u_2(array[i])
    return True

def MathSinPi_1(array, result):
    size = ArraySize(array)
    if size == 0:
        return False
    if ArraySize(result) < size:
        if ArrayResize(result, size) != size:
            return False
    for i in range(0, size):
        result[i] = MathSin_u_2(M_PI * array[i])
    return True

def MathSinPi_2(array):
    size = ArraySize(array)
    if size == 0:
        return False
    for i in range(0, size):
        array[i] = MathSin_u_2(M_PI * array[i])
    return True

def MathCosPi_1(array, result):
    size = ArraySize(array)
    if size == 0:
        return False
    if ArraySize(result) < size:
        if ArrayResize(result, size) != size:
            return False
    for i in range(0, size):
        result[i] = MathCos_u_2(M_PI * array[i])
    return True

def MathCosPi_2(array):
    size = ArraySize(array)
    if size == 0:
        return False
    for i in range(0, size):
        array[i] = MathCos_u_2(M_PI * array[i])
    return True

def MathTanPi_1(array, result):
    size = ArraySize(array)
    if size == 0:
        return False
    if ArraySize(result) < size:
        if ArrayResize(result, size) != size:
            return False
    for i in range(0, size):
        result[i] = MathTan_u_2(M_PI * array[i])
    return True

def MathTanPi_2(array):
    size = ArraySize(array)
    if size == 0:
        return False
    for i in range(0, size):
        array[i] = MathTan_u_2(M_PI * array[i])
    return True

def MathAbs_u_1(array, result):
    size = ArraySize(array)
    if size == 0:
        return False
    if ArraySize(result) < size:
        if ArrayResize(result, size) != size:
            return False
    for i in range(0, size):
        result[i] = MathAbs_u_2(array[i])
    return True

def MathAbs_u_2(array):
    size = ArraySize(array)
    if size == 0:
        return False
    for i in range(0, size):
        array[i] = MathAbs_u_2(array[i])
    return True

def MathCeil_u_1(array, result):
    size = ArraySize(array)
    if size == 0:
        return False
    if ArraySize(result) < size:
        if ArrayResize(result, size) != size:
            return False
    for i in range(0, size):
        result[i] = MathCeil_u_2(array[i])
    return True

def MathCeil_u_2(array):
    size = ArraySize(array)
    if size == 0:
        return False
    for i in range(0, size):
        array[i] = MathCeil_u_2(array[i])
    return True

def MathFloor_u_1(array, result):
    size = ArraySize(array)
    if size == 0:
        return False
    if ArraySize(result) < size:
        if ArrayResize(result, size) != size:
            return False
    for i in range(0, size):
        result[i] = MathFloor_u_2(array[i])
    return True

def MathFloor_u_2(array):
    size = ArraySize(array)
    if size == 0:
        return False
    for i in range(0, size):
        array[i] = MathFloor_u_2(array[i])
    return True

def MathSqrt_u_1(array, result):
    size = ArraySize(array)
    if size == 0:
        return False
    if ArraySize(result) < size:
        if ArrayResize(result, size) != size:
            return False
    for i in range(0, size):
        result[i] = MathSqrt_u_2(array[i])
    return True

def MathSqrt_u_2(array):
    size = ArraySize(array)
    if size == 0:
        return False
    for i in range(0, size):
        array[i] = MathSqrt_u_2(array[i])
    return True

def MathExp_u_1(array, result):
    size = ArraySize(array)
    if size == 0:
        return False
    if ArraySize(result) < size:
        if ArrayResize(result, size) != size:
            return False
    for i in range(0, size):
        result[i] = MathExp_u_2(array[i])
    return True

def MathExp_u_2(array):
    size = ArraySize(array)
    if size == 0:
        return False
    for i in range(0, size):
        array[i] = MathExp_u_2(array[i])
    return True

def MathPow_u_1(array, power, result):
    size = ArraySize(array)
    if size == 0:
        return False
    if not MathIsValidNumber(power):
        return False
    if ArraySize(result) < size:
        if ArrayResize(result, size) != size:
            return False
    for i in range(0, size):
        result[i] = MathPow_u_2(array[i], power)
    return True

def MathPow_u_2(array, power):
    size = ArraySize(array)
    if size == 0:
        return False
    if not MathIsValidNumber(power):
        return False
    for i in range(0, size):
        array[i] = MathPow_u_2(array[i], power)
    return True

def MathLog_u_1(array, result):
    size = ArraySize(array)
    if size == 0:
        return False
    if ArraySize(result) < size:
        if ArrayResize(result, size) != size:
            return False
    for i in range(0, size):
        result[i] = MathLog_u_2(array[i])
    return True

def MathLog_u_2(array):
    size = ArraySize(array)
    if size == 0:
        return False
    for i in range(0, size):
        array[i] = MathLog_u_2(array[i])
    return True

def MathLog_u_3(array, base, result):
    size = ArraySize(array)
    if size == 0:
        return False
    if not MathIsValidNumber(base):
        return False
    if base == 1.0 or base <= 0.0:
        return False
    if ArraySize(result) < size:
        if ArrayResize(result, size) != size:
            return False
    factor = _fdiv(1.0, MathLog_u_2(base))
    for i in range(0, size):
        result[i] = MathLog_u_2(array[i]) * factor
    return True

def MathLog_u_4(array, base):
    size = ArraySize(array)
    if size == 0:
        return False
    if not MathIsValidNumber(base):
        return False
    if base == 1.0 or base <= 0.0:
        return False
    factor = _fdiv(1.0, MathLog_u_2(base))
    for i in range(0, size):
        array[i] = MathLog_u_2(array[i]) * factor
    return True

def MathLog2_u_1(array, result):
    size = ArraySize(array)
    if size == 0:
        return False
    if ArraySize(result) < size:
        if ArrayResize(result, size) != size:
            return False
    for i in range(0, size):
        result[i] = MathLog_u_2(array[i]) * _s_MathLog2_factor
    return True

def MathLog2_u_2(array):
    size = ArraySize(array)
    if size == 0:
        return False
    for i in range(0, size):
        array[i] = MathLog_u_2(array[i]) * _s_MathLog2_factor_
    return True

def MathLog10_u_1(array, result):
    size = ArraySize(array)
    if size == 0:
        return False
    if ArraySize(result) < size:
        if ArrayResize(result, size) != size:
            return False
    for i in range(0, size):
        result[i] = MathLog10_u_2(array[i])
    return True

def MathLog10_u_2(array):
    size = ArraySize(array)
    if size == 0:
        return False
    for i in range(0, size):
        array[i] = MathLog10_u_2(array[i])
    return True

def MathArctan2_u(y, x, result):
    size = ArraySize(x)
    if size == 0 or ArraySize(y) != size:
        return False
    if ArraySize(result) < size:
        if ArrayResize(result, size) != size:
            return False
    for i in range(0, size):
        result[i] = MathArctan2(y[i], x[i])
    return True

def MathDifference_1(array, lag, result):
    size = ArraySize(array) - lag
    if lag < 1 or size == 0:
        return False
    if ArraySize(result) < size:
        if ArrayResize(result, size) != size:
            return False
    for i in range(0, size):
        result[i] = array[i + lag] - array[i]
    if ArrayResize(result, size) != size:
        return False
    return True

def MathDifference_2(array, lag, result):
    size = ArraySize(array) - lag
    if lag < 1 or size == 0:
        return False
    if ArraySize(result) < size:
        if ArrayResize(result, size) != size:
            return False
    for i in range(0, size):
        result[i] = array[i + lag] - array[i]
    if ArrayResize(result, size) != size:
        return False
    return True

def MathDifference_3(array, lag, differences, result):
    size = ArraySize(array)
    if (size == 0 or differences < 0) or (lag * differences) >= size:
        return False
    if ArrayCopy(result, array, 0, 0, WHOLE_ARRAY) != size:
        return False
    for i in range(0, differences):
        if not MathDifference_1(result, lag, result):
            return False
    return True

def MathDifference_4(array, lag, differences, result):
    size = ArraySize(array)
    if (size == 0 or differences < 0) or (lag * differences) >= size:
        return False
    if ArrayCopy(result, array, 0, 0, WHOLE_ARRAY) != size:
        return False
    for i in range(0, differences):
        if not MathDifference_2(result, lag, result):
            return False
    return True

def MathSample_1(array, count, result):
    size = ArraySize(array)
    if size == 0:
        return False
    if ArraySize(result) < count:
        if ArrayResize(result, count) != count:
            return False
    for i in range(0, count):
        ind = _int(_idiv(_ulong(size) * MathRand(), 32768))
        result[i] = array[ind]
    return True

def MathSample_2(array, count, result):
    size = ArraySize(array)
    if size == 0:
        return False
    if ArraySize(result) < count:
        if ArrayResize(result, count) != count:
            return False
    for i in range(0, count):
        ind = _int(_idiv(_ulong(size) * MathRand(), 32768))
        result[i] = array[ind]
    return True

def MathSample_3(array, count, replace, result):
    if replace:
        return MathSample_1(array, count, result)
    size = ArraySize(array)
    if size == 0 or count > size:
        return False
    if ArraySize(result) < count:
        if ArrayResize(result, count) != count:
            return False
    indices = Arr(0, 0)
    if not MathSequenceByCount_2(0, size - 1, size, indices):
        return False
    for i in range(0, count):
        j = i + _int(_idiv(_ulong(size - i) * MathRand(), 32768))
        if j != i:
            t = indices[i]
            indices[i] = indices[j]
            indices[j] = t
    for i in range(0, count):
        result[i] = array[indices[i]]
    return True

def MathSample_4(array, count, replace, result):
    if replace:
        return MathSample_2(array, count, result)
    size = ArraySize(array)
    if size == 0 or count > size:
        return False
    if ArraySize(result) < count:
        if ArrayResize(result, count) != count:
            return False
    indices = Arr(0, 0)
    if not MathSequenceByCount_2(0, size - 1, size, indices):
        return False
    for i in range(0, count):
        j = i + _int(_idiv(_ulong(size - i) * MathRand(), 32768))
        if j != i:
            t = indices[i]
            indices[i] = indices[j]
            indices[j] = t
    for i in range(0, count):
        result[i] = array[indices[i]]
    return True

def MathSample_5(array, probabilities, count, result):
    size = ArraySize(array)
    if size == 0 or size != ArraySize(probabilities):
        return False
    if count <= 0:
        return False
    prob = Arr(0, 0.0)
    if ArrayCopy(prob, probabilities, 0, 0, WHOLE_ARRAY) != size:
        return False
    sum_ = 0.0
    for i in range(0, size):
        sum_ += prob[i]
    if sum_ == 0.0:
        return False
    sum_ = _fdiv(1.0, sum_)
    for i in range(0, size):
        prob[i] *= sum_
    indices = Arr(0, 0)
    if ArrayResize(indices, size) != size:
        return False
    for i in range(0, size):
        indices[i] = i
    MathQuickSortDescending(prob, indices, 0, size - 1)
    for i in range(1, size):
        prob[i] += prob[i - 1]
    if ArraySize(result) < count:
        if ArrayResize(result, count) != count:
            return False
    for i in range(0, count):
        prb = MathRand() / 32767.0
        for k in range(0, size):
            if prb <= prob[k]:
                result[i] = array[indices[k]]
                break
    return True

def MathSample_6(array, probabilities, count, result):
    size = ArraySize(array)
    if size == 0 or size != ArraySize(probabilities):
        return False
    if count <= 0:
        return False
    prob = Arr(0, 0.0)
    if ArrayCopy(prob, probabilities, 0, 0, WHOLE_ARRAY) != size:
        return False
    sum_ = 0.0
    for i in range(0, size):
        sum_ += prob[i]
    if sum_ == 0.0:
        return False
    sum_ = _fdiv(1.0, sum_)
    for i in range(0, size):
        prob[i] *= sum_
    indices = Arr(0, 0)
    if ArrayResize(indices, size) != size:
        return False
    for i in range(0, size):
        indices[i] = i
    MathQuickSortDescending(prob, indices, 0, size - 1)
    for i in range(1, size):
        prob[i] += prob[i - 1]
    if ArraySize(result) < count:
        if ArrayResize(result, count) != count:
            return False
    for i in range(0, count):
        prb = MathRand() / 32767.0
        for k in range(0, size):
            if prb <= prob[k]:
                result[i] = array[indices[k]]
                break
    return True

def MathSample_7(array, probabilities, count, replace, result):
    if replace:
        return MathSample_5(array, probabilities, count, result)
    size = ArraySize(array)
    if size == 0 or size != ArraySize(probabilities):
        return False
    if count <= 0 or count > size:
        return False
    prob = Arr(0, 0.0)
    if ArrayCopy(prob, probabilities, 0, 0, WHOLE_ARRAY) != size:
        return False
    sum_ = 0.0
    for i in range(0, size):
        sum_ += prob[i]
    if sum_ == 0.0:
        return False
    sum_ = _fdiv(1.0, sum_)
    for i in range(0, size):
        prob[i] *= sum_
    indices = Arr(0, 0)
    if ArrayResize(indices, size) != size:
        return False
    for i in range(0, size):
        indices[i] = i
    MathQuickSortDescending(prob, indices, 0, size - 1)
    for i in range(1, size):
        prob[i] += prob[i - 1]
    taken_values = Arr(0, False)
    if ArrayResize(taken_values, size) != size:
        return False
    ArrayFill(taken_values, 0, size, False)
    if ArraySize(result) < count:
        if ArrayResize(result, count) != count:
            return False
    for i in range(0, count):
        prb = MathRand() / 32767.0
        for k in range(0, size):
            ind = indices[k]
            if prb <= prob[k] and taken_values[ind] == False:
                result[i] = array[ind]
                taken_values[ind] = True
                break
    return True

def MathSample_8(array, probabilities, count, replace, result):
    if replace:
        return MathSample_6(array, probabilities, count, result)
    size = ArraySize(array)
    if size == 0 or size != ArraySize(probabilities):
        return False
    if count <= 0 or count > size:
        return False
    prob = Arr(0, 0.0)
    if ArrayCopy(prob, probabilities, 0, 0, WHOLE_ARRAY) != size:
        return False
    sum_ = 0.0
    for i in range(0, size):
        sum_ += prob[i]
    if sum_ == 0.0:
        return False
    sum_ = _fdiv(1.0, sum_)
    for i in range(0, size):
        prob[i] *= sum_
    indices = Arr(0, 0)
    if ArrayResize(indices, size) != size:
        return False
    for i in range(0, size):
        indices[i] = i
    MathQuickSortDescending(prob, indices, 0, size - 1)
    for i in range(1, size):
        prob[i] += prob[i - 1]
    taken_values = Arr(0, False)
    if ArrayResize(taken_values, size) != size:
        return False
    ArrayFill(taken_values, 0, size, False)
    if ArraySize(result) < count:
        if ArrayResize(result, count) != count:
            return False
    for i in range(0, count):
        prb = MathRand() / 32767.0
        for k in range(0, size):
            ind = indices[k]
            if prb <= prob[k] and taken_values[ind] == False:
                result[i] = array[ind]
                taken_values[ind] = True
                break
    return True

def MathTukeySummary(array, removeNAN, minimum, lower_hinge, median, upper_hinge, maximum):
    minimum.v = QNaN
    lower_hinge.v = QNaN
    median.v = QNaN
    upper_hinge.v = QNaN
    maximum.v = QNaN
    size = ArraySize(array)
    if size == 0:
        return False
    data = Arr(0, 0.0)
    if ArrayResize(data, size) != size:
        return False
    actual_values = 0
    if removeNAN == True:
        for i in range(0, size):
            if MathIsValidNumber(array[i]):
                data[actual_values] = array[i]
                actual_values += 1
        ArrayResize(data, actual_values)
    else:
        for i in range(0, size):
            if not MathIsValidNumber(array[i]):
                return False
        if ArrayCopy(data, array, 0, 0, WHOLE_ARRAY) != size:
            return False
    ArraySort(data)
    n = ArraySize(data)
    if n == 0:
        return False
    n4 = MathFloor_u_2((n + 3) * 0.5) * 0.5
    ind = Arr(5, 0.0, dyn=False)
    ind[0] = 0.0
    ind[1] = n4 - 1
    ind[2] = (0.5 * (n + 1)) - 1
    ind[3] = n - n4
    ind[4] = n - 1
    minimum.v = 0.5 * (data[MathFloor_u_2(ind[0])] + data[MathCeil_u_2(ind[0])])
    lower_hinge.v = 0.5 * (data[MathFloor_u_2(ind[1])] + data[MathCeil_u_2(ind[1])])
    median.v = 0.5 * (data[MathFloor_u_2(ind[2])] + data[MathCeil_u_2(ind[2])])
    upper_hinge.v = 0.5 * (data[MathFloor_u_2(ind[3])] + data[MathCeil_u_2(ind[3])])
    maximum.v = 0.5 * (data[MathFloor_u_2(ind[4])] + data[MathCeil_u_2(ind[4])])
    return True

def MathRange(array, min_, max_):
    size = ArraySize(array)
    if size == 0:
        return False
    min_.v = array[0]
    max_.v = array[0]
    for i in range(1, size):
        value = array[i]
        min_.v = MathMin(min_.v, value)
        max_.v = MathMax(max_.v, value)
    return True

def MathMin_u(array):
    size = ArraySize(array)
    if size == 0:
        return QNaN
    min_value = array[0]
    for i in range(1, size):
        min_value = MathMin(min_value, array[i])
    return min_value

def MathMax_u(array):
    size = ArraySize(array)
    if size == 0:
        return QNaN
    max_value = array[0]
    for i in range(1, size):
        max_value = MathMax(max_value, array[i])
    return max_value

def MathSum(array):
    size = ArraySize(array)
    if size == 0:
        return QNaN
    sum_ = 0.0
    for i in range(0, size):
        sum_ += array[i]
    return sum_

def MathProduct(array):
    size = ArraySize(array)
    if size == 0:
        return QNaN
    product = 1.0
    for i in range(0, size):
        product *= array[i]
    return product

def MathStandardDeviation(array):
    size = ArraySize(array)
    if size <= 1:
        return QNaN
    mean = 0.0
    for i in range(0, size):
        mean += array[i]
    mean = _fdiv(mean, size)
    sdev = 0.0
    for i in range(0, size):
        sdev += MathPow_u_2(array[i] - mean, 2.0)
    return MathSqrt_u_2(_fdiv(sdev, size - 1))

def MathAverageDeviation(array):
    size = ArraySize(array)
    if size <= 1:
        return QNaN
    mean = 0.0
    for i in range(0, size):
        mean += array[i]
    mean = _fdiv(mean, size)
    adev = 0.0
    for i in range(0, size):
        adev += MathAbs_u_2(array[i] - mean)
    adev = _fdiv(adev, size)
    return adev

def MathMedian(array):
    size = ArraySize(array)
    if size == 0:
        return QNaN
    sorted_values = Arr(0, 0.0)
    if ArrayCopy(sorted_values, array, 0, 0, WHOLE_ARRAY) != size:
        return QNaN
    ArraySort(sorted_values)
    if _imod(size, 2) == 1:
        return sorted_values[_idiv(size, 2)]
    return 0.5 * (sorted_values[_idiv(size - 1, 2)] + sorted_values[_idiv(size + 1, 2)])

def MathMean(array):
    size = ArraySize(array)
    if size < 1:
        return QNaN
    mean = 0.0
    for i in range(0, size):
        mean += array[i]
    mean = _fdiv(mean, size)
    return mean

def MathVariance(array):
    size = ArraySize(array)
    if size < 2:
        return QNaN
    mean = 0.0
    for i in range(0, size):
        mean += array[i]
    mean = _fdiv(mean, size)
    variance = 0.0
    for i in range(0, size):
        variance += MathPow_u_2(array[i] - mean, 2.0)
    variance = _fdiv(variance, size - 1)
    return variance

def MathSkewness(array):
    size = ArraySize(array)
    if size < 3:
        return QNaN
    mean = 0.0
    for i in range(0, size):
        mean += array[i]
    mean = _fdiv(mean, size)
    variance = 0.0
    skewness = 0.0
    for i in range(0, size):
        sqr_dev = MathPow_u_2(array[i] - mean, 2.0)
        skewness += sqr_dev * (array[i] - mean)
        variance += sqr_dev
    variance = _fdiv(variance, size - 1)
    v3 = MathPow_u_2(MathSqrt_u_2(variance), 3.0)
    if v3 != 0:
        skewness = _fdiv(skewness, size * v3)
        return skewness
    else:
        return QNaN

def MathKurtosis(array):
    size = ArraySize(array)
    if size < 4:
        return QNaN
    mean = 0.0
    for i in range(0, size):
        mean += array[i]
    mean = _fdiv(mean, size)
    variance = 0.0
    kurtosis = 0.0
    for i in range(0, size):
        sqr_dev = MathPow_u_2(array[i] - mean, 2.0)
        variance += sqr_dev
        kurtosis += sqr_dev * sqr_dev
    variance = _fdiv(variance, size - 1)
    v4 = MathPow_u_2(MathSqrt_u_2(variance), 4.0)
    if v4 != 0:
        kurtosis = _fdiv(kurtosis, size * v4)
        kurtosis -= 3
        return kurtosis
    else:
        return QNaN

def MathLog1p_u_1(array, result):
    size = ArraySize(array)
    if size == 0:
        return False
    if ArraySize(result) < size:
        if ArrayResize(result, size) != size:
            return False
    for i in range(0, size):
        result[i] = MathLog1p_u_2(array[i])
    return True

def MathLog1p_u_2(array):
    size = ArraySize(array)
    if size == 0:
        return False
    for i in range(0, size):
        array[i] = MathLog1p_u_2(array[i])
    return True

def MathExpm1_u_1(array, result):
    size = ArraySize(array)
    if size == 0:
        return False
    if ArraySize(result) < size:
        if ArrayResize(result, size) != size:
            return False
    for i in range(0, size):
        result[i] = MathExpm1_u_2(array[i])
    return True

def MathExpm1_u_2(array):
    size = ArraySize(array)
    if size == 0:
        return False
    for i in range(0, size):
        array[i] = MathExpm1_u_2(array[i])
    return True

def MathSinh_u_1(array, result):
    size = ArraySize(array)
    if size == 0:
        return False
    if ArraySize(result) < size:
        if ArrayResize(result, size) != size:
            return False
    for i in range(0, size):
        result[i] = MathSinh_u_2(array[i])
    return True

def MathSinh_u_2(array):
    size = ArraySize(array)
    if size == 0:
        return False
    for i in range(0, size):
        array[i] = MathSinh_u_2(array[i])
    return True

def MathCosh_u_1(array, result):
    size = ArraySize(array)
    if size == 0:
        return False
    if ArraySize(result) < size:
        if ArrayResize(result, size) != size:
            return False
    for i in range(0, size):
        result[i] = MathCosh_u_2(array[i])
    return True

def MathCosh_u_2(array):
    size = ArraySize(array)
    if size == 0:
        return False
    for i in range(0, size):
        array[i] = MathCosh_u_2(array[i])
    return True

def MathTanh_u_1(array, result):
    size = ArraySize(array)
    if size == 0:
        return False
    if ArraySize(result) < size:
        if ArrayResize(result, size) != size:
            return False
    for i in range(0, size):
        result[i] = MathTanh_u_2(array[i])
    return True

def MathTanh_u_2(array):
    size = ArraySize(array)
    if size == 0:
        return False
    for i in range(0, size):
        array[i] = MathTanh_u_2(array[i])
    return True

def MathArcsinh_u_1(array, result):
    size = ArraySize(array)
    if size == 0:
        return False
    if ArraySize(result) < size:
        if ArrayResize(result, size) != size:
            return False
    for i in range(0, size):
        result[i] = MathArcsinh_u_2(array[i])
    return True

def MathArcsinh_u_2(array):
    size = ArraySize(array)
    if size == 0:
        return False
    for i in range(0, size):
        array[i] = MathArcsinh_u_2(array[i])
    return True

def MathArccosh_u_1(array, result):
    size = ArraySize(array)
    if size == 0:
        return False
    if ArraySize(result) < size:
        if ArrayResize(result, size) != size:
            return False
    for i in range(0, size):
        result[i] = MathArccosh_u_2(array[i])
    return True

def MathArccosh_u_2(array):
    size = ArraySize(array)
    if size == 0:
        return False
    for i in range(0, size):
        array[i] = MathArccosh_u_2(array[i])
    return True

def MathArctanh_u_1(array, result):
    size = ArraySize(array)
    if size == 0:
        return False
    if ArraySize(result) < size:
        if ArrayResize(result, size) != size:
            return False
    for i in range(0, size):
        result[i] = MathArctanh_u_2(array[i])
    return True

def MathArctanh_u_2(array):
    size = ArraySize(array)
    if size == 0:
        return False
    for i in range(0, size):
        array[i] = MathArctanh_u_2(array[i])
    return True

def MathSignif_1(x, digits):
    if x == 0:
        return x
    dig = digits
    if dig > 30:
        return x
    if dig < 1:
        dig = 1
    sign = 1.0
    xx = x
    if xx < 0.0:
        sign = -sign
        xx = -xx
    l10 = MathLog10_u_2(xx)
    e10 = dig - 1 - MathFloor_u_2(l10)
    value = 0.0
    pwr10 = 0.0
    if e10 > 0:
        pwr10 = MathPow_u_2(10, e10)
        value = _fdiv(MathFloor_u_2((xx * pwr10) + 0.5), pwr10)
    else:
        pwr10 = MathPow_u_2(10, -e10)
        value = MathFloor_u_2(_fdiv(xx, pwr10) + 0.5) * pwr10
    return sign * value

def MathSignif_2(array, digits, result):
    size = ArraySize(array)
    if size == 0:
        return False
    if ArraySize(result) < size:
        if ArrayResize(result, size) != size:
            return False
    for i in range(0, size):
        result[i] = MathSignif_1(array[i], digits)
    return True

def MathSignif_3(array, digits):
    size = ArraySize(array)
    if size == 0:
        return False
    for i in range(0, size):
        array[i] = MathSignif_1(array[i], digits)
    return True

def MathRank_1(array, rank):
    size = ArraySize(array)
    if size < 1:
        return False
    if size == 1:
        if ArrayResize(rank, size) != size:
            return False
        rank[0] = 1.0
        return True
    values = Arr(0, 0.0)
    indices = Arr(0, 0)
    if ArrayCopy(values, array, 0, 0, WHOLE_ARRAY) != size:
        return False
    if not MathSequenceByCount_2(0, size, size, indices):
        return False
    if ArrayResize(rank, size) != size:
        return False
    i = 0
    j = 0
    k = 0
    t = 0
    tmpi = 0
    tmp = 0.0
    if size != 1:
        i = 2
        while True:
            t = i
            while t != 1:
                k = _idiv(t, 2)
                if values[k - 1] >= values[t - 1]:
                    t = 1
                else:
                    tmp = values[k - 1]
                    values[k - 1] = values[t - 1]
                    values[t - 1] = tmp
                    tmpi = indices[k - 1]
                    indices[k - 1] = indices[t - 1]
                    indices[t - 1] = tmpi
                    t = k
            i = i + 1
            if not (i <= size):
                break
        i = size - 1
        while True:
            tmp = values[i]
            values[i] = values[0]
            values[0] = tmp
            tmpi = indices[i]
            indices[i] = indices[0]
            indices[0] = tmpi
            t = 1
            while t != 0:
                k = 2 * t
                if k > i:
                    t = 0
                else:
                    if k < i:
                        if values[k] > values[k - 1]:
                            k += 1
                    if values[t - 1] >= values[k - 1]:
                        t = 0
                    else:
                        tmp = values[k - 1]
                        values[k - 1] = values[t - 1]
                        values[t - 1] = tmp
                        tmpi = indices[k - 1]
                        indices[k - 1] = indices[t - 1]
                        indices[t - 1] = tmpi
                        t = k
            i = i - 1
            if not (i >= 1):
                break
    i = 0
    while i < size:
        j = i + 1
        while j < size:
            if values[j] != values[i]:
                break
            j = j + 1
        k = i
        for k in range(k, j):
            values[k] = 1 + ((i + j - 1) * 0.5)
        else:
            k = _range_end(k, j, 1)
        i = j
    i = 0
    for i in range(i, size):
        rank[indices[i]] = values[i]
    else:
        i = _range_end(i, size, 1)
    return True

def MathRank_2(array, rank):
    size = ArraySize(array)
    if size < 1:
        return False
    if size == 1:
        if ArrayResize(rank, size) != size:
            return False
        rank[0] = 1.0
        return True
    values = Arr(0, 0.0)
    indices = Arr(0, 0)
    if ArrayResize(values, size) != size:
        return False
    for i in range(0, size):
        values[i] = array[i]
    if not MathSequenceByCount_2(0, size, size, indices):
        return False
    if ArrayResize(rank, size) != size:
        return False
    i = 0
    j = 0
    k = 0
    t = 0
    tmpi = 0
    tmp = 0.0
    if size != 1:
        i = 2
        while True:
            t = i
            while t != 1:
                k = _idiv(t, 2)
                if values[k - 1] >= values[t - 1]:
                    t = 1
                else:
                    tmp = values[k - 1]
                    values[k - 1] = values[t - 1]
                    values[t - 1] = tmp
                    tmpi = indices[k - 1]
                    indices[k - 1] = indices[t - 1]
                    indices[t - 1] = tmpi
                    t = k
            i = i + 1
            if not (i <= size):
                break
        i = size - 1
        while True:
            tmp = values[i]
            values[i] = values[0]
            values[0] = tmp
            tmpi = indices[i]
            indices[i] = indices[0]
            indices[0] = tmpi
            t = 1
            while t != 0:
                k = 2 * t
                if k > i:
                    t = 0
                else:
                    if k < i:
                        if values[k] > values[k - 1]:
                            k += 1
                    if values[t - 1] >= values[k - 1]:
                        t = 0
                    else:
                        tmp = values[k - 1]
                        values[k - 1] = values[t - 1]
                        values[t - 1] = tmp
                        tmpi = indices[k - 1]
                        indices[k - 1] = indices[t - 1]
                        indices[t - 1] = tmpi
                        t = k
            i = i - 1
            if not (i >= 1):
                break
    i = 0
    while i < size:
        j = i + 1
        while j < size:
            if values[j] != values[i]:
                break
            j = j + 1
        k = i
        for k in range(k, j):
            values[k] = 1 + ((i + j - 1) * 0.5)
        else:
            k = _range_end(k, j, 1)
        i = j
    i = 0
    for i in range(i, size):
        rank[indices[i]] = values[i]
    else:
        i = _range_end(i, size, 1)
    return True

def MathCorrelationPearson_1(array1, array2, r):
    r.v = QNaN
    size = ArraySize(array1)
    if size <= 1 or ArraySize(array2) != size:
        return False
    xmean = 0.0
    ymean = 0.0
    v = _fdiv(1.0, float(size))
    x0 = array1[0]
    y0 = array2[0]
    s = 0.0
    xv = 0.0
    yv = 0.0
    t1 = 0.0
    t2 = 0.0
    samex = True
    samey = True
    for i in range(0, size):
        s = array1[i]
        samex = samex and s == x0
        xmean += s * v
        s = array2[i]
        samey = samey and s == y0
        ymean += s * v
    if samex or samey:
        return False
    s = 0.0
    for i in range(0, size):
        t1 = array1[i] - xmean
        t2 = array2[i] - ymean
        xv += t1 * t1
        yv += t2 * t2
        s += t1 * t2
    if xv == 0 or yv == 0:
        return False
    r.v = _fdiv(s, MathSqrt_u_2(xv * yv))
    return True

def MathCorrelationPearson_2(array1, array2, r):
    r.v = QNaN
    size = ArraySize(array1)
    if size <= 1 or ArraySize(array2) != size:
        return False
    xmean = 0.0
    ymean = 0.0
    v = _fdiv(1.0, float(size))
    x0 = array1[0]
    y0 = array2[0]
    s = 0.0
    xv = 0.0
    yv = 0.0
    t1 = 0.0
    t2 = 0.0
    samex = True
    samey = True
    for i in range(0, size):
        s = array1[i]
        samex = samex and s == x0
        xmean += s * v
        s = array2[i]
        samey = samey and s == y0
        ymean += s * v
    if samex or samey:
        return False
    s = 0.0
    for i in range(0, size):
        t1 = array1[i] - xmean
        t2 = array2[i] - ymean
        xv += t1 * t1
        yv += t2 * t2
        s += t1 * t2
    if xv == 0 or yv == 0:
        return False
    r.v = _fdiv(s, MathSqrt_u_2(xv * yv))
    return True

def MathCorrelationSpearman_1(array1, array2, r):
    r.v = QNaN
    size = ArraySize(array1)
    if size < 1 or ArraySize(array2) != size:
        return False
    rank_x = Arr(0, 0.0)
    rank_y = Arr(0, 0.0)
    if not MathRank_1(array1, rank_x):
        return False
    if not MathRank_1(array2, rank_y):
        return False
    return MathCorrelationPearson_1(rank_x, rank_y, r)

def MathCorrelationSpearman_2(array1, array2, r):
    r.v = QNaN
    size = ArraySize(array1)
    if size < 1 or ArraySize(array2) != size:
        return False
    rank_x = Arr(0, 0.0)
    rank_y = Arr(0, 0.0)
    if not MathRank_2(array1, rank_x):
        return False
    if not MathRank_2(array2, rank_y):
        return False
    return MathCorrelationPearson_1(rank_x, rank_y, r)

def MathCorrelationKendall_1(array1, array2, tau):
    tau.v = QNaN
    size = ArraySize(array1)
    if size == 0 or ArraySize(array2) != size:
        return False
    cnt1 = 0
    cnt2 = 0
    cnt = 0
    for i in range(0, size):
        for j in range(i + 1, size):
            delta1 = array1[i] - array1[j]
            delta2 = array2[i] - array2[j]
            delta = delta1 * delta2
            if delta == 0:
                if delta1 != 0:
                    cnt1 += 1
                if delta2 != 0:
                    cnt2 += 1
            else:
                cnt1 += 1
                cnt2 += 1
                if delta > 0.0:
                    cnt += 1
                else:
                    cnt -= 1
    den = cnt1 * cnt2
    if den == 0:
        return False
    tau.v = _idiv(cnt, MathSqrt_u_2(den))
    return True

def MathCorrelationKendall_2(array1, array2, tau):
    tau.v = QNaN
    size = ArraySize(array1)
    if size == 0 or ArraySize(array2) != size:
        return False
    cnt1 = 0
    cnt2 = 0
    cnt = 0
    for i in range(0, size):
        for j in range(i + 1, size):
            delta1 = array1[i] - array1[j]
            delta2 = array2[i] - array2[j]
            delta = delta1 * delta2
            if delta == 0:
                if delta1 != 0:
                    cnt1 += 1
                if delta2 != 0:
                    cnt2 += 1
            else:
                cnt1 += 1
                cnt2 += 1
                if delta > 0.0:
                    cnt += 1
                else:
                    cnt -= 1
    den = cnt1 * cnt2
    if den == 0:
        return False
    tau.v = _idiv(cnt, MathSqrt_u_2(den))
    return True

def MathQuantile(array, probs, quantile):
    size = ArraySize(array)
    size_p = ArraySize(probs)
    if size == 0 or size_p == 0:
        return False
    for i in range(0, size_p):
        if not MathIsValidNumber(probs[i]):
            return False
        if probs[i] < 0.0 or probs[i] > 1.0:
            return False
    x_values = Arr(0, 0.0)
    if ArrayCopy(x_values, array, 0, 0, WHOLE_ARRAY) != size:
        return False
    if ArraySize(quantile) < size_p:
        if ArrayResize(quantile, size_p) != size_p:
            return False
    ind = Arr(0, 0.0)
    lo = Arr(0, 0)
    hi = Arr(0, 0)
    ArrayResize(ind, size_p)
    ArrayResize(lo, size_p)
    ArrayResize(hi, size_p)
    for i in range(0, size_p):
        ind[i] = (size - 1) * probs[i]
        lo[i] = MathFloor_u_2(ind[i])
        hi[i] = MathCeil_u_2(ind[i])
    indices = Arr(0, 0)
    MathSequenceByCount_2(0, size - 1, size, indices)
    MathQuickSort(x_values, indices, 0, size - 1, 1)
    for i in range(0, size_p):
        quantile[i] = x_values[lo[i]]
        if ind[i] > lo[i]:
            gamma = ind[i] - lo[i]
            quantile[i] = ((1.0 - gamma) * quantile[i]) + (gamma * x_values[hi[i]])
    return True

def MathProbabilityDensityEmpirical(array, count, x, pdf):
    if count <= 1:
        return False
    size = ArraySize(array)
    if size == 0:
        return False
    for i in range(0, size):
        if not MathIsValidNumber(array[i]):
            return False
    if ArraySize(x) < count:
        if ArrayResize(x, count) != count:
            return False
    if ArraySize(pdf) < count:
        if ArrayResize(pdf, count) != count:
            return False
    minv = array[0]
    maxv = array[0]
    for i in range(1, size):
        minv = MathMin(minv, array[i])
        maxv = MathMax(maxv, array[i])
    range_ = maxv - minv
    if range_ == 0:
        return False
    for i in range(0, count):
        x[i] = minv + _fdiv(i * range_, count - 1)
        pdf[i] = 0.0
    for i in range(0, size):
        v = _fdiv(array[i] - minv, range_)
        ind = _int(v * (count - 1))
        pdf[ind] += 1
    dx = _fdiv(range_, count)
    sum_ = 0.0
    for i in range(0, count):
        sum_ += pdf[i] * dx
    if sum_ == 0:
        return False
    coef = _fdiv(1.0, sum_)
    for i in range(0, count):
        pdf[i] *= coef
    return True

def MathCumulativeDistributionEmpirical(array, count, x, cdf):
    if count <= 1:
        return False
    size = ArraySize(array)
    if size == 0:
        return False
    for i in range(0, size):
        if not MathIsValidNumber(array[i]):
            return False
    if ArraySize(x) < count:
        if ArrayResize(x, count) != count:
            return False
    if ArraySize(cdf) < count:
        if ArrayResize(cdf, count) != count:
            return False
    minv = array[0]
    maxv = array[0]
    for i in range(1, size):
        minv = MathMin(minv, array[i])
        maxv = MathMax(maxv, array[i])
    range_ = maxv - minv
    if range_ == 0:
        return False
    pdf = Arr(0, 0.0)
    if ArrayResize(pdf, count) != count:
        return False
    for i in range(0, count):
        x[i] = minv + _fdiv(i * range_, count - 1)
        pdf[i] = 0.0
    for i in range(0, size):
        v = _fdiv(array[i] - minv, range_)
        ind = _int(v * (count - 1))
        pdf[ind] += 1
    dx = _fdiv(range_, count)
    sum_ = 0.0
    for i in range(0, count):
        sum_ += pdf[i] * dx
    if sum_ == 0:
        return False
    coef = _fdiv(1.0, sum_)
    for i in range(0, count):
        pdf[i] *= coef
    sum_ = 0.0
    for i in range(0, count):
        sum_ += pdf[i] * dx
        cdf[i] = sum_
    return True

def MathCheckProbabilityInput(probability, tail, log_mode, prob, error_code):
    if not MathIsValidNumber(probability):
        if not (log_mode and probability == QNEGINF):
            error_code.v = 1
            return False
    prob.v = TailLogProbability(probability, tail, log_mode)
    if not MathIsValidNumber(prob.v):
        error_code.v = 1
        return False
    if prob.v < 0.0 or prob.v > 1.0:
        error_code.v = 2
        return False
    error_code.v = 0
    return True

def MathBisectionConverged(lo, hi, abs_tol, rel_tol):
    mid = 0.5 * (lo + hi)
    width = hi - lo
    scale = MathMax(1.0, MathAbs_u_2(mid))
    return width <= abs_tol or width <= (rel_tol * scale)

def OnInit():
    global splittedPairsNumber
    sep = ','
    u_sep = 0
    u_sep = StringGetCharacter(sep, 0)
    splittedPairsNumber = StringSplit(SymbolsList, u_sep, splittedPairs)
    ArrayResize(allspreads, splittedPairsNumber)
    smbls = ""
    if splittedPairsNumber > 0:
        i = 0
        while i < splittedPairsNumber:
            getSymbolByName(splittedPairs[i])
            SetIndexBuffer(i, allspreads[i].zscore, INDICATOR_DATA)
            ArraySetAsSeries(allspreads[i].spreadBuffer, True)
            ArrayResize(allspreads[i].spreadBuffer, learning_depth)
            ArrayResize(allspreads[i].pricesBuffer, learning_depth)
            ArraySetAsSeries(allspreads[i].pricesBuffer, True)
            ArrayInitialize(allspreads[i].pricesBuffer, 0)
            ArrayResize(allspreads[i].weights, splittedPairsNumber)
            ArraySetAsSeries(allspreads[i].zscore, True)
            ArrayInitialize(allspreads[i].zscore, 0)
            allspreads[i].symbol = splittedPairs[i]
            PlotIndexSetString(i, PLOT_LABEL, allspreads[i].symbol)
            PlotIndexSetInteger(i, PLOT_LINE_WIDTH, 2)
            smbls += splittedPairs[i] + ', '
            i += 1
    SetIndexBuffer(splittedPairsNumber, zscore, INDICATOR_DATA)
    PlotIndexSetInteger(splittedPairsNumber, PLOT_DRAW_TYPE, DRAW_HISTOGRAM)
    PlotIndexSetInteger(splittedPairsNumber, PLOT_LINE_STYLE, STYLE_DOT)
    PlotIndexSetInteger(splittedPairsNumber, PLOT_LINE_WIDTH, 1)
    PlotIndexSetInteger(splittedPairsNumber, PLOT_LINE_COLOR, clrSilver)
    PlotIndexSetString(splittedPairsNumber, PLOT_LABEL, 'Z-SCORE')
    LRmatrix.Resize(learning_depth, splittedPairsNumber)
    ArrayResize(mainsynthetic, learning_depth)
    ArraySetAsSeries(mainsynthetic, True)
    ArrayResize(zscore, learning_depth)
    ArraySetAsSeries(zscore, True)
    ArrayInitialize(mainsynthetic, 0)
    ArrayInitialize(zscore, 0)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Z-score: ' + smbls)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    IndicatorSetInteger(INDICATOR_LEVELS, 6)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, 1)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, -1)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 3, -2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 4, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 5, -3)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, begin, price):
    global second_call
    first_call = prev_calculated == 0
    if first_call or second_call:
        if fillPricesToBuffers(learning_depth):
            fillLRmatrixes()
            calculateSpreads(learning_depth)
            calculateMainSynthetic(learning_depth)
            second_call = False
        else:
            second_call = True
    if isNewBar():
        if fillPricesToBuffers(learning_depth):
            fillLRmatrixes()
            calculateSpreads(learning_depth)
            calculateMainSynthetic(learning_depth)
            second_call = False
        else:
            second_call = True
    if not second_call:
        fillPricesToBuffers(1)
        calculateSpreads(1)
        calculateMainSynthetic(learning_depth)
    return rates_total

def fillPricesToBuffers(depth):
    for l in range(0, ArraySize(allspreads)):
        copied = CopyClose(allspreads[l].symbol, PERIOD_CURRENT, 0, learning_depth, allspreads[l].pricesBuffer)
        Comment('')
        if copied != learning_depth:
            Comment('Update ' + allspreads[l].symbol + ', waiting for quotes to be downloaded!')
            return False
    return True

def fillLRmatrixes():
    k = 0
    while k < ArraySize(allspreads):
        n = 0
        l = 0
        while l < ArraySize(allspreads):
            if l == k:
                l += 1
                continue
            for i in range(0, learning_depth):
                LRmatrix[i].Set(n, allspreads[l].pricesBuffer[i])
            n += 1
            l += 1
        for i in range(0, learning_depth):
            LRmatrix[i].Set(splittedPairsNumber - 1, allspreads[k].pricesBuffer[i])
        linear_regression.LRBuild(LRmatrix, learning_depth, splittedPairsNumber - 1, retcode, linear_model, linear_report)
        nvars = 0
        linear_regression.LRUnpack(linear_model, allspreads[k].weights, nvars)
        k += 1

def calculateSpreads(depth):
    k = 0
    while k < ArraySize(allspreads):
        summKoeffForIndex = 0.0
        for i in range(depth - 1, 0 - 1, -1):
            n = 0
            for l in range(0, ArraySize(allspreads)):
                if l == k:
                    continue
                summKoeffForIndex += allspreads[l].pricesBuffer[i] * allspreads[k].weights[n]
                n += 1
            allspreads[k].spreadBuffer[i] = allspreads[k].pricesBuffer[i] - (summKoeffForIndex + allspreads[k].weights[ArraySize(allspreads) - 1])
            summKoeffForIndex = 0.0
        std = MathStandardDeviation(allspreads[k].spreadBuffer)
        for i in range(depth - 1, 0 - 1, -1):
            allspreads[k].zscore[i] = _fdiv(allspreads[k].spreadBuffer[i], std)
        k += 1

def calculateMainSynthetic(depth):
    ArrayInitialize(zscore, 0)
    for i in range(depth - 1, 0 - 1, -1):
        for l in range(0, ArraySize(allspreads)):
            zscore[i] += allspreads[l].zscore[i]

def isNewBar():
    global last_time
    lastbar_time = SeriesInfoInteger(Symbol(), Period(), SERIES_LASTBAR_DATE)
    if last_time == 0:
        last_time = lastbar_time
        return False
    if last_time != lastbar_time:
        last_time = lastbar_time
        return True
    return False

def getSymbolByName(symbol):
    symbol_name = ''
    if symbol == '':
        return ''
    s = 0
    while s < SymbolsTotal(False):
        symbol_name = SymbolName(s, False)
        if symbol == symbol_name:
            SymbolSelect(symbol, True)
            return symbol
        s += 1
    Alert('The symbol ' + symbol + ' is not present on the server, please change symbol name!')
    return ''

# ---- global variables initialised from expressions
QNaN = StringToDouble('nan')  # QNaN
QPOSINF = StringToDouble('inf')  # +infinity 1.#INF
QNEGINF = StringToDouble('-inf')  # -infinity -1.#INF
linear_regression = CLinReg()
linear_model = CLinearModel()
linear_report = CLRReport()
LRmatrix = CMatrixDouble()
allspreads = Arr(0, 0, factory=spreads)

# ---- static local variables
_s_MathLog2_factor = 1.0 / M_LN2
_s_MathLog2_factor_ = 1.0 / M_LN2


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CointegrationIndicator(_MQL5Indicator):
    name = 'cointegration_indicator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'learning_depth': 500,
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

