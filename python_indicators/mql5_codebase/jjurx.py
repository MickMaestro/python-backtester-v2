"""jjurx — converted from MQL5: MQL5 Indicators/JJurX/jjurx.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [55295]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'JJurX'}, 'levels': [], 'description': [], 'name': 'jjurx', 'source': 'MQL5 Indicators/JJurX/jjurx.mq5', 'folder': 'JJurX', 'inputs': [{'mql': 'JurX_Length', 'py': 'JurX_Length', 'param': 'JurX_Length', 'type': 'int', 'default': 5, 'label': 'Depth of the JurX smoothing', 'sinput': False}, {'mql': 'JJMA_Length', 'py': 'JJMA_Length', 'param': 'JJMA_Length', 'type': 'int', 'default': 4, 'label': 'Depth of the JJMA smoothing', 'sinput': False}, {'mql': 'JJMA_Phase', 'py': 'JJMA_Phase', 'param': 'JJMA_Phase', 'type': 'int', 'default': -100, 'label': 'Parameter of the first smoothing,', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Price constant', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'Vertical shift of the average in points', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
JurX_Length = _input('JurX_Length', 5)  # Depth of the JurX smoothing
JJMA_Length = _input('JJMA_Length', 4)  # Depth of the JJMA smoothing
JJMA_Phase = _input('JJMA_Phase', -100)  # Parameter of the first smoothing,
IPC = _input('IPC', PRICE_CLOSE_)  # Price constant
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
PriceShift = _input('PriceShift', 0)  # Vertical shift of the average in points
Ind_Buffer = Arr(0, 0.0)
dPriceShift = 0.0

def OnInit():
    global dPriceShift
    SetIndexBuffer(0, Ind_Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, 30)
    PlotIndexSetString(0, PLOT_LABEL, 'JJurX')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    StringConcatenate(shortname, 'JJurX( JurX_Length = ', JurX_Length, ', JJMA_Length = ', JJMA_Length, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    JMA = CJJMA()
    JMA.JJMALengthCheck('JJMA_Length', JJMA_Length)
    JMA.JJMALengthCheck('JurX_Length', JurX_Length)
    JMA.JJMAPhaseCheck('JJMA_Phase', JJMA_Phase)
    dPriceShift = Point() * PriceShift

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 30:
        return 0
    first = 0
    bar = 0
    series = 0.0
    jurx = 0.0
    jjurx = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        series = PriceSeries(IPC, bar, open, low, high, close)
        jurx = _s_OnCalculate_Jur.JurXSeries(0, prev_calculated, rates_total, 0, JurX_Length, series, bar, False)
        jjurx = _s_OnCalculate_JMA.JJMASeries(0, prev_calculated, rates_total, 0, JJMA_Phase, JJMA_Length, jurx, bar, False)
        Ind_Buffer[bar] = jjurx + dPriceShift
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_OnCalculate_Jur = CJurX()
_s_OnCalculate_JMA = CJJMA()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Jjurx(_MQL5Indicator):
    name = 'jjurx'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'JurX_Length': 5,  # Depth of the JurX smoothing
        'JJMA_Length': 4,  # Depth of the JJMA smoothing
        'JJMA_Phase': -100,  # Parameter of the first smoothing,
        'IPC': _Choice({1: 'PRICE_CLOSE', 2: 'PRICE_OPEN', 3: 'PRICE_HIGH', 4: 'PRICE_LOW', 5: 'PRICE_MEDIAN', 6: 'PRICE_TYPICAL', 7: 'PRICE_WEIGHTED', 8: 'PRICE_SIMPLE', 9: 'PRICE_QUARTER', 10: 'PRICE_TRENDFOLLOW0', 11: 'PRICE_TRENDFOLLOW1'}, default=1),  # Price constant
        'Shift': 0,  # Horizontal shift of the indicator in bars
        'PriceShift': 0,  # Vertical shift of the average in points
    }

