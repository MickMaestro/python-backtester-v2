"""Magic_Trend — converted from MQL5: MQL5 Indicators/Magic_Trend/Magic_Trend.mq5

Magic trend
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [3329330, 17919, 12632256]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'MT'}, 'levels': [], 'description': ['Magic trend'], 'name': 'Magic_Trend', 'source': 'MQL5 Indicators/Magic_Trend/Magic_Trend.mq5', 'folder': 'Magic_Trend', 'inputs': [{'mql': 'InpPeriodCCI', 'py': 'InpPeriodCCI', 'param': 'InpPeriodCCI', 'type': 'uint', 'default': 50, 'label': 'CCI period', 'sinput': False}, {'mql': 'InpPeriodATR', 'py': 'InpPeriodATR', 'param': 'InpPeriodATR', 'type': 'uint', 'default': 5, 'label': 'ATR period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodCCI = _input('InpPeriodCCI', 50)  # CCI period
InpPeriodATR = _input('InpPeriodATR', 5)  # ATR period
BufferMT = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferCCI = Arr(0, 0.0)
BufferATR = Arr(0, 0.0)
period_cci = 0
period_atr = 0
handle_cci = 0
handle_atr = 0

def OnInit():
    global handle_atr, handle_cci, period_atr, period_cci
    period_cci = (1 if (InpPeriodCCI < 1) else InpPeriodCCI)
    period_atr = (1 if (InpPeriodATR < 1) else InpPeriodATR)
    SetIndexBuffer(0, BufferMT, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferCCI, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferATR, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'MT(' + _str(period_cci) + ',' + _str(period_atr) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferMT, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferCCI, True)
    ArraySetAsSeries(BufferATR, True)
    ResetLastError()
    handle_cci = iCCI(None, PERIOD_CURRENT, period_cci, PRICE_TYPICAL)
    if handle_cci == INVALID_HANDLE:
        Print('The iCCI(', _str(period_cci), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    ResetLastError()
    handle_atr = iATR(None, PERIOD_CURRENT, period_atr)
    if handle_atr == INVALID_HANDLE:
        Print('The iATR(', _str(period_atr), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferMT, EMPTY_VALUE)
        ArrayInitialize(BufferCCI, 0)
        ArrayInitialize(BufferATR, 0)
    copied = 0
    count = (1 if (limit == 0) else rates_total)
    copied = CopyBuffer(handle_cci, 0, 0, count, BufferCCI)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_atr, 0, 0, count, BufferATR)
    if copied != count:
        return 0
    cci = 0.0
    atr = 0.0
    for i in range(limit, 0 - 1, -1):
        if BufferMT[i + 1] == 0 or BufferMT[i + 1] == EMPTY_VALUE:
            cci = BufferCCI[i + 1]
            atr = BufferATR[i + 1]
            BufferMT[i + 1] = ((low[i + 1] - atr) if (cci > 0) else (high[i + 1] + atr))
        cci = BufferCCI[i]
        atr = BufferATR[i]
        BufferMT[i] = (fmax(BufferMT[i + 1], low[i] - atr) if (cci > 0) else fmin(BufferMT[i + 1], high[i] + atr))
        BufferColors[i] = (0 if (BufferMT[i] > BufferMT[i + 1]) else 1 if (BufferMT[i] < BufferMT[i + 1]) else 2)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MagicTrend(_MQL5Indicator):
    name = 'Magic_Trend'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'InpPeriodCCI': 50,  # CCI period
        'InpPeriodATR': 5,  # ATR period
    }

