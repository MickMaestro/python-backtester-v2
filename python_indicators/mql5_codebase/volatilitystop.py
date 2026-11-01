"""VolatilityStop — converted from MQL5: MQL5 Indicators/Volatility Stop/VolatilityStop.mq5

Copyright: Copyright 2024, MetaQuotes Ltd.; Link: https://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2024, MetaQuotes Ltd.', 'link': 'https://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 12}, 'colors': {1: [8951296, 3556340, 8421504]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'VStop'}, 'levels': [], 'description': [], 'name': 'VolatilityStop', 'source': 'MQL5 Indicators/Volatility Stop/VolatilityStop.mq5', 'folder': 'Volatility Stop', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 20, 'label': 'Length', 'sinput': False}, {'mql': 'InpPrice', 'py': 'InpPrice', 'param': 'InpPrice', 'type': 'int', 'default': 1, 'label': 'Source', 'sinput': False}, {'mql': 'InpMultiplier', 'py': 'InpMultiplier', 'param': 'InpMultiplier', 'type': 'double', 'default': 1.75, 'label': 'Multiplier', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 20)  # Length
InpPrice = _input('InpPrice', PRICE_CLOSE)  # Source
InpMultiplier = _input('InpMultiplier', 1.75)  # Multiplier
ExtBufferVStop = Arr(0, 0.0)
ExtBufferColors = Arr(0, 0.0)
ExtBufferATR = Arr(0, 0.0)
ExtBufferSRC = Arr(0, 0.0)
ExtPeriod = 0
ExtMultiplier = 0.0
ExtHandleATR = 0

def OnInit():
    global ExtHandleATR, ExtMultiplier, ExtPeriod
    SetIndexBuffer(0, ExtBufferVStop, INDICATOR_DATA)
    SetIndexBuffer(1, ExtBufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, ExtBufferATR, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, ExtBufferSRC, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_ARROW, 158)
    ArraySetAsSeries(ExtBufferVStop, True)
    ArraySetAsSeries(ExtBufferColors, True)
    ArraySetAsSeries(ExtBufferATR, True)
    ArraySetAsSeries(ExtBufferSRC, True)
    ExtPeriod = (2 if (InpPeriod < 2) else InpPeriod)
    ExtMultiplier = (0.25 if (InpMultiplier < 0.25) else InpMultiplier)
    shortname = StringFormat('VStop %u %s %.2f', ExtPeriod, AppliedPriceDescription(InpPrice), ExtMultiplier)
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    ResetLastError()
    ExtHandleATR = iATR(None, PERIOD_CURRENT, ExtPeriod)
    if ExtHandleATR == INVALID_HANDLE:
        PrintFormat('The iATR(%d) object was not created: Error %d', ExtPeriod, GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < ExtPeriod:
        return 0
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(time, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - ExtPeriod - 2
        ArrayInitialize(ExtBufferVStop, EMPTY_VALUE)
        ArrayInitialize(ExtBufferColors, 2)
        ArrayInitialize(ExtBufferATR, 0)
        ArrayInitialize(ExtBufferSRC, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(ExtHandleATR, 0, 0, count, ExtBufferATR)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        price = GetPriceSRC(i, open, high, low, close)
        stop = ExtBufferVStop[i + 1]
        upper = price + (ExtMultiplier * ExtBufferATR[i])
        lower = price - (ExtMultiplier * ExtBufferATR[i])
        ExtBufferColors[i] = 2.0
        if price > ExtBufferVStop[i + 1]:
            stop = fmax(ExtBufferVStop[i + 1], lower)
            ExtBufferColors[i] = 0.0
        elif price < ExtBufferVStop[i + 1]:
            stop = fmin(ExtBufferVStop[i + 1], upper)
            ExtBufferColors[i] = 1.0
        if ExtBufferColors[i] != ExtBufferColors[i + 1]:
            stop = (lower if (ExtBufferColors[i] == 0) else upper if (ExtBufferColors[i] == 1) else price)
        ExtBufferVStop[i] = stop
    return rates_total

def GetPriceSRC(index, open, high, low, close):
    _sw1 = InpPrice
    if _sw1 == PRICE_OPEN:
        return open[index]
    elif _sw1 == PRICE_HIGH:
        return high[index]
    elif _sw1 == PRICE_LOW:
        return low[index]
    elif _sw1 == PRICE_CLOSE:
        return close[index]
    elif _sw1 == PRICE_MEDIAN:
        return (high[index] + low[index]) / 2.0
    elif _sw1 == PRICE_TYPICAL:
        return (high[index] + low[index] + close[index]) / 3.0
    elif _sw1 == PRICE_WEIGHTED:
        return (high[index] + low[index] + close[index] + close[index]) / 4
    else:
        return 0.0

def AppliedPriceDescription(price):
    res = StringSubstr(EnumToString(price, 'ENUM_APPLIED_PRICE'), 6)
    if res.Lower():
        res.SetChar(0, _ushort(res.GetChar(0) - 32))
    return res


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VolatilityStop(_MQL5Indicator):
    name = 'VolatilityStop'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 20,  # Length
        'InpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Source
        'InpMultiplier': 1.75,  # Multiplier
    }

