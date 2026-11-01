"""Average_True_Range_Bands — converted from MQL5: MQL5 Indicators/Average_True_Range_Bands/Average_True_Range_Bands.mq5

Average True Range Bands
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 1, 4: 1}, 'colors': {1: [255], 2: [255], 3: [16711680], 4: [16711680]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'Top', 2: 'Bottom', 3: 'Bottom2', 4: 'Top2'}, 'levels': [], 'description': ['Average True Range Bands'], 'name': 'Average_True_Range_Bands', 'source': 'MQL5 Indicators/Average_True_Range_Bands/Average_True_Range_Bands.mq5', 'folder': 'Average_True_Range_Bands', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 14, 'label': 'ATR period', 'sinput': False}, {'mql': 'InpDeviation', 'py': 'InpDeviation', 'param': 'InpDeviation', 'type': 'double', 'default': 2.0, 'label': 'Deviation', 'sinput': False}, {'mql': 'InpMode', 'py': 'InpMode', 'param': 'InpMode', 'type': 'int', 'default': 0, 'label': 'Calculating mode', 'sinput': False}, {'mql': 'InpShowDeviation', 'py': 'InpShowDeviation', 'param': 'InpShowDeviation', 'type': 'int', 'default': 0, 'label': 'Show deviation line', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# enum ENUM_CALC_MODE
MODE_CALC_CLOSE = 0
MODE_CALC_HL = 1
_enum('ENUM_CALC_MODE', {0: 'MODE_CALC_CLOSE', 1: 'MODE_CALC_HL'})

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 14)  # ATR period
InpDeviation = _input('InpDeviation', 2.0)  # Deviation
InpMode = _input('InpMode', MODE_CALC_CLOSE)  # Calculating mode
InpShowDeviation = _input('InpShowDeviation', INPUT_NO)  # Show deviation line
BufferTop = Arr(0, 0.0)
BufferBottom = Arr(0, 0.0)
BufferTop2 = Arr(0, 0.0)
BufferBottom2 = Arr(0, 0.0)
BufferTrend = Arr(0, 0.0)
BufferATR = Arr(0, 0.0)
deviation = 0.0
period_atr = 0
handle_atr = 0

def OnInit():
    global deviation, handle_atr, period_atr
    period_atr = (1 if (InpPeriod < 1) else InpPeriod)
    deviation = InpDeviation
    SetIndexBuffer(0, BufferTop, INDICATOR_DATA)
    SetIndexBuffer(1, BufferBottom, INDICATOR_DATA)
    SetIndexBuffer(2, BufferTop2, INDICATOR_DATA)
    SetIndexBuffer(3, BufferBottom2, INDICATOR_DATA)
    SetIndexBuffer(4, BufferTrend, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferATR, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'ATR Bands (' + _str(period_atr) + ',' + DoubleToString(deviation, 1) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(2, PLOT_DRAW_TYPE, InpShowDeviation)
    PlotIndexSetInteger(3, PLOT_DRAW_TYPE, InpShowDeviation)
    ArraySetAsSeries(BufferTop, True)
    ArraySetAsSeries(BufferBottom, True)
    ArraySetAsSeries(BufferTop2, True)
    ArraySetAsSeries(BufferBottom2, True)
    ArraySetAsSeries(BufferTrend, True)
    ArraySetAsSeries(BufferATR, True)
    ResetLastError()
    handle_atr = iATR(None, PERIOD_CURRENT, period_atr)
    if handle_atr == INVALID_HANDLE:
        Print('The iATR(', _str(period_atr), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < fmax(period_atr, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferTop, EMPTY_VALUE)
        ArrayInitialize(BufferBottom, EMPTY_VALUE)
        ArrayInitialize(BufferTop2, EMPTY_VALUE)
        ArrayInitialize(BufferBottom2, EMPTY_VALUE)
        ArrayInitialize(BufferTrend, 0)
        ArrayInitialize(BufferATR, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = CopyBuffer(handle_atr, 0, 0, count, BufferATR)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        ATR = BufferATR[i]
        BufferTrend[i] = (1 if (close[i] > BufferTop[i + 1]) else -1 if (close[i] < BufferBottom[i + 1]) else BufferTrend[i + 1])
        if BufferTrend[i] == 1:
            if InpMode == MODE_CALC_CLOSE:
                BufferBottom[i] = close[i] - (ATR * deviation)
                BufferTop[i] = close[i] + (ATR * deviation)
            else:
                BufferTop[i] = low[i] + (ATR * deviation)
                BufferBottom[i] = high[i] - (ATR * deviation)
            if BufferBottom[i] < BufferBottom[i + 1]:
                BufferBottom[i] = BufferBottom[i + 1]
        else:
            if BufferTrend[i] == -1:
                if InpMode == MODE_CALC_CLOSE:
                    BufferBottom[i] = close[i] - (ATR * deviation)
                    BufferTop[i] = close[i] + (ATR * deviation)
                else:
                    BufferBottom[i] = high[i] - (ATR * deviation)
                    BufferTop[i] = low[i] + (ATR * deviation)
                if BufferTop[i] > BufferTop[i + 1]:
                    BufferTop[i] = BufferTop[i + 1]
        if InpMode == MODE_CALC_CLOSE:
            BufferBottom2[i] = close[i] + (ATR * deviation)
            BufferTop2[i] = close[i] - (ATR * deviation)
        else:
            BufferBottom2[i] = low[i] + (ATR * deviation)
            BufferTop2[i] = high[i] - (ATR * deviation)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AverageTrueRangeBands(_MQL5Indicator):
    name = 'Average_True_Range_Bands'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 14,  # ATR period
        'InpDeviation': 2.0,  # Deviation
        'InpMode': _Choice({0: 'Close', 1: 'High/Low'}, default=0),  # Calculating mode
        'InpShowDeviation': _Choice({1: 'Yes', 0: 'No'}, default=0),  # Show deviation line
    }

