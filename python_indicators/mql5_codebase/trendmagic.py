"""trendmagic — converted from MQL5: MQL5 Indicators/TrendMagic/trendmagic.mq5

Copyright: Sergey Gritsai; Link: sergey1294@list.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Sergey Gritsai', 'link': 'sergey1294@list.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [16711680, 255]}, 'widths': {1: 2}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'trendmagic', 'source': 'MQL5 Indicators/TrendMagic/trendmagic.mq5', 'folder': 'TrendMagic', 'inputs': [{'mql': 'CCI_Period', 'py': 'CCI_Period', 'param': 'CCI_Period', 'type': 'int', 'default': 50, 'label': '', 'sinput': False}, {'mql': 'ATR_Period', 'py': 'ATR_Period', 'param': 'ATR_Period', 'type': 'int', 'default': 5, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
CCI_Period = _input('CCI_Period', 50)
ATR_Period = _input('ATR_Period', 5)
Buffer = Arr(0, 0.0)
Color = Arr(0, 0.0)
CCI = Arr(0, 0.0)
ATR = Arr(0, 0.0)
Hcci = INVALID_HANDLE
Hatr = INVALID_HANDLE

def OnInit():
    global Hatr, Hcci
    SetIndexBuffer(0, Buffer, INDICATOR_DATA)
    SetIndexBuffer(1, Color, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, CCI, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, ATR, INDICATOR_CALCULATIONS)
    ArrayInitialize(Buffer, 0.0)
    ArrayInitialize(CCI, 0.0)
    ArrayInitialize(ATR, 0.0)
    Hcci = iCCI(Symbol(), Period(), CCI_Period, PRICE_TYPICAL)
    Hatr = iATR(Symbol(), Period(), ATR_Period)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global Hatr, Hcci
    if rates_total < CCI_Period or rates_total < ATR_Period:
        return rates_total
    if Hcci == INVALID_HANDLE or Hcci == 0:
        Hcci = iCCI(Symbol(), Period(), CCI_Period, PRICE_TYPICAL)
        return rates_total
    if Hatr == INVALID_HANDLE or Hatr == 0:
        Hatr = iATR(Symbol(), Period(), ATR_Period)
        return rates_total
    calculated1 = BarsCalculated(Hcci)
    calculated2 = BarsCalculated(Hatr)
    to_copy = MathMin(calculated1, calculated2)
    if to_copy < 0:
        return rates_total
    if CopyBuffer(Hcci, 0, 0, to_copy, CCI) < to_copy:
        return rates_total
    if CopyBuffer(Hatr, 0, 0, to_copy, ATR) < to_copy:
        return rates_total
    ArraySetAsSeries(CCI, True)
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(Buffer, True)
    ArraySetAsSeries(Color, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(high, True)
    for i in range(rates_total - 2, 0 - 1, -1):
        if CCI[i] >= 0.0:
            Buffer[i] = low[i] - ATR[i]
            if Buffer[i] < Buffer[i + 1]:
                Buffer[i] = Buffer[i + 1]
            Color[i] = 0.0
        elif CCI[i] < 0.0:
            Buffer[i] = high[i] + ATR[i]
            if Buffer[i] > Buffer[i + 1]:
                Buffer[i] = Buffer[i + 1]
            Color[i] = 1.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Trendmagic(_MQL5Indicator):
    name = 'trendmagic'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'CCI_Period': 50,
        'ATR_Period': 5,
    }

