"""FineTuningMACandle — converted from MQL5: MQL5 Indicators/FineTuningMACandle_HTF/FineTuningMACandle.mq5

Свечной график на более тонком усреднении таймсерий
Copyright: Copyright © 2018, gumgum; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, gumgum', 'link': '', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [9639167, 8421504, 15570276]}, 'widths': {}, 'styles': {}, 'labels': {1: 'FineTuningMA Open;FineTuningMA High;FineTuningMA Low;FineTuningMA Close'}, 'levels': [], 'description': ['Свечной график на более тонком усреднении таймсерий'], 'name': 'FineTuningMACandle', 'source': 'MQL5 Indicators/FineTuningMACandle_HTF/FineTuningMACandle.mq5', 'folder': 'FineTuningMACandle_HTF', 'inputs': [{'mql': 'FTMA', 'py': 'FTMA', 'param': 'FTMA', 'type': 'uint', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'rank1', 'py': 'rank1', 'param': 'rank1', 'type': 'double', 'default': 2.0, 'label': '', 'sinput': False}, {'mql': 'rank2', 'py': 'rank2', 'param': 'rank2', 'type': 'double', 'default': 2.0, 'label': '', 'sinput': False}, {'mql': 'rank3', 'py': 'rank3', 'param': 'rank3', 'type': 'double', 'default': 2.0, 'label': '', 'sinput': False}, {'mql': 'shift1', 'py': 'shift1', 'param': 'shift1', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'shift2', 'py': 'shift2', 'param': 'shift2', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'shift3', 'py': 'shift3', 'param': 'shift3', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'cдвиг индикатора по вертикали в пунктах', 'sinput': False}, {'mql': 'Gap', 'py': 'Gap', 'param': 'Gap', 'type': 'uint', 'default': 10, 'label': 'размер неучитываемого гэпа в пунктах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
FTMA = _input('FTMA', 10)
rank1 = _input('rank1', 2.0)
rank2 = _input('rank2', 2.0)
rank3 = _input('rank3', 2.0)
shift1 = _input('shift1', 1.0)
shift2 = _input('shift2', 1.0)
shift3 = _input('shift3', 1.0)
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
PriceShift = _input('PriceShift', 0)  # cдвиг индикатора по вертикали в пунктах
Gap = _input('Gap', 10)  # размер неучитываемого гэпа в пунктах
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
PM = Arr(0, 0.0)
dPriceShift = 0.0
min_rates_total = 0

def OnInit():
    global dPriceShift, min_rates_total
    dPriceShift = Point() * PriceShift
    ArrayResize(PM, FTMA)
    sum_ = 0.0
    for h in range(0, _int(FTMA)):
        PM[h] = shift1 + (MathPow(_fdiv(h, FTMA - 1.0), rank1) * (1.0 - shift1))
        PM[h] = (shift2 + (MathPow(1 - _fdiv(h, FTMA - 1.0), rank2) * (1.0 - shift2))) * PM[h]
        if _fdiv(h, FTMA - 1.0) < 0.5:
            PM[h] = (shift3 + (MathPow(1 - (_fdiv(h, FTMA - 1.0) * 2.0), rank3) * (1.0 - shift3))) * PM[h]
        else:
            PM[h] = (shift3 + (MathPow((_fdiv(h, FTMA - 1.0) * 2.0) - 1.0, rank3) * (1.0 - shift3))) * PM[h]
        sum_ += PM[h]
    sum1 = 0.0
    for h in range(0, _int(FTMA)):
        PM[h] = _fdiv(PM[h], sum_)
        sum1 += PM[h]
    min_rates_total = _int(FTMA) + 1
    SetIndexBuffer(0, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    IndicatorSetString(INDICATOR_SHORTNAME, 'FineTuningMACandle(' + _str(FTMA) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    O = 0.0
    H = 0.0
    L = 0.0
    C = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        O = 0.0
        for index in range(0, _int(FTMA)):
            O += PM[index] * open[bar - index]
        H = 0.0
        for index in range(0, _int(FTMA)):
            H += PM[index] * high[bar - index]
        L = 0.0
        for index in range(0, _int(FTMA)):
            L += PM[index] * low[bar - index]
        C = 0.0
        for index in range(0, _int(FTMA)):
            C += PM[index] * close[bar - index]
        Max = MathMax(O, C)
        Max = MathMax(Max, L)
        Max = MathMax(Max, H)
        Min = MathMin(O, C)
        Min = MathMin(Min, L)
        Min = MathMin(Min, H)
        ExtOpenBuffer[bar] = O
        ExtHighBuffer[bar] = Max
        ExtLowBuffer[bar] = Min
        ExtCloseBuffer[bar] = C
        if MathAbs(open[bar] - close[bar]) <= Gap:
            ExtOpenBuffer[bar] = ExtCloseBuffer[MathMax(bar - 1, 0)]
        if ExtOpenBuffer[bar] < ExtCloseBuffer[bar]:
            ExtColorBuffer[bar] = 2.0
        elif ExtOpenBuffer[bar] > ExtCloseBuffer[bar]:
            ExtColorBuffer[bar] = 0.0
        else:
            ExtColorBuffer[bar] = 1.0
        ExtOpenBuffer[bar] += dPriceShift
        ExtHighBuffer[bar] += dPriceShift
        ExtLowBuffer[bar] += dPriceShift
        ExtCloseBuffer[bar] += dPriceShift
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

def PriceSeries(applied_price, bar, Open, Low, High, Close):
    _sw1 = applied_price
    if _sw1 == PRICE_CLOSE:
        return Close[bar]
    elif _sw1 == PRICE_OPEN:
        return Open[bar]
    elif _sw1 == PRICE_HIGH:
        return High[bar]
    elif _sw1 == PRICE_LOW:
        return Low[bar]
    elif _sw1 == PRICE_MEDIAN:
        return (High[bar] + Low[bar]) / 2.0
    elif _sw1 == PRICE_TYPICAL:
        return (Close[bar] + High[bar] + Low[bar]) / 3.0
    elif _sw1 == PRICE_WEIGHTED:
        return ((2 * Close[bar]) + High[bar] + Low[bar]) / 4.0
    elif _sw1 == 8:
        return (Open[bar] + Close[bar]) / 2.0
    elif _sw1 == 9:
        return (Open[bar] + Close[bar] + High[bar] + Low[bar]) / 4.0
    elif _sw1 == 10:
        if Close[bar] > Open[bar]:
            return High[bar]
        else:
            if Close[bar] < Open[bar]:
                return Low[bar]
            else:
                return Close[bar]
    elif _sw1 == 11:
        if Close[bar] > Open[bar]:
            return (High[bar] + Close[bar]) / 2.0
        else:
            if Close[bar] < Open[bar]:
                return (Low[bar] + Close[bar]) / 2.0
            else:
                return Close[bar]
    else:
        return Close[bar]


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FineTuningMACandle(_MQL5Indicator):
    name = 'FineTuningMACandle'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'FTMA': 10,
        'rank1': 2.0,
        'rank2': 2.0,
        'rank3': 2.0,
        'shift1': 1.0,
        'shift2': 1.0,
        'shift3': 1.0,
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
        'PriceShift': 0,  # cдвиг индикатора по вертикали в пунктах
        'Gap': 10,  # размер неучитываемого гэпа в пунктах
    }

