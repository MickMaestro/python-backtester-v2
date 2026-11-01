"""3x_nonlinearregression — converted from MQL5: MQL5 Indicators/^X_NonLinearRegression/3x_nonlinearregression.mq5

Copyright: Copyright © 2007, Mr.WT, Senior Linux Hacker; Link: http://w-tiger.narod.ru/wk2/; Version: 2.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, Mr.WT, Senior Linux Hacker', 'link': 'http://w-tiger.narod.ru/wk2/', 'version': '2.01', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': '3x_nonlinearregression', 'source': 'MQL5 Indicators/^X_NonLinearRegression/3x_nonlinearregression.mq5', 'folder': '^X_NonLinearRegression', 'inputs': [{'mql': 'period', 'py': 'period', 'param': 'period', 'type': 'int', 'default': 120, 'label': '', 'sinput': False}, {'mql': 'RegressionDegree_', 'py': 'RegressionDegree_', 'param': 'RegressionDegree_', 'type': 'uint', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'KNL_Dev', 'py': 'KNL_Dev', 'param': 'KNL_Dev', 'type': 'double', 'default': 2.72, 'label': '', 'sinput': False}, {'mql': 'RegressionColor1', 'py': 'RegressionColor1', 'param': None, 'type': 'color', 'default': 0, 'label': 'Regression color 1', 'sinput': False}, {'mql': 'RegressionColor2', 'py': 'RegressionColor2', 'param': None, 'type': 'color', 'default': 0, 'label': 'Regression color 2', 'sinput': False}, {'mql': 'RegressionColor3', 'py': 'RegressionColor3', 'param': None, 'type': 'color', 'default': 0, 'label': 'Regression color 3', 'sinput': False}, {'mql': 'RegressionColor4', 'py': 'RegressionColor4', 'param': None, 'type': 'color', 'default': 0, 'label': 'Regression color 4', 'sinput': False}, {'mql': 'linesStyle', 'py': 'linesStyle', 'param': 'linesStyle', 'type': 'int', 'default': 1, 'label': 'Lines style', 'sinput': False}, {'mql': 'linesWidth', 'py': 'linesWidth', 'param': 'linesWidth', 'type': 'int', 'default': 1, 'label': 'Lines width', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

BlueViolet = 0xE22B8A  # MQL4 colour name
Magenta = 0xFF00FF  # MQL4 colour name
Red = 0x0000FF  # MQL4 colour name
SpringGreen = 0x7FFF00  # MQL4 colour name

# enum WIDTH
Width_1 = 1
Width_2 = 2
Width_3 = 3
Width_4 = 4
Width_5 = 5
_enum('WIDTH', {1: 'Width_1', 2: 'Width_2', 3: 'Width_3', 4: 'Width_4', 5: 'Width_5'})

# enum STYLE
SOLID_ = 0
DASH_ = 1
DOT_ = 2
DASHDOT_ = 3
DASHDOTDOT_ = 4
_enum('STYLE', {0: 'SOLID_', 1: 'DASH_', 2: 'DOT_', 3: 'DASHDOT_', 4: 'DASHDOTDOT_'})

# ---- inputs and global variables
period = _input('period', 120)
RegressionDegree_ = _input('RegressionDegree_', 5)
KNL_Dev = _input('KNL_Dev', 2.72)
linesStyle = _input('linesStyle', DASH_)  # Lines style
linesWidth = _input('linesWidth', Width_1)  # Lines width
fx = 0.0
fx1 = 0.0
a = Arr(10, 0.0, dyn=False, dims=(10,))
b = Arr(10, 0.0, dyn=False)
x = Arr(10, 0.0, dyn=False)
sx = Arr(20, 0.0, dyn=False)
sum_ = 0.0
sum1 = 0.0
sq = 0.0
p = 0
nn = 0
kt = 0
te = 0
te1 = 0
tp = 0
t0 = 0
i0 = 0
ip = 0
pn = 0
i0n = 0
ipn = 0
RegressionDegree = 0
str_ = ""

def init(RatesTotal, Time):
    global i0, ip, kt, nn, p, pn, t0, tp
    p = period
    if p > RatesTotal:
        Comment('\n\n                    ERROR - TOO SMALL HISTORY, RETURN NOW!')
        return False
    kt = PeriodSeconds()
    nn = RegressionDegree + 1
    t0 = Time[0]
    i0 = 0
    ip = i0 + p
    tp = Time[ip]
    pn = p
    for j in range(_idiv(-p, 2), p):
        sJ = str_ + ')' + _str(j)
        r = i0 + j
        if r < 0:
            r = 0
        ObjectCreate(0, '_ar(' + sJ, OBJ_TREND, 0, Time[r + 1], 0, Time[r], 0)
        ObjectSetInteger(0, '_ar(' + sJ, OBJPROP_RAY, False)
        ObjectSetInteger(0, '_ar(' + sJ, OBJPROP_STYLE, linesStyle)
        ObjectSetInteger(0, '_ar(' + sJ, OBJPROP_WIDTH, linesWidth)
        ObjectCreate(0, '_arH(' + sJ, OBJ_TREND, 0, Time[r + 1], 0, Time[r], 0)
        ObjectSetInteger(0, '_arH(' + sJ, OBJPROP_RAY, False)
        ObjectSetInteger(0, '_arH(' + sJ, OBJPROP_STYLE, linesStyle)
        ObjectSetInteger(0, '_arH(' + sJ, OBJPROP_WIDTH, linesWidth)
        ObjectCreate(0, '_arL(' + sJ, OBJ_TREND, 0, Time[r + 1], 0, Time[r], 0)
        ObjectSetInteger(0, '_arL(' + sJ, OBJPROP_RAY, False)
        ObjectSetInteger(0, '_arL(' + sJ, OBJPROP_STYLE, linesStyle)
        ObjectSetInteger(0, '_arL(' + sJ, OBJPROP_WIDTH, linesWidth)
    return True

def OnInit():
    global RegressionDegree, str_
    str_ = ''
    StringConcatenate(_GlobRef(globals(), 'str_'), period, ',', RegressionDegree, ',', DoubleToString(KNL_Dev, 3))
    IndicatorSetString(INDICATOR_SHORTNAME, 'X_NonLinearRegression_v2.0.1(' + str_ + ')')
    RegressionDegree = _int(RegressionDegree_)
    if RegressionDegree > 8:
        RegressionDegree = 8
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'DinapoliTargets')

def OnDeinit(reason):
    for j in range(p, _idiv(-p, 2) - 1, -1):
        sJ = str_ + ')' + _str(j)
        ObjectDelete(0, '_ar(' + sJ)
        ObjectDelete(0, '_arH(' + sJ)
        ObjectDelete(0, '_arL(' + sJ)
    Comment('')

def OnCalculate(rates_total, prev_calculated, Time, Open, high, low, Close, Tick_volume, Volume, Spread):
    global fx, fx1, i0n, ipn, p, pn, sq, sum1, sum_, te, te1
    if rates_total < (period + 1):
        return 0
    if rates_total == prev_calculated:
        return rates_total
    ArraySetAsSeries(Time, True)
    ArraySetAsSeries(Close, True)
    for j in range(p, _idiv(-p, 2) - 1, -1):
        sJ = str_ + ')' + _str(j)
        ObjectDelete(0, '_ar(' + sJ)
        ObjectDelete(0, '_arH(' + sJ)
        ObjectDelete(0, '_arL(' + sJ)
    if not init(rates_total, Time):
        return 0
    i = 0
    j = 0
    n = 0
    k = 0
    if i0n != i0 or ipn != ip:
        p = ip - i0
        i0n = ip
        ipn = ip
        if pn < p:
            j = pn
            for j in range(j, p + 1):
                sJ = str_ + ')' + _str(j)
                ObjectCreate(0, '_ar(' + sJ, OBJ_TREND, 0, Time[i0 + 1 + j], 0, Time[i0 + j], 0)
                ObjectSetInteger(0, '_ar(' + sJ, OBJPROP_RAY, False)
                ObjectSetInteger(0, '_ar(' + sJ, OBJPROP_STYLE, linesStyle)
                ObjectSetInteger(0, '_ar(' + sJ, OBJPROP_WIDTH, linesWidth)
                ObjectCreate(0, '_arH(' + sJ, OBJ_TREND, 0, Time[i0 + 1 + j], 0, Time[i0 + j], 0)
                ObjectSetInteger(0, '_arH(' + sJ, OBJPROP_RAY, False)
                ObjectSetInteger(0, '_arH(' + sJ, OBJPROP_STYLE, linesStyle)
                ObjectSetInteger(0, '_arH(' + sJ, OBJPROP_WIDTH, linesWidth)
                ObjectCreate(0, '_arL(' + sJ, OBJ_TREND, 0, Time[i0 + 1 + j], 0, Time[i0 + j], 0)
                ObjectSetInteger(0, '_arL(' + sJ, OBJPROP_RAY, False)
                ObjectSetInteger(0, '_arL(' + sJ, OBJPROP_STYLE, linesStyle)
                ObjectSetInteger(0, '_arL(' + sJ, OBJPROP_WIDTH, linesWidth)
            else:
                j = _range_end(j, p + 1, 1)
            j = _idiv(-pn, 2)
            for j in range(j, _idiv(-p, 2) - 1, -1):
                sJ = str_ + ')' + _str(j)
                ObjectCreate(0, '_ar(' + sJ, OBJ_TREND, 0, Time[i0 + 1 + j], 0, Time[i0 + j], 0)
                ObjectSetInteger(0, '_ar(' + sJ, OBJPROP_RAY, False)
                ObjectSetInteger(0, '_ar(' + sJ, OBJPROP_STYLE, linesStyle)
                ObjectSetInteger(0, '_ar(' + sJ, OBJPROP_WIDTH, linesWidth)
                ObjectCreate(0, '_arH(' + sJ, OBJ_TREND, 0, Time[i0 + 1 + j], 0, Time[i0 + j], 0)
                ObjectSetInteger(0, '_arH(' + sJ, OBJPROP_RAY, False)
                ObjectSetInteger(0, '_arH(' + sJ, OBJPROP_STYLE, linesStyle)
                ObjectSetInteger(0, '_arH(' + sJ, OBJPROP_WIDTH, linesWidth)
                ObjectCreate(0, '_arL(' + sJ, OBJ_TREND, 0, Time[i0 + 1 + j], 0, Time[i0 + j], 0)
                ObjectSetInteger(0, '_arL(' + sJ, OBJPROP_RAY, False)
                ObjectSetInteger(0, '_arL(' + sJ, OBJPROP_STYLE, linesStyle)
                ObjectSetInteger(0, '_arL(' + sJ, OBJPROP_WIDTH, linesWidth)
            else:
                j = _range_end(j, _idiv(-p, 2) - 1, -1)
            pn = p
        if pn > p:
            j = pn
            for j in range(j, p - 1, -1):
                sJ = str_ + ')' + _str(j)
                ObjectDelete(0, '_ar(' + sJ)
                ObjectDelete(0, '_arH(' + sJ)
                ObjectDelete(0, '_arL(' + sJ)
            else:
                j = _range_end(j, p - 1, -1)
            j = _idiv(-p, 2)
            for j in range(j, _idiv(-pn, 2) - 1, -1):
                sJ = str_ + ')' + _str(j)
                ObjectDelete(0, '_ar(' + sJ)
                ObjectDelete(0, '_arH(' + sJ)
                ObjectDelete(0, '_arL(' + sJ)
            else:
                j = _range_end(j, _idiv(-pn, 2) - 1, -1)
            pn = p
    sx[1] = p + 1
    i = 1
    for i in range(i, (nn * 2) - 2 + 1):
        sum_ = 0.0
        n = i0
        for n in range(n, i0 + p + 1):
            sum_ += MathPow(n, i)
        else:
            n = _range_end(n, i0 + p + 1, 1)
        sx[i + 1] = sum_
    else:
        i = _range_end(i, (nn * 2) - 2 + 1, 1)
    i = 1
    for i in range(i, nn + 1):
        sum_ = 0.0
        n = i0
        for n in range(n, i0 + p + 1):
            if i == 1:
                sum_ += Close[n]
            else:
                sum_ += Close[n] * MathPow(n, i - 1)
        else:
            n = _range_end(n, i0 + p + 1, 1)
        b[i] = sum_
    else:
        i = _range_end(i, nn + 1, 1)
    j = 1
    for j in range(j, nn + 1):
        i = 1
        for i in range(i, nn + 1):
            k = i + j - 1
            a[i][j] = sx[k]
        else:
            i = _range_end(i, nn + 1, 1)
    else:
        j = _range_end(j, nn + 1, 1)
    af_Gauss(nn)
    sq = 0.0
    n = p
    for n in range(n, 0 - 1, -1):
        sum_ = 0.0
        k = 1
        for k in range(k, RegressionDegree + 1):
            sum_ += x[k + 1] * MathPow(i0 + n, k)
            sum1 += x[k + 1] * MathPow(i0 + n + 1, k)
        else:
            k = _range_end(k, RegressionDegree + 1, 1)
        fx = x[1] + sum_
        sq += MathPow(Close[n + i0] - fx, 2)
    else:
        n = _range_end(n, 0 - 1, -1)
    sq = KNL_Dev * MathSqrt(_fdiv(sq, p + 1))
    n = p
    for n in range(n, _idiv(-p, 2) - 1, -1):
        sum_ = 0.0
        sum1 = 0.0
        sN = str_ + ')' + _str(n)
        k = 1
        for k in range(k, RegressionDegree + 1):
            sum_ += x[k + 1] * MathPow(i0 + n, k)
            sum1 += x[k + 1] * MathPow(i0 + n + 1, k)
        else:
            k = _range_end(k, RegressionDegree + 1, 1)
        fx = x[1] + sum_
        fx1 = x[1] + sum1
        if n >= 0 and n < p:
            ObjectMove(0, '_ar(' + sN, 0, Time[n + i0 + 1], fx1)
            ObjectMove(0, '_ar(' + sN, 1, Time[n + i0], fx)
            ObjectMove(0, '_arH(' + sN, 0, Time[n + i0 + 1], fx1 + sq)
            ObjectMove(0, '_arH(' + sN, 1, Time[n + i0], fx + sq)
            ObjectMove(0, '_arL(' + sN, 0, Time[n + i0 + 1], fx1 - sq)
            ObjectMove(0, '_arL(' + sN, 1, Time[n + i0], fx - sq)
            if fx > fx1:
                ObjectSetInteger(0, '_ar(' + sN, OBJPROP_COLOR, RegressionColor1)
                ObjectSetInteger(0, '_arH(' + sN, OBJPROP_COLOR, RegressionColor1)
                ObjectSetInteger(0, '_arL(' + sN, OBJPROP_COLOR, RegressionColor1)
            if fx < fx1:
                ObjectSetInteger(0, '_ar(' + sN, OBJPROP_COLOR, RegressionColor2)
                ObjectSetInteger(0, '_arH(' + sN, OBJPROP_COLOR, RegressionColor2)
                ObjectSetInteger(0, '_arL(' + sN, OBJPROP_COLOR, RegressionColor2)
        if n < 0:
            if (n + i0) >= 0:
                ObjectMove(0, '_ar(' + sN, 0, Time[n + i0 + 1], fx1)
                ObjectMove(0, '_ar(' + sN, 1, Time[n + i0], fx)
                ObjectMove(0, '_arH(' + sN, 0, Time[n + i0 + 1], fx1 + sq)
                ObjectMove(0, '_arH(' + sN, 1, Time[n + i0], fx + sq)
                ObjectMove(0, '_arL(' + sN, 0, Time[n + i0 + 1], fx1 - sq)
                ObjectMove(0, '_arL(' + sN, 1, Time[n + i0], fx - sq)
            if (n + i0) < 0:
                te = Time[0] - ((n + i0) * kt)
                te1 = Time[0] - ((n + i0 + 1) * kt)
                ObjectMove(0, '_ar(' + sN, 0, te1, fx1)
                ObjectMove(0, '_ar(' + sN, 1, te, fx)
                ObjectMove(0, '_arH(' + sN, 0, te1, fx1 + sq)
                ObjectMove(0, '_arH(' + sN, 1, te, fx + sq)
                ObjectMove(0, '_arL(' + sN, 0, te1, fx1 - sq)
                ObjectMove(0, '_arL(' + sN, 1, te, fx - sq)
            if fx > fx1:
                ObjectSetInteger(0, '_ar(' + sN, OBJPROP_COLOR, RegressionColor3)
                ObjectSetInteger(0, '_arH(' + sN, OBJPROP_COLOR, RegressionColor3)
                ObjectSetInteger(0, '_arL(' + sN, OBJPROP_COLOR, RegressionColor3)
            if fx < fx1:
                ObjectSetInteger(0, '_ar(' + sN, OBJPROP_COLOR, RegressionColor4)
                ObjectSetInteger(0, '_arH(' + sN, OBJPROP_COLOR, RegressionColor4)
                ObjectSetInteger(0, '_arL(' + sN, OBJPROP_COLOR, RegressionColor4)
    else:
        n = _range_end(n, _idiv(-p, 2) - 1, -1)
    ChartRedraw(0)
    return rates_total

def af_Gauss(n):
    i = 0
    j = 0
    k = 0
    l = 0
    q = 0.0
    m = 0.0
    t = 0.0
    k = 1
    for k in range(k, n - 1 + 1):
        l = 0
        m = 0.0
        i = k
        for i in range(i, n + 1):
            if MathAbs(a[i][k]) > m:
                m = MathAbs(a[i][k])
                l = i
        else:
            i = _range_end(i, n + 1, 1)
        if l == 0:
            return
        if l != k:
            j = 1
            for j in range(j, n + 1):
                t = a[k][j]
                a[k][j] = a[l][j]
                a[l][j] = t
            else:
                j = _range_end(j, n + 1, 1)
            t = b[k]
            b[k] = b[l]
            b[l] = t
        i = k + 1
        for i in range(i, n + 1):
            q = _fdiv(a[i][k], a[k][k])
            j = 1
            for j in range(j, n + 1):
                if j == k:
                    a[i][j] = 0.0
                else:
                    a[i][j] = a[i][j] - (q * a[k][j])
            else:
                j = _range_end(j, n + 1, 1)
            b[i] = b[i] - (q * b[k])
        else:
            i = _range_end(i, n + 1, 1)
    else:
        k = _range_end(k, n - 1 + 1, 1)
    x[n] = _fdiv(b[n], a[n][n])
    i = n - 1
    for i in range(i, 1 - 1, -1):
        t = 0.0
        j = 1
        for j in range(j, n - i + 1):
            t = t + (a[i][i + j] * x[i + j])
            x[i] = _fdiv(1, a[i][i]) * (b[i] - t)
        else:
            j = _range_end(j, n - i + 1, 1)
    else:
        i = _range_end(i, 1 - 1, -1)

# ---- global variables initialised from expressions
RegressionColor1 = _input('RegressionColor1', _uint(SpringGreen))  # Regression color 1
RegressionColor2 = _input('RegressionColor2', _uint(Red))  # Regression color 2
RegressionColor3 = _input('RegressionColor3', _uint(BlueViolet))  # Regression color 3
RegressionColor4 = _input('RegressionColor4', _uint(Magenta))  # Regression color 4


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Ind3xNonlinearregression(_MQL5Indicator):
    name = '3x_nonlinearregression'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'period': 120,
        'RegressionDegree_': 5,
        'KNL_Dev': 2.72,
        'linesStyle': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=1),  # Lines style
        'linesWidth': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # Lines width
    }

