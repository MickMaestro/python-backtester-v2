"""colormarsi-trigger — converted from MQL5: MQL5 Indicators/ColorMaRsi-Trigger_HTF/colormarsi-trigger.mq5

Copyright: Copyright © 2010, fx-system@mail.ru; Link: fx-system@mail.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2010, fx-system@mail.ru', 'link': 'fx-system@mail.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [16711935, 14772545]}, 'widths': {}, 'styles': {}, 'labels': {1: 'MaRsi-Trigger'}, 'levels': [], 'description': [], 'name': 'colormarsi-trigger', 'source': 'MQL5 Indicators/ColorMaRsi-Trigger_HTF/colormarsi-trigger.mq5', 'folder': 'ColorMaRsi-Trigger_HTF', 'inputs': [{'mql': 'nPeriodRsi', 'py': 'nPeriodRsi', 'param': 'nPeriodRsi', 'type': 'uint', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'nRSIPrice', 'py': 'nRSIPrice', 'param': 'nRSIPrice', 'type': 'int', 'default': 7, 'label': '', 'sinput': False}, {'mql': 'nPeriodRsiLong', 'py': 'nPeriodRsiLong', 'param': 'nPeriodRsiLong', 'type': 'uint', 'default': 13, 'label': '', 'sinput': False}, {'mql': 'nRSIPriceLong', 'py': 'nRSIPriceLong', 'param': 'nRSIPriceLong', 'type': 'int', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'nPeriodMa', 'py': 'nPeriodMa', 'param': 'nPeriodMa', 'type': 'uint', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'nMAType', 'py': 'nMAType', 'param': 'nMAType', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'nMAPrice', 'py': 'nMAPrice', 'param': 'nMAPrice', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'nPeriodMaLong', 'py': 'nPeriodMaLong', 'param': 'nPeriodMaLong', 'type': 'uint', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'nMATypeLong', 'py': 'nMATypeLong', 'param': 'nMATypeLong', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'nMAPriceLong', 'py': 'nMAPriceLong', 'param': 'nMAPriceLong', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
nPeriodRsi = _input('nPeriodRsi', 3)
nRSIPrice = _input('nRSIPrice', PRICE_WEIGHTED)
nPeriodRsiLong = _input('nPeriodRsiLong', 13)
nRSIPriceLong = _input('nRSIPriceLong', PRICE_MEDIAN)
nPeriodMa = _input('nPeriodMa', 5)
nMAType = _input('nMAType', MODE_EMA)
nMAPrice = _input('nMAPrice', PRICE_CLOSE)
nPeriodMaLong = _input('nPeriodMaLong', 10)
nMATypeLong = _input('nMATypeLong', MODE_EMA)
nMAPriceLong = _input('nMAPriceLong', PRICE_CLOSE)
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
ExtMapBuffer = Arr(0, 0.0)
ExtZerBuffer = Arr(0, 0.0)
min_rates_total = 0
MA_Handle = 0
RSI_Handle = 0
MAl_Handle = 0
RSIl_Handle = 0

def OnInit():
    global MA_Handle, MAl_Handle, RSI_Handle, RSIl_Handle, min_rates_total
    RSI_Handle = iRSI(None, 0, nPeriodRsi, nRSIPrice)
    if RSI_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iRSI')
    RSIl_Handle = iRSI(None, 0, nPeriodRsiLong, nRSIPriceLong)
    if RSIl_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iRSIl')
    MA_Handle = iMA(None, 0, nPeriodMa, 0, nMAType, nMAPrice)
    if MA_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMA')
    MAl_Handle = iMA(None, 0, nPeriodMaLong, 0, nMATypeLong, nMAPriceLong)
    if MAl_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMAl')
    min_rates_total = _int(MathMax(MathMax(MathMax(nPeriodRsi, nPeriodRsiLong), nPeriodMa), nPeriodMaLong))
    SetIndexBuffer(0, ExtZerBuffer, INDICATOR_DATA)
    ArraySetAsSeries(ExtZerBuffer, True)
    SetIndexBuffer(1, ExtMapBuffer, INDICATOR_DATA)
    ArraySetAsSeries(ExtMapBuffer, True)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = 'MaRsi-Trigger()'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (((BarsCalculated(MA_Handle) < rates_total or BarsCalculated(MAl_Handle) < rates_total) or BarsCalculated(RSI_Handle) < rates_total) or BarsCalculated(RSIl_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    res = 0.0
    MA_ = Arr(0, 0.0)
    MAl_ = Arr(0, 0.0)
    RSI_ = Arr(0, 0.0)
    RSIl_ = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(MA_Handle, 0, 0, to_copy, MA_) <= 0:
        return 0
    if CopyBuffer(MAl_Handle, 0, 0, to_copy, MAl_) <= 0:
        return 0
    if CopyBuffer(RSI_Handle, 0, 0, to_copy, RSI_) <= 0:
        return 0
    if CopyBuffer(RSIl_Handle, 0, 0, to_copy, RSIl_) <= 0:
        return 0
    ArraySetAsSeries(MA_, True)
    ArraySetAsSeries(MAl_, True)
    ArraySetAsSeries(RSI_, True)
    ArraySetAsSeries(RSIl_, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        res = 0.0
        if MA_[bar] > MAl_[bar]:
            res = 1.0
        if MA_[bar] < MAl_[bar]:
            res = -1.0
        if RSI_[bar] > RSIl_[bar]:
            res += 1
        if RSI_[bar] < RSIl_[bar]:
            res -= 1
        ExtMapBuffer[bar] = MathMax(MathMin(1, res), -1)
        ExtZerBuffer[bar] = 0.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ColormarsiTrigger(_MQL5Indicator):
    name = 'colormarsi-trigger'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'nPeriodRsi': 3,
        'nRSIPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=7),
        'nPeriodRsiLong': 13,
        'nRSIPriceLong': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=5),
        'nPeriodMa': 5,
        'nMAType': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),
        'nMAPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'nPeriodMaLong': 10,
        'nMATypeLong': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),
        'nMAPriceLong': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

