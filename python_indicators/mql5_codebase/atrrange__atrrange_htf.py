"""atrrange — converted from MQL5: MQL5 Indicators/AtrRange_HTF/atrrange.mq5

Copyright: Copyright © 2011, raxxla; Link: http://www.cmetrading.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, raxxla', 'link': 'http://www.cmetrading.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 5, 2: 5, 3: 5}, 'colors': {1: [16711680], 2: [255], 3: [55295]}, 'widths': {1: 3, 2: 3, 3: 3}, 'styles': {1: 0}, 'labels': {1: 'HiRange', 2: 'LoRange', 3: 'MultiRange'}, 'levels': [], 'description': [], 'name': 'atrrange', 'source': 'MQL5 Indicators/AtrRange_HTF/atrrange.mq5', 'folder': 'AtrRange_HTF', 'inputs': [{'mql': 'MaxRange', 'py': 'MaxRange', 'param': 'MaxRange', 'type': 'uint', 'default': 25, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
MaxRange = _input('MaxRange', 25)
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
HiRangeBuffer = Arr(0, 0.0)
LoRangeBuffer = Arr(0, 0.0)
MRangeBuffer = Arr(0, 0.0)
ATR_Handle = Arr(5, 0, dyn=False)
min_rates_total = 0
Atr_Start = 0
Atr_Step = 0
MA = 0
pt = 0
ATR1 = Arr(0, 0.0)
ATR2 = Arr(0, 0.0)
ATR3 = Arr(0, 0.0)
ATR4 = Arr(0, 0.0)
ATR5 = Arr(0, 0.0)

def OnInit():
    global Atr_Start, Atr_Step, MA, min_rates_total, pt
    Atr_Start = 3
    Atr_Step = 2
    MA = 14
    pt = 1
    if Digits() == 5 or Digits() == 3:
        pt = 10
    min_rates_total = Atr_Start + (Atr_Step * 5) + 3 + MA
    ATR_Handle[0] = iATR(None, PERIOD_CURRENT, Atr_Start + (Atr_Step * 1))
    if ATR_Handle[0] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR1')
        return INIT_FAILED
    ATR_Handle[1] = iATR(None, PERIOD_CURRENT, Atr_Start + (Atr_Step * 2))
    if ATR_Handle[1] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR2')
        return INIT_FAILED
    ATR_Handle[2] = iATR(None, PERIOD_CURRENT, Atr_Start + (Atr_Step * 3))
    if ATR_Handle[2] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR3')
        return INIT_FAILED
    ATR_Handle[3] = iATR(None, PERIOD_CURRENT, Atr_Start + (Atr_Step * 4))
    if ATR_Handle[3] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR4')
        return INIT_FAILED
    ATR_Handle[4] = iATR(None, PERIOD_CURRENT, Atr_Start + (Atr_Step * 5))
    if ATR_Handle[4] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR5')
        return INIT_FAILED
    ArraySetAsSeries(ATR1, True)
    ArraySetAsSeries(ATR2, True)
    ArraySetAsSeries(ATR3, True)
    ArraySetAsSeries(ATR4, True)
    ArraySetAsSeries(ATR5, True)
    SetIndexBuffer(0, HiRangeBuffer, INDICATOR_DATA)
    ArraySetAsSeries(HiRangeBuffer, True)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetInteger(0, PLOT_ARROW, 159)
    SetIndexBuffer(1, LoRangeBuffer, INDICATOR_DATA)
    ArraySetAsSeries(LoRangeBuffer, True)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetInteger(1, PLOT_ARROW, 159)
    SetIndexBuffer(2, MRangeBuffer, INDICATOR_DATA)
    ArraySetAsSeries(MRangeBuffer, True)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetInteger(2, PLOT_ARROW, 162)
    shortname = Box("")
    StringConcatenate(shortname, 'AtrRange(', MaxRange, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if ((((BarsCalculated(ATR_Handle[0]) < rates_total or BarsCalculated(ATR_Handle[1]) < rates_total) or BarsCalculated(ATR_Handle[2]) < rates_total) or BarsCalculated(ATR_Handle[3]) < rates_total) or BarsCalculated(ATR_Handle[4]) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(ATR_Handle[0], 0, 0, to_copy + 1, ATR1) <= 0:
        return 0
    if CopyBuffer(ATR_Handle[1], 0, 0, to_copy, ATR2) <= 0:
        return 0
    if CopyBuffer(ATR_Handle[2], 0, 0, to_copy + MA, ATR3) <= 0:
        return 0
    if CopyBuffer(ATR_Handle[3], 0, 0, to_copy, ATR4) <= 0:
        return 0
    if CopyBuffer(ATR_Handle[4], 0, 0, to_copy, ATR5) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if AtrRange(bar, MaxRange * pt, high, low):
            HiRangeBuffer[bar] = high[bar] + (Point() * 3)
            LoRangeBuffer[bar] = low[bar] - (Point() * 3)
        else:
            HiRangeBuffer[bar] = 0.0
            LoRangeBuffer[bar] = 0.0
        if AtrBreakIn(bar, high, low):
            MRangeBuffer[bar] = (high[bar] + low[bar]) / 2
        else:
            MRangeBuffer[bar] = 0.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

def AtrBreakIn(index, High, Low):
    vlt1 = _fdiv(High[index] - Low[index], Point()) + Point()
    vlt2 = _fdiv(High[index + 1] - Low[index + 1], Point()) + Point()
    if _fdiv(vlt1, vlt2) > 1.5:
        return False
    max_ = MathMax(ATR2[index], MathMax(ATR3[index], MathMax(ATR4[index], ATR5[index])))
    min_ = MathMin(ATR2[index], MathMin(ATR3[index], MathMin(ATR4[index], ATR5[index])))
    summ = 0.0
    for iii in range(0, MA):
        summ += ATR3[index + iii]
    atrMa3 = _fdiv(summ, MA)
    if max_ > atrMa3:
        return False
    if _fdiv(max_ - min_, Point()) > (25 * pt):
        return False
    atr1 = ATR1[index]
    if atr1 < min_ or atr1 > atrMa3:
        return False
    if atr1 < ATR1[index + 1]:
        return False
    if atr1 >= ATR5[index]:
        return False
    return True

def AtrRange(index, maxRange, High, Low):
    vlt1 = _fdiv(High[index] - Low[index], Point()) + Point()
    vlt2 = _fdiv(High[index + 1] - Low[index + 1], Point()) + Point()
    vlt3 = _fdiv(High[index + 2] - Low[index + 2], Point()) + Point()
    if vlt1 > maxRange:
        return False
    if _fdiv(vlt3, vlt2) > 1.8:
        return False
    if (vlt1 > vlt2 or vlt2 > vlt3) or vlt1 > vlt3:
        return False
    if (High[index] - High[index + 1]) > Point():
        return False
    if (High[index + 1] - High[index + 2]) > Point():
        return False
    if (Low[index + 1] - Low[index]) > Point():
        return False
    if (Low[index + 2] - Low[index + 1]) > Point():
        return False
    return True


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Atrrange(_MQL5Indicator):
    name = 'atrrange'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MaxRange': 25,
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

