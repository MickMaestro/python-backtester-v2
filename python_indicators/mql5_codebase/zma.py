"""ZMA — converted from MQL5: MQL5 Indicators/ZMA/ZMA.mq5

ZigZag Moving Average
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.1

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.1', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [255], 2: [32768]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'MA Top', 2: 'MA Bottom'}, 'levels': [], 'description': ['ZigZag Moving Average'], 'name': 'ZMA', 'source': 'MQL5 Indicators/ZMA/ZMA.mq5', 'folder': 'ZMA', 'inputs': [{'mql': 'InpDepth', 'py': 'InpDepth', 'param': 'InpDepth', 'type': 'uint', 'default': 12, 'label': 'ZigZag depth', 'sinput': False}, {'mql': 'InpDeviation', 'py': 'InpDeviation', 'param': 'InpDeviation', 'type': 'uint', 'default': 5, 'label': 'ZigZag deviation', 'sinput': False}, {'mql': 'InpBackstep', 'py': 'InpBackstep', 'param': 'InpBackstep', 'type': 'uint', 'default': 3, 'label': 'ZigZag backstep', 'sinput': False}, {'mql': 'InpPrice', 'py': 'InpPrice', 'param': 'InpPrice', 'type': 'int', 'default': 0, 'label': 'Price type', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_PRICE_TYPE
PRICE_TYPE_CLOSE = 0
PRICE_TYPE_HL = 1
_enum('ENUM_PRICE_TYPE', {0: 'PRICE_TYPE_CLOSE', 1: 'PRICE_TYPE_HL'})

# ---- inputs and global variables
InpDepth = _input('InpDepth', 12)  # ZigZag depth
InpDeviation = _input('InpDeviation', 5)  # ZigZag deviation
InpBackstep = _input('InpBackstep', 3)  # ZigZag backstep
InpPrice = _input('InpPrice', PRICE_TYPE_CLOSE)  # Price type
BufferMAT = Arr(0, 0.0)
BufferMAB = Arr(0, 0.0)
BufferZZ = Arr(0, 0.0)
depth = 0
deviation = 0
backstep = 0
handle_zz = 0

def OnInit():
    global backstep, depth, deviation, handle_zz
    backstep = (1 if (InpBackstep < 1) else InpBackstep)
    depth = (backstep if (_int(InpDepth) < backstep) else 1 if (InpDepth < 1) else InpDepth)
    deviation = (1 if (InpDeviation < 1) else InpDeviation)
    SetIndexBuffer(0, BufferMAT, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMAB, INDICATOR_DATA)
    SetIndexBuffer(2, BufferZZ, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_ARROW, 159)
    PlotIndexSetInteger(1, PLOT_ARROW, 159)
    IndicatorSetString(INDICATOR_SHORTNAME, 'ZMA (' + _str(depth) + ',' + _str(deviation) + ',' + _str(backstep) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferMAT, True)
    ArraySetAsSeries(BufferMAB, True)
    ArraySetAsSeries(BufferZZ, True)
    ResetLastError()
    handle_zz = iCustom(None, PERIOD_CURRENT, 'Examples\\ZigZag', depth, deviation, backstep)
    if handle_zz == INVALID_HANDLE:
        Print('The iCustom(MQL5/Indicators/Examples/ZigZag (', _str(depth), ',', _str(deviation), ',', _str(backstep), ')) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < fmax(depth, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferMAT, EMPTY_VALUE)
        ArrayInitialize(BufferMAB, EMPTY_VALUE)
        ArrayInitialize(BufferZZ, 0)
    count = (rates_total if (limit > 0) else 1)
    copied = 0
    copied = CopyBuffer(handle_zz, 0, 0, count, BufferZZ)
    if copied != count:
        return 0
    index = 0
    for i in range(limit, 0 - 1, -1):
        BufferMAB[i] = EMPTY_VALUE
        BufferMAT[i] = BufferMAB[i]
        if BufferZZ[i] > 0:
            index = GetIndexExtremumZZ(rates_total, i, 1, BufferZZ)
            if index != WRONG_VALUE:
                ma = 0.0
                period = 0
                if BufferZZ[index] > BufferZZ[i]:
                    for j in range(index, i - 1, -1):
                        period += 1
                        ma += (high[j] if (InpPrice == PRICE_TYPE_HL) else close[j])
                        BufferMAT[j] = _fdiv(ma, period)
                else:
                    for j in range(index, i - 1, -1):
                        period += 1
                        ma += (low[j] if (InpPrice == PRICE_TYPE_HL) else close[j])
                        BufferMAB[j] = _fdiv(ma, period)
    return rates_total

def GetIndexExtremumZZ(rates_total, shift, num_ext, buffer_zz):
    k_ext = 0
    index = WRONG_VALUE
    for i in range(shift, rates_total):
        if buffer_zz[i] != 0:
            k_ext += 1
            if k_ext > num_ext:
                index = i
                break
    return index


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ZMA(_MQL5Indicator):
    name = 'ZMA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpDepth': 12,  # ZigZag depth
        'InpDeviation': 5,  # ZigZag deviation
        'InpBackstep': 3,  # ZigZag backstep
        'InpPrice': _Choice({0: 'Close', 1: 'High/Low'}, default=0),  # Price type
    }

