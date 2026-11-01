"""bw-wiseman-1 — converted from MQL5: MQL5 Indicators/BW-wiseMan-1/bw-wiseman-1.mq5

Copyright: Copyright © 2005, wellx; Link: http://www.metaquotes.net; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, wellx', 'link': 'http://www.metaquotes.net', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711935], 2: [16748574]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'BW-wiseMan-1 Sell', 2: 'BW-wiseMan-1 Buy'}, 'levels': [], 'description': [], 'name': 'bw-wiseman-1', 'source': 'MQL5 Indicators/BW-wiseMan-1/bw-wiseman-1.mq5', 'folder': 'BW-wiseMan-1', 'inputs': [{'mql': 'back', 'py': 'back', 'param': 'back', 'type': 'uint', 'default': 2, 'label': 'Number of bars for analysis', 'sinput': False}, {'mql': 'jaw_period', 'py': 'jaw_period', 'param': 'jaw_period', 'type': 'uint', 'default': 13, 'label': 'Period for calculating jaws', 'sinput': False}, {'mql': 'jaw_shift', 'py': 'jaw_shift', 'param': 'jaw_shift', 'type': 'uint', 'default': 8, 'label': 'Horizontal shift of jaws', 'sinput': False}, {'mql': 'teeth_period', 'py': 'teeth_period', 'param': 'teeth_period', 'type': 'uint', 'default': 8, 'label': 'Teeth calculation period', 'sinput': False}, {'mql': 'teeth_shift', 'py': 'teeth_shift', 'param': 'teeth_shift', 'type': 'uint', 'default': 5, 'label': 'Horizontal shift of teeth', 'sinput': False}, {'mql': 'lips_period', 'py': 'lips_period', 'param': 'lips_period', 'type': 'uint', 'default': 5, 'label': 'Period for calculating lips', 'sinput': False}, {'mql': 'lips_shift', 'py': 'lips_shift', 'param': 'lips_shift', 'type': 'uint', 'default': 3, 'label': 'Horizontal shift of lips', 'sinput': False}, {'mql': 'ma_method', 'py': 'ma_method', 'param': 'ma_method', 'type': 'int', 'default': 2, 'label': 'Smoothing type', 'sinput': False}, {'mql': 'applied_price', 'py': 'applied_price', 'param': 'applied_price', 'type': 'int', 'default': 5, 'label': 'Price type or handle', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
back = _input('back', 2)  # Number of bars for analysis
jaw_period = _input('jaw_period', 13)  # Period for calculating jaws
jaw_shift = _input('jaw_shift', 8)  # Horizontal shift of jaws
teeth_period = _input('teeth_period', 8)  # Teeth calculation period
teeth_shift = _input('teeth_shift', 5)  # Horizontal shift of teeth
lips_period = _input('lips_period', 5)  # Period for calculating lips
lips_shift = _input('lips_shift', 3)  # Horizontal shift of lips
ma_method = _input('ma_method', MODE_SMMA)  # Smoothing type
applied_price = _input('applied_price', PRICE_MEDIAN)  # Price type or handle
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
ALG_Handle = 0
ATR_Handle = 0
min_rates_total = 0

def OnInit():
    global ALG_Handle, ATR_Handle, min_rates_total
    min_rates_total = _int(MathMax(lips_period, MathMax(jaw_period, teeth_period)))
    ALG_Handle = iAlligator(None, 0, jaw_period, jaw_shift, teeth_period, teeth_shift, lips_period, lips_shift, ma_method, applied_price)
    if ALG_Handle == INVALID_HANDLE:
        Print(' Failed to get the handle of iAlligator')
        return INIT_FAILED
    ATR_Handle = iATR(None, 0, 15)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the ATR indicator')
        return INIT_FAILED
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 119)
    ArraySetAsSeries(SellBuffer, True)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 119)
    ArraySetAsSeries(BuyBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'BW-wiseMan-1'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (BarsCalculated(ALG_Handle) < rates_total or BarsCalculated(ATR_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    JAW = Arr(0, 0.0)
    TEETH = Arr(0, 0.0)
    LIPS = Arr(0, 0.0)
    ATR = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(ALG_Handle, GATORJAW_LINE, 0, to_copy, JAW) <= 0:
        return 0
    if CopyBuffer(ALG_Handle, GATORTEETH_LINE, 0, to_copy, TEETH) <= 0:
        return 0
    if CopyBuffer(ALG_Handle, GATORLIPS_LINE, 0, to_copy, LIPS) <= 0:
        return 0
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    ArraySetAsSeries(JAW, True)
    ArraySetAsSeries(TEETH, True)
    ArraySetAsSeries(LIPS, True)
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        if ((low[bar] > LIPS[bar] and low[bar] > TEETH[bar]) and low[bar] > JAW[bar]) and close[bar] < ((high[bar] + low[bar]) / 2):
            contup = True
            for i in range(1, _int(back) + 1):
                if high[bar] <= high[bar + i]:
                    contup = False
                    break
            if contup:
                SellBuffer[bar] = high[bar] + ((ATR[bar] * 3) / 8)
        if ((high[bar] < LIPS[bar] and high[bar] < TEETH[bar]) and high[bar] < JAW[bar]) and close[bar] > ((high[bar] + low[bar]) / 2):
            contup = True
            for i in range(1, _int(back) + 1):
                if low[bar] >= low[bar + i]:
                    contup = False
                    break
            if contup:
                BuyBuffer[bar] = low[bar] - ((ATR[bar] * 3) / 8)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BwWiseman1(_MQL5Indicator):
    name = 'bw-wiseman-1'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'back': 2,  # Number of bars for analysis
        'jaw_period': 13,  # Period for calculating jaws
        'jaw_shift': 8,  # Horizontal shift of jaws
        'teeth_period': 8,  # Teeth calculation period
        'teeth_shift': 5,  # Horizontal shift of teeth
        'lips_period': 5,  # Period for calculating lips
        'lips_shift': 3,  # Horizontal shift of lips
        'ma_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=2),  # Smoothing type
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=5),  # Price type or handle
    }

