"""ASAR — converted from MQL5: MQL5 Indicators/ASAR/ASAR.mq5

Advance Parabolic Time/Price System
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711680], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'ASAR UP', 2: 'ASAR DN'}, 'levels': [], 'description': ['Advance Parabolic Time/Price System'], 'name': 'ASAR', 'source': 'MQL5 Indicators/ASAR/ASAR.mq5', 'folder': 'ASAR', 'inputs': [{'mql': 'InpPriceMode', 'py': 'InpPriceMode', 'param': 'InpPriceMode', 'type': 'int', 'default': 0, 'label': 'Price mode', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'InpStart', 'py': 'InpStart', 'param': 'InpStart', 'type': 'double', 'default': 0.02, 'label': 'Start', 'sinput': False}, {'mql': 'InpStep', 'py': 'InpStep', 'param': 'InpStep', 'type': 'double', 'default': 0.002, 'label': 'Step', 'sinput': False}, {'mql': 'InpMax', 'py': 'InpMax', 'param': 'InpMax', 'type': 'double', 'default': 0.2, 'label': 'Max', 'sinput': False}, {'mql': 'InpFilter', 'py': 'InpFilter', 'param': 'InpFilter', 'type': 'double', 'default': 0.0, 'label': 'Filter', 'sinput': False}, {'mql': 'InpMinChange', 'py': 'InpMinChange', 'param': 'InpMinChange', 'type': 'double', 'default': 0.0, 'label': 'Min change', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_PRICE_MODE
PRICE_MODE_DEF = 0
PRICE_MODE_HL = 1
_enum('ENUM_PRICE_MODE', {0: 'PRICE_MODE_DEF', 1: 'PRICE_MODE_HL'})

# ---- inputs and global variables
InpPriceMode = _input('InpPriceMode', PRICE_MODE_DEF)  # Price mode
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
InpStart = _input('InpStart', 0.02)  # Start
InpStep = _input('InpStep', 0.002)  # Step
InpMax = _input('InpMax', 0.2)  # Max
InpFilter = _input('InpFilter', 0.0)  # Filter
InpMinChange = _input('InpMinChange', 0.0)  # Min change
BufferSARUP = Arr(0, 0.0)
BufferSARDN = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
BufferAF = Arr(0, 0.0)
BufferTrend = Arr(0, 0.0)
HighValue = Arr(10, 0.0, dyn=False)
LowValue = Arr(10, 0.0, dyn=False)
HiPrice = Arr(10, 0.0, dyn=False)
LoPrice = Arr(10, 0.0, dyn=False)
start = 0.0
step = 0.0
max_ = 0.0
filter_ = 0.0
min_change = 0.0
last_time = 0
first_start = False
handle_ma = 0

def OnInit():
    global filter_, first_start, handle_ma, last_time, max_, min_change, start, step
    start = (0 if (InpStart < 0) else InpStart)
    step = (0.0001 if (InpStep < 0.0001) else InpStep)
    max_ = (0.002 if (InpMax < 0.002) else InpMax)
    min_change = (0 if (InpMinChange < 0) else InpMinChange)
    filter_ = InpFilter
    first_start = True
    last_time = 0
    SetIndexBuffer(0, BufferSARUP, INDICATOR_DATA)
    SetIndexBuffer(1, BufferSARDN, INDICATOR_DATA)
    SetIndexBuffer(2, BufferMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferAF, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferTrend, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_ARROW, 158)
    PlotIndexSetInteger(1, PLOT_ARROW, 158)
    IndicatorSetString(INDICATOR_SHORTNAME, 'ASAR (' + _str(start) + ',' + _str(step) + ',' + _str(max_) + ',' + _str(min_change) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferSARUP, True)
    ArraySetAsSeries(BufferSARDN, True)
    ArraySetAsSeries(BufferMA, True)
    ArraySetAsSeries(BufferAF, True)
    ArraySetAsSeries(BufferTrend, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA (1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global first_start, last_time
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(time, True)
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 3
        ArrayInitialize(BufferSARUP, EMPTY_VALUE)
        ArrayInitialize(BufferSARDN, EMPTY_VALUE)
        ArrayInitialize(BufferMA, 0)
        ArrayInitialize(BufferAF, 0)
        ArrayInitialize(BufferTrend, 1)
    count = (rates_total if (limit > 0) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        if last_time < time[i]:
            HighValue[2] = HighValue[1]
            HighValue[1] = HighValue[0]
            LowValue[2] = LowValue[1]
            LowValue[1] = LowValue[0]
            HiPrice[2] = HiPrice[1]
            HiPrice[1] = HiPrice[0]
            LoPrice[2] = LoPrice[1]
            LoPrice[1] = LoPrice[0]
            last_time = time[i]
        if InpPriceMode == PRICE_MODE_HL:
            HiPrice[0] = high[i]
            LoPrice[0] = low[i]
        else:
            HiPrice[0] = BufferMA[i]
            LoPrice[0] = HiPrice[0]
        if i == (rates_total - 2) and first_start:
            BufferTrend[i] = 1.0
            HighValue[1] = HiPrice[1]
            HighValue[0] = fmax(HiPrice[0], HighValue[1])
            LowValue[1] = LoPrice[1]
            LowValue[0] = fmin(LoPrice[0], LowValue[1])
            BufferAF[i] = start
            BufferSARUP[i] = LowValue[0]
            BufferSARDN[i] = EMPTY_VALUE
            first_start = False
            continue
        HighValue[0] = HighValue[1]
        LowValue[0] = LowValue[1]
        BufferTrend[i] = BufferTrend[i + 1]
        BufferAF[i] = BufferAF[i + 1]
        if BufferTrend[i + 1] > 0.0:
            if BufferTrend[i + 1] == BufferTrend[i + 2]:
                if HighValue[1] > HighValue[2]:
                    BufferAF[i] = BufferAF[i + 1] + step
                if BufferAF[i] > max_:
                    BufferAF[i] = max_
                if HighValue[1] < HighValue[2]:
                    BufferAF[i] = start
            else:
                BufferAF[i] = BufferAF[i + 1]
            BufferSARUP[i] = BufferSARUP[i + 1] + (BufferAF[i] * (HighValue[1] - BufferSARUP[i + 1]))
            if BufferSARUP[i] > LoPrice[1]:
                BufferSARUP[i] = LoPrice[1]
            if BufferSARUP[i] > LoPrice[2]:
                BufferSARUP[i] = LoPrice[2]
        else:
            if BufferTrend[i + 1] < 0:
                if BufferTrend[i + 1] == BufferTrend[i + 2]:
                    if LowValue[1] < LowValue[2]:
                        BufferAF[i] = BufferAF[i + 1] + step
                    if BufferAF[i] > max_:
                        BufferAF[i] = max_
                    if LowValue[1] > LowValue[2]:
                        BufferAF[i] = start
                else:
                    BufferAF[i] = BufferAF[i + 1]
                BufferSARDN[i] = BufferSARDN[i + 1] + (BufferAF[i] * (LowValue[1] - BufferSARDN[i + 1]))
                if BufferSARDN[i] < HiPrice[1]:
                    BufferSARDN[i] = HiPrice[1]
                if BufferSARDN[i] < HiPrice[2]:
                    BufferSARDN[i] = HiPrice[2]
        if HiPrice[0] > HighValue[0]:
            HighValue[0] = HiPrice[0]
        if LoPrice[0] < LowValue[0]:
            LowValue[0] = LoPrice[0]
        if min_change > 0:
            if ((BufferSARUP[i] - BufferSARUP[i + 1]) < (min_change * Point()) and BufferSARUP[i] > 0) and BufferSARUP[i + 1] > 0:
                BufferSARUP[i] = BufferSARUP[i + 1]
            if ((BufferSARDN[i + 1] - BufferSARDN[i]) < (min_change * Point()) and BufferSARDN[i] > 0) and BufferSARDN[i + 1] > 0:
                BufferSARDN[i] = BufferSARDN[i + 1]
        if BufferTrend[i] < 0 and HiPrice[0] >= (BufferSARDN[i] + (filter_ * Point())):
            BufferTrend[i] = 1.0
            BufferSARUP[i] = LowValue[0]
            BufferSARDN[i] = EMPTY_VALUE
            BufferAF[i] = start
            LowValue[0] = LoPrice[0]
            HighValue[0] = HiPrice[0]
        else:
            if BufferTrend[i] > 0 and LoPrice[0] <= (BufferSARUP[i] - (filter_ * Point())):
                BufferTrend[i] = -1.0
                BufferSARDN[i] = HighValue[0]
                BufferSARUP[i] = EMPTY_VALUE
                BufferAF[i] = start
                LowValue[0] = LoPrice[0]
                HighValue[0] = HiPrice[0]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ASAR(_MQL5Indicator):
    name = 'ASAR'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPriceMode': _Choice({0: 'Defined', 1: 'High/Low'}, default=0),  # Price mode
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'InpStart': 0.02,  # Start
        'InpStep': 0.002,  # Step
        'InpMax': 0.2,  # Max
        'InpFilter': 0.0,  # Filter
        'InpMinChange': 0.0,  # Min change
    }

