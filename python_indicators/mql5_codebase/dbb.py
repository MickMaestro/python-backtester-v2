"""DBB — converted from MQL5: MQL5 Indicators/DBB/DBB.mq5

Distance from Bollinger Band indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [255], 2: [32768]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Top', 2: 'Bottom'}, 'levels': [], 'description': ['Distance from Bollinger Band indicator'], 'name': 'DBB', 'source': 'MQL5 Indicators/DBB/DBB.mq5', 'folder': 'DBB', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 20, 'label': 'BB Period', 'sinput': False}, {'mql': 'InpDeviation', 'py': 'InpDeviation', 'param': 'InpDeviation', 'type': 'double', 'default': 2.0, 'label': 'BB Deviation', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'InpMode', 'py': 'InpMode', 'param': 'InpMode', 'type': 'int', 'default': 0, 'label': 'Display mode', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_CALC_MODE
MODE_PRC = 0
MODE_PT = 1
_enum('ENUM_CALC_MODE', {0: 'MODE_PRC', 1: 'MODE_PT'})

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 20)  # BB Period
InpDeviation = _input('InpDeviation', 2.0)  # BB Deviation
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
InpMode = _input('InpMode', MODE_PRC)  # Display mode
BufferTop = Arr(0, 0.0)
BufferBottom = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
BufferBandsUP = Arr(0, 0.0)
BufferBandsDN = Arr(0, 0.0)
deviation = 0.0
period = 0
handle_ma = 0
handle_bb = 0

def OnInit():
    global deviation, handle_bb, handle_ma, period
    period = (1 if (InpPeriod < 1) else InpPeriod)
    deviation = (0.01 if (InpDeviation == 0) else InpDeviation)
    SetIndexBuffer(0, BufferTop, INDICATOR_DATA)
    SetIndexBuffer(1, BufferBottom, INDICATOR_DATA)
    SetIndexBuffer(2, BufferMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferBandsUP, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferBandsDN, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Distance from BB (' + _str(period) + ',' + DoubleToString(deviation, 2) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferTop, True)
    ArraySetAsSeries(BufferBottom, True)
    ArraySetAsSeries(BufferMA, True)
    ArraySetAsSeries(BufferBandsUP, True)
    ArraySetAsSeries(BufferBandsDN, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_bb = iBands(None, PERIOD_CURRENT, period, 0, deviation, InpAppliedPrice)
    if handle_bb == INVALID_HANDLE:
        Print('The iBands(', _str(period), ',', DoubleToString(deviation, 2), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4 or Point() == 0:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferTop, EMPTY_VALUE)
        ArrayInitialize(BufferBottom, EMPTY_VALUE)
        ArrayInitialize(BufferMA, 0)
        ArrayInitialize(BufferBandsUP, 0)
        ArrayInitialize(BufferBandsDN, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_bb, UPPER_BAND, 0, count, BufferBandsUP)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_bb, LOWER_BAND, 0, count, BufferBandsDN)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        TL = BufferBandsUP[i]
        BL = BufferBandsDN[i]
        if InpMode == MODE_PRC:
            if TL != BL:
                BufferTop[i] = _fdiv(100.0 * (TL - BufferMA[i]), TL - BL)
                BufferBottom[i] = _fdiv(100.0 * (BufferMA[i] - BL), TL - BL)
        else:
            BufferTop[i] = _fdiv(TL - BufferMA[i], Point())
            BufferBottom[i] = _fdiv(BufferMA[i] - BL, Point())
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DBB(_MQL5Indicator):
    name = 'DBB'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 20,  # BB Period
        'InpDeviation': 2.0,  # BB Deviation
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'InpMode': _Choice({0: 'Percentage', 1: 'Price points'}, default=0),  # Display mode
    }

