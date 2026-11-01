"""BB stops 2 - JMA — converted from MQL5: MQL5 Indicators/BB stops JMA - multiple stops/BB stops 2 - JMA.mq5

Bollinger bands stops - JMA based with multiple stops
Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 8}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 5, 8: 5}, 'colors': {1: [16748574], 2: [6333684], 3: [16748574], 4: [6333684], 5: [16748574], 6: [6333684], 7: [16748574], 8: [6333684]}, 'widths': {1: 3, 2: 3, 7: 2, 8: 2}, 'styles': {}, 'labels': {1: 'Bollinger bands stops up stop line', 2: 'Bollinger bands stops down stop line', 3: 'Bollinger bands stops up first stop line', 4: 'Bollinger bands stops down first stop line', 5: 'Bollinger bands stops up second stop line', 6: 'Bollinger bands stops down second stop line', 7: 'Bollinger bands stops up trend start', 8: 'Bollinger bands stops down trend start'}, 'levels': [], 'description': ['Bollinger bands stops - JMA based with multiple stops'], 'name': 'BB stops 2 - JMA', 'source': 'MQL5 Indicators/BB stops JMA - multiple stops/BB stops 2 - JMA.mq5', 'folder': 'BB stops JMA - multiple stops', 'inputs': [{'mql': 'inpJmaPeriod', 'py': 'inpJmaPeriod', 'param': 'inpJmaPeriod', 'type': 'double', 'default': 30.0, 'label': 'JMA period', 'sinput': False}, {'mql': 'inpJmaPhase', 'py': 'inpJmaPhase', 'param': 'inpJmaPhase', 'type': 'double', 'default': 0.0, 'label': 'JMA phase', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpDevPeriod', 'py': 'inpDevPeriod', 'param': 'inpDevPeriod', 'type': 'double', 'default': 20.0, 'label': 'Deviation period (<=1 for same as average period)', 'sinput': False}, {'mql': 'inpDeviation', 'py': 'inpDeviation', 'param': 'inpDeviation', 'type': 'double', 'default': 2.0, 'label': 'Deviation multiplier', 'sinput': False}, {'mql': '__º__01_00', 'py': '__º__01_00', 'param': None, 'type': 'string', 'default': '', 'label': '.', 'sinput': False}, {'mql': '__º__01_01', 'py': '__º__01_01', 'param': None, 'type': 'string', 'default': '', 'label': 'Risk settings', 'sinput': False}, {'mql': '__º__01_02', 'py': '__º__01_02', 'param': None, 'type': 'string', 'default': '', 'label': '.', 'sinput': False}, {'mql': 'inpRisk', 'py': 'inpRisk', 'param': 'inpRisk', 'type': 'double', 'default': 0.75, 'label': 'Risk multiplier', 'sinput': False}, {'mql': 'inpRisk2', 'py': 'inpRisk2', 'param': 'inpRisk2', 'type': 'double', 'default': 1.5, 'label': 'Risk 2 multiplier', 'sinput': False}, {'mql': 'inpRisk3', 'py': 'inpRisk3', 'param': 'inpRisk3', 'type': 'double', 'default': 2.5, 'label': 'Risk 3 multiplier', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpJmaPeriod = _input('inpJmaPeriod', 30.0)  # JMA period
inpJmaPhase = _input('inpJmaPhase', 0.0)  # JMA phase
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpDevPeriod = _input('inpDevPeriod', 20.0)  # Deviation period (<=1 for same as average period)
inpDeviation = _input('inpDeviation', 2.0)  # Deviation multiplier
__º__01_00 = _input('__º__01_00', '')  # .
__º__01_01 = _input('__º__01_01', '')  # Risk settings
__º__01_02 = _input('__º__01_02', '')  # .
inpRisk = _input('inpRisk', 0.75)  # Risk multiplier
inpRisk2 = _input('inpRisk2', 1.5)  # Risk 2 multiplier
inpRisk3 = _input('inpRisk3', 2.5)  # Risk 3 multiplier
lineup = Arr(0, 0.0)
linedn = Arr(0, 0.0)
lineup2 = Arr(0, 0.0)
linedn2 = Arr(0, 0.0)
lineup3 = Arr(0, 0.0)
linedn3 = Arr(0, 0.0)
arrowup = Arr(0, 0.0)
arrowdn = Arr(0, 0.0)
_risk1 = 0.0
_risk2 = 0.0
_risk3 = 0.0
_devPeriod = 0.0
workEmaDeviation = Arr(6, 0.0, dyn=False, dims=(2,))
workSmooth = Arr(15, 0.0, dyn=False, dims=(10,))
workStops = Arr(6, 0.0, dyn=False, dims=(9,))

class sStops(MqlObject):
    _q_fields = ('upline', 'downline', 'upline2', 'downline2', 'upline3', 'downline3', 'trend', 'trendChange')
    def __init__(self, *args):
        self.upline = 0.0
        self.downline = 0.0
        self.upline2 = 0.0
        self.downline2 = 0.0
        self.upline3 = 0.0
        self.downline3 = 0.0
        self.trend = 0
        self.trendChange = False

def OnInit():
    global _devPeriod, _risk1, _risk2, _risk3
    SetIndexBuffer(0, lineup, INDICATOR_DATA)
    SetIndexBuffer(1, linedn, INDICATOR_DATA)
    SetIndexBuffer(2, lineup2, INDICATOR_DATA)
    SetIndexBuffer(3, linedn2, INDICATOR_DATA)
    SetIndexBuffer(4, lineup3, INDICATOR_DATA)
    SetIndexBuffer(5, linedn3, INDICATOR_DATA)
    SetIndexBuffer(6, arrowup, INDICATOR_DATA)
    PlotIndexGetInteger(6, PLOT_ARROW, 159)
    SetIndexBuffer(7, arrowdn, INDICATOR_DATA)
    PlotIndexGetInteger(7, PLOT_ARROW, 159)
    _risks = Arr(3, 0.0, dyn=False)
    _risks[0] = inpRisk
    _risks[1] = inpRisk2
    _risks[2] = inpRisk3
    ArraySort(_risks)
    _risk1 = _risks[0]
    _risk2 = _risks[1]
    _risk3 = _risks[2]
    _devPeriod = (inpDevPeriod if (inpDevPeriod > 1) else inpJmaPeriod)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    _result = sStops()
    i = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    while i < rates_total:
        _price = getPrice(inpPrice, open, close, high, low, i)
        _avg = iSmooth(_price, inpJmaPeriod, inpJmaPhase, i)
        _dev = iEmaDeviation(_price, _devPeriod, i)
        _assign(_result, iStops(_price, _avg, _dev, inpDeviation, _risk1, _risk2, _risk3, i))
        lineup[i] = _result.upline3
        linedn[i] = _result.downline3
        lineup2[i] = _result.upline
        linedn2[i] = _result.downline
        lineup3[i] = _result.upline2
        linedn3[i] = _result.downline2
        arrowup[i] = (lineup[i] if (_result.trendChange and _result.trend == 1) else EMPTY_VALUE)
        arrowdn[i] = (linedn[i] if (_result.trendChange and _result.trend == -1) else EMPTY_VALUE)
        i += 1
    return i

def iEmaDeviation(price, period, i, instance=0):
    _indC = _imod(i, 6)
    _inst = instance * 2
    if i > 0 and period > 1:
        _indP = _imod(i - 1, 6)
        _alpha = _fdiv(2.0, 2.0 + ((period - 1.0) / 2.0))
        workEmaDeviation[_indC][_inst + 0] = workEmaDeviation[_indP][_inst + 0] + (_alpha * (price - workEmaDeviation[_indP][_inst + 0]))
        workEmaDeviation[_indC][_inst + 1] = workEmaDeviation[_indP][_inst + 1] + (_alpha * ((price * price) - workEmaDeviation[_indP][_inst + 1]))
    else:
        for k in range(0, 2):
            workEmaDeviation[_indC][_inst + k] = price
    return MathSqrt(_fdiv(period * (workEmaDeviation[_indC][_inst + 1] - (workEmaDeviation[_indC][_inst + 0] * workEmaDeviation[_indC][_inst + 0])), ((period - 1.0) if (period > 2) else 1)))

def iSmooth(price, length, phase, i, instance=0):
    _indP = _imod(i - 1, 15)
    _indC = _imod(i, 15)
    _inst = instance * 10
    if i == 0 or length <= 1:
        k = 0
        while k < 7:
            workSmooth[_indC][_inst + k] = price
            k += 1
        while k < 10:
            workSmooth[_indC][_inst + k] = 0.0
            k += 1
        return price
    len1 = (MathLog(MathSqrt(0.5 * (length - 1.0))) / M_LN2) + 2.0
    if len1 < 0:
        len1 = 0.0
    pow1 = len1 - 2.0
    if pow1 < 0.5:
        pow1 = 0.5
    del1 = price - workSmooth[_indP][_inst + 5]
    absDel1 = (del1 if (del1 > 0) else (-del1))
    del2 = price - workSmooth[_indP][_inst + 6]
    absDel2 = (del2 if (del2 > 0) else (-del2))
    _indF = _imod(((i - 10) if (i > 10) else 0), 15)
    workSmooth[_indC][_inst + 7] = (absDel1 if (absDel1 > absDel2) else absDel2 if (absDel1 < absDel2) else 0)
    workSmooth[_indC][_inst + 8] = workSmooth[_indP][_inst + 8] + ((workSmooth[_indC][_inst + 7] - workSmooth[_indF][_inst + 7]) * 0.1)
    workSmooth[_indC][_inst + 9] = workSmooth[_indP][_inst + 9] + (_fdiv(2.0, (30 if (length < 7.5) else (4.0 * length)) + 1.0) * (workSmooth[_indC][_inst + 8] - workSmooth[_indP][_inst + 9]))
    dVolty = (_fdiv(workSmooth[_indC][_inst + 7], workSmooth[_indC][_inst + 9]) if (workSmooth[_indC][_inst + 9] > 0) else 0)
    dVoltyTmp = MathPow(len1, _fdiv(1.0, pow1))
    if dVolty > dVoltyTmp:
        dVolty = dVoltyTmp
    if dVolty < 1.0:
        dVolty = 1.0
    pow2 = MathPow(dVolty, pow1)
    len2 = MathSqrt(0.5 * (length - 1)) * len1
    Kv = MathPow(_fdiv(len2, len2 + 1), MathSqrt(pow2))
    workSmooth[_indC][_inst + 5] = (price if (del1 > 0) else (price - (Kv * del1)))
    workSmooth[_indC][_inst + 6] = (price if (del2 < 0) else (price - (Kv * del2)))
    corr = ((100.0 if (phase > 100.0) else -100.0 if (phase < -100.0) else phase) / 100.0) + 1.5
    beta = _fdiv(0.45 * (length - 1.0), (0.45 * (length - 1.0)) + 2.0)
    alpha = MathPow(beta, pow2)
    workSmooth[_indC][_inst + 0] = price + (alpha * (workSmooth[_indP][_inst + 0] - price))
    workSmooth[_indC][_inst + 1] = ((price - workSmooth[_indC][_inst + 0]) * (1 - beta)) + (beta * workSmooth[_indP][_inst + 1])
    workSmooth[_indC][_inst + 2] = workSmooth[_indC][_inst + 0] + (corr * workSmooth[_indC][_inst + 1])
    workSmooth[_indC][_inst + 3] = ((workSmooth[_indC][_inst + 2] - workSmooth[_indP][_inst + 4]) * ((1 - alpha) * (1 - alpha))) + (alpha * alpha * workSmooth[_indP][_inst + 3])
    workSmooth[_indC][_inst + 4] = workSmooth[_indP][_inst + 4] + workSmooth[_indC][_inst + 3]
    return workSmooth[_indC][_inst + 4]

def iStops(value, average, deviation, bands, risk, risk2, risk3, i, instance=0):
    _indC = _imod(i, 6)
    _indP = _imod(i - 1, 6)
    _inst = instance * 9
    workStops[_indC][_inst + 1] = average + (bands * deviation)
    workStops[_indC][_inst + 0] = average - (bands * deviation)
    workStops[_indC][_inst + 3] = average + (risk * deviation)
    workStops[_indC][_inst + 2] = average - (risk * deviation)
    workStops[_indC][_inst + 5] = average + (risk2 * deviation)
    workStops[_indC][_inst + 4] = average - (risk2 * deviation)
    workStops[_indC][_inst + 7] = average + (risk3 * deviation)
    workStops[_indC][_inst + 6] = average - (risk3 * deviation)
    workStops[_indC][_inst + 8] = ((1 if (value > workStops[_indP][_inst + 1]) else -1 if (value < workStops[_indP][_inst + 0]) else workStops[_indP][_inst + 8]) if (i > 0) else 0)
    if i > 0:
        if workStops[_indC][_inst + 8] == -1:
            if workStops[_indC][_inst + 1] > workStops[_indP][_inst + 1]:
                workStops[_indC][_inst + 1] = workStops[_indP][_inst + 1]
            if workStops[_indC][_inst + 3] > workStops[_indP][_inst + 3]:
                workStops[_indC][_inst + 3] = workStops[_indP][_inst + 3]
            if workStops[_indC][_inst + 5] > workStops[_indP][_inst + 5]:
                workStops[_indC][_inst + 5] = workStops[_indP][_inst + 5]
            if workStops[_indC][_inst + 7] > workStops[_indP][_inst + 7]:
                workStops[_indC][_inst + 7] = workStops[_indP][_inst + 7]
        if workStops[_indC][_inst + 8] == 1:
            if workStops[_indC][_inst + 0] < workStops[_indP][_inst + 0]:
                workStops[_indC][_inst + 0] = workStops[_indP][_inst + 0]
            if workStops[_indC][_inst + 2] < workStops[_indP][_inst + 2]:
                workStops[_indC][_inst + 2] = workStops[_indP][_inst + 2]
            if workStops[_indC][_inst + 4] < workStops[_indP][_inst + 4]:
                workStops[_indC][_inst + 4] = workStops[_indP][_inst + 4]
            if workStops[_indC][_inst + 6] < workStops[_indP][_inst + 6]:
                workStops[_indC][_inst + 6] = workStops[_indP][_inst + 6]
    _result = sStops()
    _result.trend = _int(workStops[_indC][_inst + 8])
    _result.trendChange = ((workStops[_indC][_inst + 8] != workStops[_indP][_inst + 8]) if (i > 0) else False)
    _result.upline = (workStops[_indC][_inst + 2] if (workStops[_indC][_inst + 8] == 1) else EMPTY_VALUE)
    _result.downline = (workStops[_indC][_inst + 3] if (workStops[_indC][_inst + 8] == -1) else EMPTY_VALUE)
    _result.upline2 = (workStops[_indC][_inst + 4] if (workStops[_indC][_inst + 8] == 1) else EMPTY_VALUE)
    _result.downline2 = (workStops[_indC][_inst + 5] if (workStops[_indC][_inst + 8] == -1) else EMPTY_VALUE)
    _result.upline3 = (workStops[_indC][_inst + 6] if (workStops[_indC][_inst + 8] == 1) else EMPTY_VALUE)
    _result.downline3 = (workStops[_indC][_inst + 7] if (workStops[_indC][_inst + 8] == -1) else EMPTY_VALUE)
    return _copy(_result)

def getPrice(tprice, open, close, high, low, i):
    _sw1 = tprice
    if _sw1 == PRICE_CLOSE:
        return close[i]
    elif _sw1 == PRICE_OPEN:
        return open[i]
    elif _sw1 == PRICE_HIGH:
        return high[i]
    elif _sw1 == PRICE_LOW:
        return low[i]
    elif _sw1 == PRICE_MEDIAN:
        return (high[i] + low[i]) / 2.0
    elif _sw1 == PRICE_TYPICAL:
        return (high[i] + low[i] + close[i]) / 3.0
    elif _sw1 == PRICE_WEIGHTED:
        return (high[i] + low[i] + close[i] + close[i]) / 4.0
    return 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BBStops2JMA(_MQL5Indicator):
    name = 'BB stops 2 - JMA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpJmaPeriod': 30.0,  # JMA period
        'inpJmaPhase': 0.0,  # JMA phase
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpDevPeriod': 20.0,  # Deviation period (<=1 for same as average period)
        'inpDeviation': 2.0,  # Deviation multiplier
        'inpRisk': 0.75,  # Risk multiplier
        'inpRisk2': 1.5,  # Risk 2 multiplier
        'inpRisk3': 2.5,  # Risk 3 multiplier
    }

