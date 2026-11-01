"""momentum_ama — converted from MQL5: MQL5 Indicators/ColorMomentum_AMA/momentum_ama.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 3}, 'colors': {1: [14822282]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Momentum_AMA'}, 'levels': [], 'description': [], 'name': 'momentum_ama', 'source': 'MQL5 Indicators/ColorMomentum_AMA/momentum_ama.mq5', 'folder': 'ColorMomentum_AMA', 'inputs': [{'mql': 'MLength', 'py': 'MLength', 'param': 'MLength', 'type': 'int', 'default': 8, 'label': 'Momentum period', 'sinput': False}, {'mql': 'AMA_Period', 'py': 'AMA_Period', 'param': 'AMA_Period', 'type': 'int', 'default': 9, 'label': 'AMA period', 'sinput': False}, {'mql': 'Fast_MA_Period', 'py': 'Fast_MA_Period', 'param': 'Fast_MA_Period', 'type': 'int', 'default': 2, 'label': 'Fast MA period', 'sinput': False}, {'mql': 'Slow_MA_Period', 'py': 'Slow_MA_Period', 'param': 'Slow_MA_Period', 'type': 'int', 'default': 30, 'label': 'Slow MA period', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Price constant', 'sinput': False}, {'mql': 'G', 'py': 'G', 'param': 'G', 'type': 'double', 'default': 2.0, 'label': 'A power the smoothing constant is raised to', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPL_ = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'})

# ---- inputs and global variables
MLength = _input('MLength', 8)  # Momentum period
AMA_Period = _input('AMA_Period', 9)  # AMA period
Fast_MA_Period = _input('Fast_MA_Period', 2)  # Fast MA period
Slow_MA_Period = _input('Slow_MA_Period', 30)  # Slow MA period
IPC = _input('IPC', PRICE_CLOSE_)  # Price constant
G = _input('G', 2.0)  # A power the smoothing constant is raised to
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
MomentumBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, MomentumBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, 0)
    PlotIndexSetString(0, PLOT_LABEL, 'Momentum_AMA')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    StringConcatenate(shortname, 'Momentum_AMA( MLength = ', MLength, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    Mom = CMomentum()
    Mom.MALengthCheck_1('MLength', MLength)
    Mom.MALengthCheck_1('AMA_Period', AMA_Period)
    Mom.MALengthCheck_1('Fast_MA_Period', Fast_MA_Period)
    Mom.MALengthCheck_1('Slow_MA_Period', Slow_MA_Period)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < (MLength + AMA_Period + 1):
        return 0
    price = 0.0
    momentum = 0.0
    amomentum = 0.0
    first = 0
    bar = 0
    if prev_calculated == 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price = PriceSeries(IPC, bar, open, low, high, close)
        momentum = _s_OnCalculate_Mom.MomentumSeries(0, prev_calculated, rates_total, MLength, price, bar, False)
        amomentum = _s_OnCalculate_AMA.AMASeries(MLength + 1, prev_calculated, rates_total, AMA_Period, Fast_MA_Period, Slow_MA_Period, G, momentum, bar, False)
        MomentumBuffer[bar] = _fdiv(amomentum, Point())
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_OnCalculate_Mom = CMomentum()
_s_OnCalculate_AMA = CAMA()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MomentumAma(_MQL5Indicator):
    name = 'momentum_ama'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MLength': 8,  # Momentum period
        'AMA_Period': 9,  # AMA period
        'Fast_MA_Period': 2,  # Fast MA period
        'Slow_MA_Period': 30,  # Slow MA period
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simple Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price'}, default=1),  # Price constant
        'G': 2.0,  # A power the smoothing constant is raised to
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

