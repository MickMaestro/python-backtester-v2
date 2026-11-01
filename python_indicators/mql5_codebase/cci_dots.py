"""CCI_Dots — converted from MQL5: MQL5 Indicators/CCI_Dots/CCI_Dots.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [255], 2: [16711680]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'UP', 2: 'DN'}, 'levels': [], 'description': [], 'name': 'CCI_Dots', 'source': 'MQL5 Indicators/CCI_Dots/CCI_Dots.mq5', 'folder': 'CCI_Dots', 'inputs': [{'mql': 'InpPeriodCCI', 'py': 'InpPeriodCCI', 'param': 'InpPeriodCCI', 'type': 'uint', 'default': 14, 'label': 'CCI period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'CCI applied price', 'sinput': False}, {'mql': 'InpPeriodMA', 'py': 'InpPeriodMA', 'param': 'InpPeriodMA', 'type': 'uint', 'default': 10, 'label': 'MA period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodCCI = _input('InpPeriodCCI', 14)  # CCI period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # CCI applied price
InpPeriodMA = _input('InpPeriodMA', 10)  # MA period
BufferUP = Arr(0, 0.0)
BufferDN = Arr(0, 0.0)
BufferCCI = Arr(0, 0.0)
BufferMAH = Arr(0, 0.0)
BufferMAL = Arr(0, 0.0)
period_cci = 0
period_ma = 0
handle_cci = 0
handle_mah = 0
handle_mal = 0

def OnInit():
    global handle_cci, handle_mah, handle_mal, period_cci, period_ma
    period_cci = (1 if (InpPeriodCCI < 1) else InpPeriodCCI)
    period_ma = (1 if (InpPeriodMA < 1) else InpPeriodMA)
    SetIndexBuffer(0, BufferUP, INDICATOR_DATA)
    SetIndexBuffer(1, BufferDN, INDICATOR_DATA)
    SetIndexBuffer(2, BufferCCI, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferMAH, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferMAL, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_ARROW, 119)
    PlotIndexSetInteger(1, PLOT_ARROW, 119)
    IndicatorSetString(INDICATOR_SHORTNAME, 'CCI dots(' + _str(period_cci) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferUP, True)
    ArraySetAsSeries(BufferDN, True)
    ArraySetAsSeries(BufferCCI, True)
    ArraySetAsSeries(BufferMAH, True)
    ArraySetAsSeries(BufferMAL, True)
    ResetLastError()
    handle_cci = iCCI(None, PERIOD_CURRENT, period_cci, InpAppliedPrice)
    if handle_cci == INVALID_HANDLE:
        Print('The iCCI(', _str(period_cci), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    ResetLastError()
    handle_mah = iMA(None, PERIOD_CURRENT, period_ma, 0, MODE_SMA, PRICE_HIGH)
    if handle_mah == INVALID_HANDLE:
        Print('The iMA(', _str(period_ma), ') by PRICE_HIGH object was not created: Error ', GetLastError())
        return INIT_FAILED
    ResetLastError()
    handle_mal = iMA(None, PERIOD_CURRENT, period_ma, 0, MODE_SMA, PRICE_LOW)
    if handle_mal == INVALID_HANDLE:
        Print('The iMA(', _str(period_ma), ') by PRICE_LOW object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    max_ = fmax(period_cci, period_ma)
    if rates_total < max_:
        return 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferUP, EMPTY_VALUE)
        ArrayInitialize(BufferDN, EMPTY_VALUE)
        ArrayInitialize(BufferCCI, EMPTY_VALUE)
        ArrayInitialize(BufferMAH, EMPTY_VALUE)
        ArrayInitialize(BufferMAL, EMPTY_VALUE)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_cci, 0, 0, count, BufferCCI)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_mah, 0, 0, count, BufferMAH)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_mal, 0, 0, count, BufferMAL)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        range_ = (BufferMAH[i] - BufferMAL[i]) / 2
        cci0 = BufferCCI[i]
        cci1 = BufferCCI[i + 1]
        if cci1 >= 0 and cci0 < 0:
            BufferUP[i] = high[i] + range_
            BufferDN[i] = EMPTY_VALUE
        elif cci1 <= 0 and cci0 > 0:
            BufferUP[i] = EMPTY_VALUE
            BufferDN[i] = low[i] - range_
        else:
            BufferUP[i] = EMPTY_VALUE
            BufferDN[i] = EMPTY_VALUE
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CCIDots(_MQL5Indicator):
    name = 'CCI_Dots'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodCCI': 14,  # CCI period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # CCI applied price
        'InpPeriodMA': 10,  # MA period
    }

