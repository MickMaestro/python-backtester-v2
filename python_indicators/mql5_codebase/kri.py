"""kri — converted from MQL5: MQL5 Indicators/KRI/kri.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [55295]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'KRI'}, 'levels': [], 'description': [], 'name': 'kri', 'source': 'MQL5 Indicators/KRI/kri.mq5', 'folder': 'KRI', 'inputs': [{'mql': 'KRIPeriod', 'py': 'KRIPeriod', 'param': 'KRIPeriod', 'type': 'int', 'default': 20, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'MA_Method_', 'py': 'MA_Method_', 'param': 'MA_Method_', 'type': 'int', 'default': 0, 'label': 'Smoothing method', 'sinput': False}, {'mql': 'Ratio', 'py': 'Ratio', 'param': 'Ratio', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Price constant', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
KRIPeriod = _input('KRIPeriod', 20)  # Smoothing period
MA_Method_ = _input('MA_Method_', MODE_SMA)  # Smoothing method
Ratio = _input('Ratio', 1.0)
IPC = _input('IPC', PRICE_CLOSE_)  # Price constant
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
KRIBuffer = Arr(0, 0.0)
StartBar = 0

def OnInit():
    global StartBar
    StartBar = KRIPeriod + 1
    SetIndexBuffer(0, KRIBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, StartBar)
    PlotIndexSetString(0, PLOT_LABEL, 'KRI')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    StringConcatenate(shortname, 'KRI( KRIPeriod = ', KRIPeriod, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < StartBar:
        return 0
    price_ = 0.0
    KRI = 0.0
    mov = 0.0
    first = 0
    bar = 0
    if prev_calculated == 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price_ = PriceSeries(IPC, bar, open, low, high, close)
        mov = _s_OnCalculate_MA.MASeries(0, prev_calculated, rates_total, KRIPeriod, MA_Method_, price_, bar, False)
        KRI = _fdiv(100 * (price_ - mov), mov)
        KRIBuffer[bar] = KRI
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_OnCalculate_MA = CMoving_Average()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Kri(_MQL5Indicator):
    name = 'kri'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'KRIPeriod': 20,  # Smoothing period
        'MA_Method_': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Smoothing method
        'Ratio': 1.0,
        'IPC': _Choice({1: 'PRICE_CLOSE', 2: 'PRICE_OPEN', 3: 'PRICE_HIGH', 4: 'PRICE_LOW', 5: 'PRICE_MEDIAN', 6: 'PRICE_TYPICAL', 7: 'PRICE_WEIGHTED', 8: 'PRICE_SIMPLE', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'}, default=1),  # Price constant
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

