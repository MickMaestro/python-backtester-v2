"""volatilitypivot — converted from MQL5: MQL5 Indicators/VolatilityPivot/volatilitypivot.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [2237106]}, 'widths': {1: 3}, 'styles': {1: 0}, 'labels': {1: 'VolatilityPivot'}, 'levels': [], 'description': [], 'name': 'volatilitypivot', 'source': 'MQL5 Indicators/VolatilityPivot/volatilitypivot.mq5', 'folder': 'VolatilityPivot', 'inputs': [{'mql': 'ima_Method', 'py': 'ima_Method', 'param': 'ima_Method', 'type': 'int', 'default': 3, 'label': 'averaging method', 'sinput': False}, {'mql': 'ima_Phase', 'py': 'ima_Phase', 'param': 'ima_Phase', 'type': 'int', 'default': 15, 'label': 'smoothing parameter,', 'sinput': False}, {'mql': 'ima_range', 'py': 'ima_range', 'param': 'ima_range', 'type': 'uint', 'default': 100, 'label': '', 'sinput': False}, {'mql': 'Mode', 'py': 'Mode', 'param': 'Mode', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'atr_factor', 'py': 'atr_factor', 'param': 'atr_factor', 'type': 'double', 'default': 3.0, 'label': '', 'sinput': False}, {'mql': 'DeltaPrice', 'py': 'DeltaPrice', 'param': 'DeltaPrice', 'type': 'double', 'default': 30.0, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
ima_Method = _input('ima_Method', MODE_LWMA)  # averaging method
ima_Phase = _input('ima_Phase', 15)  # smoothing parameter,
ima_range = _input('ima_range', 100)
Mode = _input('Mode', False)
atr_factor = _input('atr_factor', 3.0)
DeltaPrice = _input('DeltaPrice', 30.0)
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
IndBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = XATR1.GetStartBars(ima_Method, ima_range, ima_Phase) + 1
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    IndicatorSetString(INDICATOR_SHORTNAME, 'VolatilityPivot')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    atr = 0.0
    DeltaStop = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 1
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        if not Mode:
            atr = MathMax(high[bar], close[bar - 1]) - MathMin(low[bar], close[bar - 1])
            DeltaStop = XATR1.XMASeries(1, prev_calculated, rates_total, ima_Method, ima_Phase, ima_range, atr, bar, False)
            DeltaStop *= atr_factor
        else:
            DeltaStop = DeltaPrice * Point()
        if close[bar] == IndBuffer[bar - 1]:
            IndBuffer[bar] = IndBuffer[bar - 1]
        else:
            if close[bar - 1] < IndBuffer[bar - 1] and close[bar] < IndBuffer[bar - 1]:
                IndBuffer[bar] = MathMin(IndBuffer[bar - 1], close[bar] + DeltaStop)
            else:
                if close[bar - 1] > IndBuffer[bar - 1] and close[bar] > IndBuffer[bar - 1]:
                    IndBuffer[bar] = MathMax(IndBuffer[bar - 1], close[bar] - DeltaStop)
                elif close[bar] > IndBuffer[bar - 1]:
                    IndBuffer[bar] = close[bar] - DeltaStop
                else:
                    IndBuffer[bar] = close[bar] + DeltaStop
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XATR1 = _alloc(CXMA)
XATR1.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Volatilitypivot(_MQL5Indicator):
    name = 'volatilitypivot'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ima_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=3),  # averaging method
        'ima_Phase': 15,  # smoothing parameter,
        'ima_range': 100,
        'Mode': False,
        'atr_factor': 3.0,
        'DeltaPrice': 30.0,
        'Shift': 0,  # horizontal shift of the indicator in bars
    }

