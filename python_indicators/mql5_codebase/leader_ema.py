"""Leader EMA — converted from MQL5: MQL5 Indicators/Leader EMA/Leader EMA.mq5

Leader EMA
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 1, 2: 8}, 'colors': {1: [11119017], 2: [11119017, 32768, 9639167]}, 'widths': {2: 2}, 'styles': {1: 2}, 'labels': {1: 'EMA', 2: 'Leader EMA'}, 'levels': [], 'description': ['Leader EMA'], 'name': 'Leader EMA', 'source': 'MQL5 Indicators/Leader EMA/Leader EMA.mq5', 'folder': 'Leader EMA', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'double', 'default': 14.0, 'label': 'EMA cycles period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpColorMode', 'py': 'inpColorMode', 'param': 'inpColorMode', 'type': 'int', 'default': 0, 'label': 'Color mode', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enColorMode
cm_onSlope = 0
cm_onCross = 1
_enum('enColorMode', {0: 'cm_onSlope', 1: 'cm_onCross'})

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 14.0)  # EMA cycles period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpColorMode = _input('inpColorMode', cm_onSlope)  # Color mode
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
ema = Arr(0, 0.0)
emaw = Arr(0, 0.0)
ª_alpha = 0.0

def OnInit():
    global ª_alpha
    SetIndexBuffer(0, ema, INDICATOR_DATA)
    SetIndexBuffer(1, val, INDICATOR_DATA)
    SetIndexBuffer(2, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(3, emaw, INDICATOR_CALCULATIONS)
    ª_alpha = _fdiv(2.0, 1.0 + inpPeriod)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Leader EMA (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    while i < rates_total:
        _price = 0.0
        _sw1 = inpPrice
        if _sw1 == PRICE_CLOSE:
            _price = close[i]
        elif _sw1 == PRICE_OPEN:
            _price = open[i]
        elif _sw1 == PRICE_HIGH:
            _price = high[i]
        elif _sw1 == PRICE_LOW:
            _price = low[i]
        elif _sw1 == PRICE_MEDIAN:
            _price = (high[i] + low[i]) / 2.0
        elif _sw1 == PRICE_TYPICAL:
            _price = (high[i] + low[i] + close[i]) / 3.0
        elif _sw1 == PRICE_WEIGHTED:
            _price = (high[i] + low[i] + close[i] + close[i]) / 4.0
        else:
            _price = 0.0
        ema[i] = ((ema[i - 1] + (ª_alpha * (_price - ema[i - 1]))) if (i > 0) else _price)
        emaw[i] = ((emaw[i - 1] + (ª_alpha * (_price - ema[i] - emaw[i - 1]))) if (i > 0) else _price)
        val[i] = ema[i] + emaw[i]
        if inpColorMode == cm_onSlope:
            valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        else:
            valc[i] = (1 if (val[i] > ema[i]) else 2 if (val[i] < ema[i]) else valc[i - 1] if (i > 0) else 0)
        i += 1
    return i


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class LeaderEMA(_MQL5Indicator):
    name = 'Leader EMA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 14.0,  # EMA cycles period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpColorMode': _Choice({0: 'Change color on slope change', 1: 'Change color on leader ema to ema cross'}, default=0),  # Color mode
    }

