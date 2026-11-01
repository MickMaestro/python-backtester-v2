"""RVRResistance — converted from MQL5: MQL5 Indicators/RVRResistance/RVRResistance.mq5

RVR Price Resistance oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 10, 2: 1}, 'colors': {1: [10526303, 2263842, 7504122], 2: [16711680]}, 'widths': {1: 2, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'SR', 2: 'Signal'}, 'levels': [], 'description': ['RVR Price Resistance oscillator'], 'name': 'RVRResistance', 'source': 'MQL5 Indicators/RVRResistance/RVRResistance.mq5', 'folder': 'RVRResistance', 'inputs': [{'mql': 'InpType', 'py': 'InpType', 'param': 'InpType', 'type': 'int', 'default': 0, 'label': 'Calculation type', 'sinput': False}, {'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 15, 'label': 'Period', 'sinput': False}, {'mql': 'InpMinP', 'py': 'InpMinP', 'param': 'InpMinP', 'type': 'uint', 'default': 5, 'label': 'Min points', 'sinput': False}, {'mql': 'InpMinV', 'py': 'InpMinV', 'param': 'InpMinV', 'type': 'uint', 'default': 5, 'label': 'Min volume', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 1, 'label': 'MA Method', 'sinput': False}, {'mql': 'InpPrevBars', 'py': 'InpPrevBars', 'param': 'InpPrevBars', 'type': 'int', 'default': 1, 'label': 'Colors setting', 'sinput': False}, {'mql': 'InpInverse', 'py': 'InpInverse', 'param': 'InpInverse', 'type': 'int', 'default': 0, 'label': 'Inverse', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# enum ENUM_TYPE_CALC
TYPE_OC = 0
TYPE_HL = 1
_enum('ENUM_TYPE_CALC', {0: 'TYPE_OC', 1: 'TYPE_HL'})

# enum ENUM_COLOR_SET
COLORS_PREV = 1
COLORS_ONE = 0
_enum('ENUM_COLOR_SET', {1: 'COLORS_PREV', 0: 'COLORS_ONE'})

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpType = _input('InpType', TYPE_OC)  # Calculation type
InpPeriod = _input('InpPeriod', 15)  # Period
InpMinP = _input('InpMinP', 5)  # Min points
InpMinV = _input('InpMinV', 5)  # Min volume
InpMethod = _input('InpMethod', MODE_EMA)  # MA Method
InpPrevBars = _input('InpPrevBars', COLORS_PREV)  # Colors setting
InpInverse = _input('InpInverse', INPUT_NO)  # Inverse
BufferSR = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferSignal = Arr(0, 0.0)
BufferRVR = Arr(0, 0.0)
period_ind = 0
min_point = 0
min_volume = 0
weight_sum = 0

def OnInit():
    global min_point, min_volume, period_ind
    period_ind = (2 if (InpPeriod < 2) else InpPeriod)
    min_point = (1 if (InpMinP < 1) else InpMinP)
    min_volume = (1 if (InpMinV < 1) else InpMinV)
    SetIndexBuffer(0, BufferSR, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferSignal, INDICATOR_DATA)
    SetIndexBuffer(3, BufferRVR, INDICATOR_CALCULATIONS)
    descr = ('High/Low' if (InpType == TYPE_HL) else 'Open/Close')
    IndicatorSetString(INDICATOR_SHORTNAME, 'RVR Price Resistance ' + descr + ' (' + _str(period_ind) + ',' + _str(min_point) + ',' + _str(min_volume) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetDouble(INDICATOR_MINIMUM, 0)
    PlotIndexSetString(0, PLOT_LABEL, 'SR ' + descr)
    PlotIndexSetString(1, PLOT_LABEL, 'Signal' + ' (' + _str(period_ind) + ')')
    ArraySetAsSeries(BufferSR, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferSignal, True)
    ArraySetAsSeries(BufferRVR, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(tick_volume, True)
    if rates_total < 4 or Point() == 0:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferRVR, EMPTY_VALUE)
        ArrayInitialize(BufferSignal, 0)
        ArrayInitialize(BufferRVR, 0)
    for i in range(limit, 0 - 1, -1):
        BufferRVR[i] = _fdiv((fabs(open[i] - close[i]) if (InpType == TYPE_OC) else (high[i] - low[i])), Point())
        diff = fmax(BufferRVR[i], min_point)
        vol = _int(fmax(tick_volume[i], min_volume))
        BufferSR[i] = ((_fdiv(vol, diff) if InpInverse else _fdiv(diff, vol)) if (vol != 0 and diff != 0) else 0)
        BufferColors[i] = 0.0
    _sw1 = InpMethod
    if _sw1 == MODE_EMA:
        ExponentialMAOnBuffer(rates_total, prev_calculated, period_ind, period_ind, BufferSR, BufferSignal)
    elif _sw1 == MODE_SMMA:
        SmoothedMAOnBuffer(rates_total, prev_calculated, period_ind, period_ind, BufferSR, BufferSignal)
    elif _sw1 == MODE_LWMA:
        LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, period_ind, period_ind, BufferSR, BufferSignal, _GlobRef(globals(), 'weight_sum'))
    else:
        SimpleMAOnBuffer(rates_total, prev_calculated, period_ind, period_ind, BufferSR, BufferSignal)
    if InpPrevBars:
        for i in range(limit, 0 - 1, -1):
            BufferColors[i] = (1 if (BufferSR[i + 1] > BufferSignal[i + 1]) else 2)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RVRResistance(_MQL5Indicator):
    name = 'RVRResistance'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpType': _Choice({0: 'Open/Close', 1: 'High/Low'}, default=0),  # Calculation type
        'InpPeriod': 15,  # Period
        'InpMinP': 5,  # Min points
        'InpMinV': 5,  # Min volume
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # MA Method
        'InpPrevBars': _Choice({1: 'By previous bar position', 0: 'One color'}, default=1),  # Colors setting
        'InpInverse': _Choice({1: 'Yes', 0: 'No'}, default=0),  # Inverse
    }

