"""LinearRegressionChannel_Cloud — converted from MQL5: MQL5 Indicators/LinearRegressionChannel_Cloud/LinearRegressionChannel_Cloud.mq5

Канал линейной регрессии с сохранением своих значений в индикаторных буферах и с цветным фоновым заполнением канала
Copyright: Copyright © 2008, dimicr; Link: http://www.signalsbg.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2008, dimicr', 'link': 'http://www.signalsbg.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 5}, 'types': {1: 7, 2: 7, 3: 1, 4: 1, 5: 1}, 'colors': {1: [10025880], 2: [13353215], 3: [14822282], 4: [8421376], 5: [255]}, 'widths': {3: 1, 4: 1, 5: 1}, 'styles': {3: 4, 4: 4, 5: 4}, 'labels': {1: 'LinearRegressionChannel_Cloud Upper', 2: 'LinearRegressionChannel_Cloud Lower', 3: 'LinearRegression Line', 4: 'LinearRegression Resistance', 5: 'LinearRegression Support'}, 'levels': [], 'description': ['Канал линейной регрессии с сохранением своих значений в индикаторных буферах и с цветным фоновым заполнением канала'], 'name': 'LinearRegressionChannel_Cloud', 'source': 'MQL5 Indicators/LinearRegressionChannel_Cloud/LinearRegressionChannel_Cloud.mq5', 'folder': 'LinearRegressionChannel_Cloud', 'inputs': [{'mql': 'UserPrice', 'py': 'UserPrice', 'param': 'UserPrice', 'type': 'int', 'default': 0, 'label': 'Вариант цен', 'sinput': False}, {'mql': 'barsToCount', 'py': 'barsToCount', 'param': 'barsToCount', 'type': 'uint', 'default': 100, 'label': 'Количество баров для расчёта', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_USER_PRICE
MODE_CLOSE_ = 0
MODE_HIGH_LOW = 1
_enum('ENUM_USER_PRICE', {0: 'MODE_CLOSE_', 1: 'MODE_HIGH_LOW'})

# ---- inputs and global variables
UserPrice = _input('UserPrice', MODE_CLOSE_)  # Вариант цен
barsToCount = _input('barsToCount', 100)  # Количество баров для расчёта
LineBuffer = Arr(0, 0.0)
ResBuffer = Arr(0, 0.0)
SupBuffer = Arr(0, 0.0)
UpUpBuffer = Arr(0, 0.0)
UpDnBuffer = Arr(0, 0.0)
DnUpBuffer = Arr(0, 0.0)
DnDnBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(barsToCount)
    SetIndexBuffer(0, UpUpBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(UpUpBuffer, True)
    SetIndexBuffer(1, UpDnBuffer, INDICATOR_DATA)
    ArraySetAsSeries(UpDnBuffer, True)
    SetIndexBuffer(2, DnUpBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(DnUpBuffer, True)
    SetIndexBuffer(3, DnDnBuffer, INDICATOR_DATA)
    ArraySetAsSeries(DnDnBuffer, True)
    SetIndexBuffer(4, LineBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(LineBuffer, True)
    SetIndexBuffer(5, ResBuffer, INDICATOR_DATA)
    SetIndexBuffer(6, SupBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(ResBuffer, True)
    ArraySetAsSeries(SupBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'LinearRegression(', EnumToString(UserPrice, 'ENUM_USER_PRICE'), ', ', barsToCount, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    DRAW_BEGIN = rates_total - min_rates_total + 1
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, DRAW_BEGIN)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, DRAW_BEGIN)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, DRAW_BEGIN)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, DRAW_BEGIN)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, DRAW_BEGIN)
    a = 0.0
    b = 0.0
    c = 0.0
    res = 0.0
    sumy = 0.0
    sumx = 0.0
    sumxy = 0.0
    sumx2 = 0.0
    h = 0.0
    l = 0.0
    bar = 0
    limit = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    bar = limit + min_rates_total
    for bar in range(bar, min_rates_total, -1):
        LineBuffer[bar] = 0.0
        SupBuffer[bar] = 0.0
        ResBuffer[bar] = 0.0
        UpUpBuffer[bar] = 0.0
        UpDnBuffer[bar] = 0.0
        DnUpBuffer[bar] = 0.0
        DnDnBuffer[bar] = 0.0
    else:
        bar = _range_end(bar, min_rates_total, -1)
    bar = 0
    for bar in range(bar, min_rates_total):
        sumy += close[bar]
        sumxy += close[bar] * bar
        sumx += bar
        sumx2 += bar * bar
    else:
        bar = _range_end(bar, min_rates_total, 1)
    c = (sumx2 * barsToCount) - (sumx * sumx)
    if not c:
        Alert('Error in linear regression!')
        return 0
    b = _fdiv((sumxy * barsToCount) - (sumx * sumy), c)
    a = (sumy - (sumx * b)) / barsToCount
    bar = 0
    for bar in range(bar, min_rates_total):
        DnUpBuffer[bar] = a + (b * bar)
        UpDnBuffer[bar] = DnUpBuffer[bar]
        LineBuffer[bar] = UpDnBuffer[bar]
    else:
        bar = _range_end(bar, min_rates_total, 1)
    if UserPrice == MODE_CLOSE_:
        bar = 0
        for bar in range(bar, min_rates_total):
            h = MathMax(h, close[bar] - LineBuffer[bar])
            l = MathMax(l, LineBuffer[bar] - close[bar])
        else:
            bar = _range_end(bar, min_rates_total, 1)
    else:
        bar = 0
        for bar in range(bar, min_rates_total):
            h = MathMax(h, high[bar] - LineBuffer[bar])
            l = MathMax(l, LineBuffer[bar] - low[bar])
        else:
            bar = _range_end(bar, min_rates_total, 1)
    if h > l:
        res = h
    else:
        res = l
    bar = 0
    for bar in range(bar, min_rates_total):
        DnDnBuffer[bar] = a - res + (b * bar)
        SupBuffer[bar] = DnDnBuffer[bar]
        UpUpBuffer[bar] = a + res + (b * bar)
        ResBuffer[bar] = UpUpBuffer[bar]
    else:
        bar = _range_end(bar, min_rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class LinearRegressionChannelCloud(_MQL5Indicator):
    name = 'LinearRegressionChannel_Cloud'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'UserPrice': _Choice({0: 'Используем close', 1: 'Используем high и low'}, default=0),  # Вариант цен
        'barsToCount': 100,  # Количество баров для расчёта
    }

