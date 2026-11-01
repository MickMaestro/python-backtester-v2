"""sumrsi — converted from MQL5: MQL5 Indicators/SumRSI/sumrsi.mq5

Copyright: Copyright © 2008, jax1000; Link: jax1000@list.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2008, jax1000', 'link': 'jax1000@list.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1, 'indicator_minimum': 0.0, 'indicator_maximum': 100.0}, 'types': {1: 1}, 'colors': {1: [36095]}, 'widths': {1: 3}, 'styles': {1: 0}, 'labels': {1: 'SumRSI'}, 'levels': [70.0, 50.0, 30.0], 'description': [], 'name': 'sumrsi', 'source': 'MQL5 Indicators/SumRSI/sumrsi.mq5', 'folder': 'SumRSI', 'inputs': [{'mql': 'StartLength', 'py': 'StartLength', 'param': 'StartLength', 'type': 'uint', 'default': 3, 'label': 'initial smoothing period', 'sinput': False}, {'mql': 'EndLength', 'py': 'EndLength', 'param': 'EndLength', 'type': 'uint', 'default': 25, 'label': 'final smoothing period', 'sinput': False}, {'mql': 'Applied_Price', 'py': 'Applied_Price', 'param': 'Applied_Price', 'type': 'int', 'default': 1, 'label': 'type of price', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
StartLength = _input('StartLength', 3)  # initial smoothing period
EndLength = _input('EndLength', 25)  # final smoothing period
Applied_Price = _input('Applied_Price', PRICE_CLOSE)  # type of price
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
SumRSIBuffer = Arr(0, 0.0)
Init = False
RSI_Handle = Arr(0, 0)
min_rates_total = 0
xSize = 0

class CRSI(MqlObject):
    _q_fields = ('m_RSI',)
    def __init__(self, *args):
        self.m_RSI = Arr(0, 0.0)

def OnInit():
    global Init, min_rates_total, xSize
    if StartLength > EndLength:
        Init = False
        Print('The initial period of the indicator can not be greater than the final period!')
        return
    xSize = _int(EndLength - StartLength + 1)
    if ArrayResize(RSI_Handle, xSize) < xSize:
        Init = False
        Print('Failed to distribute the memory for RSI_Handle[] array!')
        return
    if ArrayResize(RSI, xSize) < xSize:
        Init = False
        Print('Failed to distribute the memory for RSI[] object array!')
        return
    else:
        Init = True
    for count in range(0, xSize):
        ArraySetAsSeries(RSI[count].m_RSI, True)
    for count in range(0, xSize):
        RSI_Handle[count] = iRSI(None, PERIOD_CURRENT, StartLength + count, Applied_Price)
        if RSI_Handle[count] == INVALID_HANDLE:
            Print(' Failed to get handle of the iRSI indicator')
            Init = False
            return
    min_rates_total = _int(EndLength)
    SetIndexBuffer(0, SumRSIBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(SumRSIBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'SumRSI(', StartLength, ', ', EndLength, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (not Init) or rates_total < min_rates_total:
        return 0
    for count in range(0, xSize):
        if BarsCalculated(RSI_Handle[count]) < rates_total:
            return 0
    limit = 0
    bar = 0
    to_copy = 0
    Sum = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    for count in range(0, xSize):
        if CopyBuffer(RSI_Handle[count], 0, 0, to_copy, RSI[count].m_RSI) <= 0:
            return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        Sum = 0.0
        for count in range(0, xSize):
            Sum += RSI[count].m_RSI[bar]
        SumRSIBuffer[bar] = Sum / (EndLength - StartLength + 1)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- global variables initialised from expressions
RSI = Arr(0, 0, factory=CRSI)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Sumrsi(_MQL5Indicator):
    name = 'sumrsi'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'StartLength': 3,  # initial smoothing period
        'EndLength': 25,  # final smoothing period
        'Applied_Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # type of price
        'Shift': 0,  # horizontal shift of the indicator in bars
    }
    y_range = (0.0, 100.0)

