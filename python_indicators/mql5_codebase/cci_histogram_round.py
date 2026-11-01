"""CCI_Histogram_Round — converted from MQL5: MQL5 Indicators/CCI_Histogram_Round/CCI_Histogram_Round.mq5

Copyright: Copyright © 2016, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2016, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.01', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [16711680, 7059389, 11823615]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'CCI_Histogram'}, 'levels': [], 'description': [], 'name': 'CCI_Histogram_Round', 'source': 'MQL5 Indicators/CCI_Histogram_Round/CCI_Histogram_Round.mq5', 'folder': 'CCI_Histogram_Round', 'inputs': [{'mql': 'CCIPeriod', 'py': 'CCIPeriod', 'param': 'CCIPeriod', 'type': 'uint', 'default': 14, 'label': 'период индикатора', 'sinput': False}, {'mql': 'CCIPrice', 'py': 'CCIPrice', 'param': 'CCIPrice', 'type': 'int', 'default': 1, 'label': 'цена', 'sinput': False}, {'mql': 'HighLevel', 'py': 'HighLevel', 'param': 'HighLevel', 'type': 'int', 'default': 100, 'label': 'уровень перезакупа', 'sinput': False}, {'mql': 'LowLevel', 'py': 'LowLevel', 'param': 'LowLevel', 'type': 'int', 'default': -100, 'label': 'уровень перепроданности', 'sinput': False}, {'mql': 'Round', 'py': 'Round', 'param': 'Round', 'type': 'int', 'default': 2, 'label': 'уровень округления', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENAM_ROUND_MODE
X1 = 0
X2 = 1
X5 = 2
X10 = 3
X20 = 4
X50 = 5
_enum('ENAM_ROUND_MODE', {0: 'X1', 1: 'X2', 2: 'X5', 3: 'X10', 4: 'X20', 5: 'X50'})

# ---- inputs and global variables
CCIPeriod = _input('CCIPeriod', 14)  # период индикатора
CCIPrice = _input('CCIPrice', PRICE_CLOSE)  # цена
HighLevel = _input('HighLevel', 100)  # уровень перезакупа
LowLevel = _input('LowLevel', -100)  # уровень перепроданности
Round = _input('Round', X5)  # уровень округления
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
nRound = 0
min_rates_total = 0
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
CCI_Handle = 0

def OnInit():
    global CCI_Handle, min_rates_total, nRound
    min_rates_total = _int(CCIPeriod)
    nRound = _int(StringToInteger(StringSubstr(EnumToString(Round, 'ENAM_ROUND_MODE'), 1, -1)))
    CCI_Handle = iCCI(None, 0, CCIPeriod, CCIPrice)
    if CCI_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iCCI')
        return INIT_FAILED
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'CCI_Histogram(' + _str(CCIPeriod) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, HighLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, 0)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, LowLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrTeal)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, clrPurple)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_DASHDOTDOT)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    if BarsCalculated(CCI_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(CCI_Handle, 0, 0, to_copy, IndBuffer) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        CCI = IndBuffer[bar]
        if CCI < 0:
            IndBuffer[bar] = nRound * MathCeil(_fdiv(CCI, nRound))
        elif CCI > 0:
            IndBuffer[bar] = nRound * MathFloor(_fdiv(CCI, nRound))
        clr = _int(1.0)
        if IndBuffer[bar] > HighLevel:
            clr = _int(0.0)
        elif IndBuffer[bar] < LowLevel:
            clr = _int(2.0)
        ColorIndBuffer[bar] = clr
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CCIHistogramRound(_MQL5Indicator):
    name = 'CCI_Histogram_Round'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'CCIPeriod': 14,  # период индикатора
        'CCIPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # цена
        'HighLevel': 100,  # уровень перезакупа
        'LowLevel': -100,  # уровень перепроданности
        'Round': _Choice({0: '1', 1: '2', 2: '5', 3: '10', 4: '20', 5: '50'}, default=2),  # уровень округления
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

