"""inversereaction — converted from MQL5: MQL5 Indicators/InverseReaction/inversereaction.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 7, 2: 10}, 'colors': {1: [16443110], 2: [16711935, 8421504, 10156544]}, 'widths': {2: 2}, 'styles': {2: 0}, 'labels': {1: 'InverseReaction Cloud', 2: 'InverseReaction Histogram'}, 'levels': [], 'description': [], 'name': 'inversereaction', 'source': 'MQL5 Indicators/InverseReaction/inversereaction.mq5', 'folder': 'InverseReaction', 'inputs': [{'mql': 'MomPeriod', 'py': 'MomPeriod', 'param': 'MomPeriod', 'type': 'uint', 'default': 1, 'label': 'Momentum period', 'sinput': False}, {'mql': 'MOMPrice', 'py': 'MOMPrice', 'param': 'MOMPrice', 'type': 'int', 'default': 1, 'label': 'Momentum price', 'sinput': False}, {'mql': 'MaPeriod', 'py': 'MaPeriod', 'param': 'MaPeriod', 'type': 'uint', 'default': 3, 'label': 'Moving average period', 'sinput': False}, {'mql': 'MaPhase', 'py': 'MaPhase', 'param': 'MaPhase', 'type': 'int', 'default': 15, 'label': 'параметр сглаживания,', 'sinput': False}, {'mql': 'MaType', 'py': 'MaType', 'param': 'MaType', 'type': 'int', 'default': 1, 'label': 'Moving average type', 'sinput': False}, {'mql': 'Coefficient', 'py': 'Coefficient', 'param': 'Coefficient', 'type': 'double', 'default': 1.618, 'label': 'Confidence coefficient', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
PRICE_DEMARK_ = 12
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_', 12: 'PRICE_DEMARK_'})

# ---- inputs and global variables
MomPeriod = _input('MomPeriod', 1)  # Momentum period
MOMPrice = _input('MOMPrice', PRICE_CLOSE)  # Momentum price
MaPeriod = _input('MaPeriod', 3)  # Moving average period
MaPhase = _input('MaPhase', 15)  # параметр сглаживания,
MaType = _input('MaType', MODE_EMA)  # Moving average type
Coefficient = _input('Coefficient', 1.618)  # Confidence coefficient
UpIndBuffer = Arr(0, 0.0)
DnIndBuffer = Arr(0, 0.0)
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(MomPeriod + MaPeriod)
    SetIndexBuffer(0, UpIndBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, DnIndBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, IndBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetString(INDICATOR_SHORTNAME, 'InverseReaction')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    if rates_total < min_rates_total:
        return 0
    price = 0.0
    mom = 0.0
    xmom = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price = PriceSeries(MOMPrice, bar, Open, Low, High, Close)
        mom = _fdiv(Mom.MomentumSeries(0, prev_calculated, rates_total, MomPeriod, price, bar, False), Point())
        xmom = Coefficient * XMA.XMASeries(MomPeriod, prev_calculated, rates_total, MaType, MaPhase, MaPeriod, MathAbs(mom), bar, False)
        UpIndBuffer[bar] = xmom
        DnIndBuffer[bar] = -xmom
        IndBuffer[bar] = mom
        clr = 1
        if mom > xmom:
            clr = 2
        if mom < (-xmom):
            clr = 0
        ColorIndBuffer[bar] = clr
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
Mom = _alloc(CMomentum)
Mom.__init__()
XMA = _alloc(CXMA)
XMA.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Inversereaction(_MQL5Indicator):
    name = 'inversereaction'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MomPeriod': 1,  # Momentum period
        'MOMPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Momentum price
        'MaPeriod': 3,  # Moving average period
        'MaPhase': 15,  # параметр сглаживания,
        'MaType': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=1),  # Moving average type
        'Coefficient': 1.618,  # Confidence coefficient
    }

