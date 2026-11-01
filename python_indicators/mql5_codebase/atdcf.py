"""atdcf — converted from MQL5: MQL5 Indicators/AT_CF/atdcf.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 1, 4: 1}, 'colors': {1: [16711680], 2: [255], 3: [16711935], 4: [65280]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'FATL', 2: 'SATL', 3: 'RFTL', 4: 'RSTL'}, 'levels': [], 'description': [], 'name': 'atdcf', 'source': 'MQL5 Indicators/AT_CF/atdcf.mq5', 'folder': 'AT_CF', 'inputs': [{'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Price constant', 'sinput': False}, {'mql': 'FATLShift', 'py': 'FATLShift', 'param': 'FATLShift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the FATL indicator in bars', 'sinput': False}, {'mql': 'SATLShift', 'py': 'SATLShift', 'param': 'SATLShift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the SATL indicator in bars', 'sinput': False}, {'mql': 'RFTLShift', 'py': 'RFTLShift', 'param': 'RFTLShift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the RFTL indicator in bars', 'sinput': False}, {'mql': 'RSTLShift', 'py': 'RSTLShift', 'param': 'RSTLShift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the RSTL indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPLE = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPLE', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'})

# ---- inputs and global variables
IPC = _input('IPC', PRICE_CLOSE_)  # Price constant
FATLShift = _input('FATLShift', 0)  # Horizontal shift of the FATL indicator in bars
SATLShift = _input('SATLShift', 0)  # Horizontal shift of the SATL indicator in bars
RFTLShift = _input('RFTLShift', 0)  # Horizontal shift of the RFTL indicator in bars
RSTLShift = _input('RSTLShift', 0)  # Horizontal shift of the RSTL indicator in bars
FATLBuffer = Arr(0, 0.0)
SATLBuffer = Arr(0, 0.0)
RFTLBuffer = Arr(0, 0.0)
RSTLBuffer = Arr(0, 0.0)
start = 0

def OnInit():
    global start
    start = 99
    SetIndexBuffer(0, FATLBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, SATLBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, RFTLBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, RSTLBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, FATLShift)
    PlotIndexSetInteger(1, PLOT_SHIFT, SATLShift)
    PlotIndexSetInteger(2, PLOT_SHIFT, RFTLShift)
    PlotIndexSetInteger(3, PLOT_SHIFT, RSTLShift)
    PlotIndexSetString(0, PLOT_LABEL, 'FATL')
    PlotIndexSetString(1, PLOT_LABEL, 'SATL')
    PlotIndexSetString(2, PLOT_LABEL, 'RFTL')
    PlotIndexSetString(3, PLOT_LABEL, 'RSTL')
    IndicatorSetString(INDICATOR_SHORTNAME, 'AT^CF')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < start:
        return 0
    first = 0
    bar = 0
    price = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price = PriceSeries(IPC, bar, open, low, high, close)
        FATLBuffer[bar] = _s_OnCalculate_FATL.FATLSeries(0, prev_calculated, rates_total, price, bar, False)
        SATLBuffer[bar] = _s_OnCalculate_SATL.SATLSeries(0, prev_calculated, rates_total, price, bar, False)
        RFTLBuffer[bar] = _s_OnCalculate_RFTL.RFTLSeries(0, prev_calculated, rates_total, price, bar, False)
        RSTLBuffer[bar] = _s_OnCalculate_RSTL.RSTLSeries(0, prev_calculated, rates_total, price, bar, False)
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_OnCalculate_FATL = CFATL()
_s_OnCalculate_SATL = CSATL()
_s_OnCalculate_RFTL = CRFTL()
_s_OnCalculate_RSTL = CRSTL()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Atdcf(_MQL5Indicator):
    name = 'atdcf'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'IPC': _Choice({1: 'PRICE_CLOSE', 2: 'PRICE_OPEN', 3: 'PRICE_HIGH', 4: 'PRICE_LOW', 5: 'PRICE_MEDIAN', 6: 'PRICE_TYPICAL', 7: 'PRICE_WEIGHTED', 8: 'PRICE_SIMPLE', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'}, default=1),  # Price constant
        'FATLShift': 0,  # Horizontal shift of the FATL indicator in bars
        'SATLShift': 0,  # Horizontal shift of the SATL indicator in bars
        'RFTLShift': 0,  # Horizontal shift of the RFTL indicator in bars
        'RSTLShift': 0,  # Horizontal shift of the RSTL indicator in bars
    }

