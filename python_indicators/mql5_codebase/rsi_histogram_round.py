"""RSI_Histogram_Round — converted from MQL5: MQL5 Indicators/RSI_Histogram_Round/RSI_Histogram_Round.mq5

Copyright: Copyright © 2016, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2016, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 11}, 'colors': {1: [10025880, 8421504, 255]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'RSI_Histogram'}, 'levels': [], 'description': [], 'name': 'RSI_Histogram_Round', 'source': 'MQL5 Indicators/RSI_Histogram_Round/RSI_Histogram_Round.mq5', 'folder': 'RSI_Histogram_Round', 'inputs': [{'mql': 'RSIPeriod', 'py': 'RSIPeriod', 'param': 'RSIPeriod', 'type': 'uint', 'default': 14, 'label': 'период индикатора', 'sinput': False}, {'mql': 'RSIPrice', 'py': 'RSIPrice', 'param': 'RSIPrice', 'type': 'int', 'default': 1, 'label': 'цена', 'sinput': False}, {'mql': 'HighLevel', 'py': 'HighLevel', 'param': 'HighLevel', 'type': 'uint', 'default': 60, 'label': 'уровень перезакупа', 'sinput': False}, {'mql': 'LowLevel', 'py': 'LowLevel', 'param': 'LowLevel', 'type': 'uint', 'default': 40, 'label': 'уровень перепроданности', 'sinput': False}, {'mql': 'Round', 'py': 'Round', 'param': 'Round', 'type': 'int', 'default': 2, 'label': 'уровень округления', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENAM_ROUND_MODE
X1 = 0
X2 = 1
X5 = 2
X10 = 3
X20 = 4
X50 = 5
_enum('ENAM_ROUND_MODE', {0: 'X1', 1: 'X2', 2: 'X5', 3: 'X10', 4: 'X20', 5: 'X50'})

# ---- inputs and global variables
RSIPeriod = _input('RSIPeriod', 14)  # период индикатора
RSIPrice = _input('RSIPrice', PRICE_CLOSE)  # цена
HighLevel = _input('HighLevel', 60)  # уровень перезакупа
LowLevel = _input('LowLevel', 40)  # уровень перепроданности
Round = _input('Round', X5)  # уровень округления
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
nRound = 0
min_rates_total = 0
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
ColorBuffer = Arr(0, 0.0)
RSI_Handle = 0

def OnInit():
    global RSI_Handle, min_rates_total, nRound
    min_rates_total = _int(RSIPeriod)
    nRound = _int(StringToInteger(StringSubstr(EnumToString(Round, 'ENAM_ROUND_MODE'), 1, -1)))
    RSI_Handle = iRSI(None, 0, RSIPeriod, RSIPrice)
    if RSI_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iRSI')
        return INIT_FAILED
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    ArraySetAsSeries(UpBuffer, True)
    SetIndexBuffer(1, DnBuffer, INDICATOR_DATA)
    ArraySetAsSeries(DnBuffer, True)
    SetIndexBuffer(2, ColorBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorBuffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'RSI_Histogram(' + _str(RSIPeriod) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, HighLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, 50)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, LowLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrLightBlue)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, clrMagenta)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_DASHDOTDOT)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    if BarsCalculated(RSI_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(RSI_Handle, 0, 0, to_copy, UpBuffer) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        RSI = UpBuffer[bar]
        if RSI < 50:
            UpBuffer[bar] = nRound * MathCeil(_fdiv(RSI, nRound))
        elif RSI > 50:
            UpBuffer[bar] = nRound * MathFloor(_fdiv(RSI, nRound))
        DnBuffer[bar] = 50.0
        clr = _int(1.0)
        if UpBuffer[bar] > HighLevel:
            clr = _int(0.0)
        elif UpBuffer[bar] < LowLevel:
            clr = _int(2.0)
        ColorBuffer[bar] = clr
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RSIHistogramRound(_MQL5Indicator):
    name = 'RSI_Histogram_Round'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RSIPeriod': 14,  # период индикатора
        'RSIPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # цена
        'HighLevel': 60,  # уровень перезакупа
        'LowLevel': 40,  # уровень перепроданности
        'Round': _Choice({0: '1', 1: '2', 2: '5', 3: '10', 4: '20', 5: '50'}, default=2),  # уровень округления
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

