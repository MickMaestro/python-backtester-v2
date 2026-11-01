"""wlxfractals — converted from MQL5: MQL5 Indicators/wlxFractals/wlxfractals.mq5

Фракталы Билла Вильямса
Copyright: Copyright © 2004, by konKop, GOODMAN, Mstera, af + wellx; Link: http://www.metaquotes.net; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2004, by konKop, GOODMAN, Mstera, af + wellx', 'link': 'http://www.metaquotes.net', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711680], 2: [16711935]}, 'widths': {1: 3, 2: 3}, 'styles': {}, 'labels': {1: 'Up Fractal', 2: 'Down Fractal'}, 'levels': [], 'description': ['Фракталы Билла Вильямса'], 'name': 'wlxfractals', 'source': 'MQL5 Indicators/wlxFractals/wlxfractals.mq5', 'folder': 'wlxFractals', 'inputs': [{'mql': 'Equals', 'py': 'Equals', 'param': 'Equals', 'type': 'uint', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'nLeftUp', 'py': 'nLeftUp', 'param': 'nLeftUp', 'type': 'uint', 'default': 2, 'label': '', 'sinput': False}, {'mql': 'nRightUp', 'py': 'nRightUp', 'param': 'nRightUp', 'type': 'uint', 'default': 2, 'label': '', 'sinput': False}, {'mql': 'nLeftDown', 'py': 'nLeftDown', 'param': 'nLeftDown', 'type': 'uint', 'default': 2, 'label': '', 'sinput': False}, {'mql': 'nRightDown', 'py': 'nRightDown', 'param': 'nRightDown', 'type': 'uint', 'default': 2, 'label': '', 'sinput': False}, {'mql': 'UpLable', 'py': 'UpLable', 'param': 'UpLable', 'type': 'int', 'default': 217, 'label': 'лейба верхнего фрактала', 'sinput': False}, {'mql': 'DnLable', 'py': 'DnLable', 'param': 'DnLable', 'type': 'int', 'default': 218, 'label': 'лейба нижнего фрактала', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Equals = _input('Equals', 5)
nLeftUp = _input('nLeftUp', 2)
nRightUp = _input('nRightUp', 2)
nLeftDown = _input('nLeftDown', 2)
nRightDown = _input('nRightDown', 2)
UpLable = _input('UpLable', 217)  # лейба верхнего фрактала
DnLable = _input('DnLable', 218)  # лейба нижнего фрактала
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
min_rates_total = 0
cntup = 0
cntdown = 0
cnt = 0
r = 0
l = 0
e = 0
fup = 0
fdown = 0

def OnInit():
    global cnt, cntdown, cntup, e, fdown, fup, l, min_rates_total, r
    r = 0
    l = 0
    e = 0
    fup = 0
    fdown = 0
    cntup = _int(nLeftUp + nRightUp + Equals) + 1
    cntdown = _int(nLeftDown + nRightDown + Equals) + 1
    if cntup >= cntdown:
        cnt = cntup
    if cntup < cntdown:
        cnt = cntdown
    min_rates_total = MathMax(cntup, cntdown)
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, UpLable)
    ArraySetAsSeries(UpBuffer, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, DnBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, DnLable)
    ArraySetAsSeries(DnBuffer, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'wlxFractals'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global e, l, r
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    i = 0
    j = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        UpBuffer[bar] = EMPTY_VALUE
        DnBuffer[bar] = EMPTY_VALUE
    else:
        bar = _range_end(bar, 0 - 1, -1)
    bar = limit + _int(nRightUp)
    for bar in range(bar, _int(nRightUp) - 1, -1):
        r = _int(nRightUp)
        i = 1
        for i in range(i, r + 1):
            if high[bar] <= high[bar - i]:
                break
        else:
            i = _range_end(i, r + 1, 1)
        if i == (r + 1):
            l = _int(nLeftUp)
            e = _int(Equals)
            j = 1
            while j <= (l + _int(Equals)):
                if high[bar] < high[bar + j]:
                    break
                if high[bar] > high[bar + j]:
                    l -= 1
                if high[bar] == high[bar + j]:
                    e -= 1
                if not l:
                    UpBuffer[bar] = high[bar]
                    break
                if e < 0:
                    break
                j += 1
    else:
        bar = _range_end(bar, _int(nRightUp) - 1, -1)
    bar = limit + _int(nRightDown)
    for bar in range(bar, _int(nRightDown) - 1, -1):
        r = _int(nRightDown)
        i = 1
        for i in range(i, r + 1):
            if low[bar] >= low[bar - i]:
                break
        else:
            i = _range_end(i, r + 1, 1)
        if i == (r + 1):
            l = _int(nLeftDown)
            e = _int(Equals)
            j = 1
            while j <= (l + _int(Equals)):
                if low[bar] > low[bar + j]:
                    break
                if low[bar] < low[bar + j]:
                    l -= 1
                if low[bar] == low[bar + j]:
                    e -= 1
                if l == 0:
                    DnBuffer[bar] = low[bar]
                    break
                if e < 0:
                    break
                j += 1
    else:
        bar = _range_end(bar, _int(nRightDown) - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Wlxfractals(_MQL5Indicator):
    name = 'wlxfractals'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Equals': 5,
        'nLeftUp': 2,
        'nRightUp': 2,
        'nLeftDown': 2,
        'nRightDown': 2,
        'UpLable': 217,  # лейба верхнего фрактала
        'DnLable': 218,  # лейба нижнего фрактала
    }

