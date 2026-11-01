"""TII — converted from MQL5: MQL5 Indicators/TII/TII.mq5

Trend Intensity Index indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [10526303]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'TII'}, 'levels': [], 'description': ['Trend Intensity Index indicator'], 'name': 'TII', 'source': 'MQL5 Indicators/TII/TII.mq5', 'folder': 'TII', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 30, 'label': 'Period', 'sinput': False}, {'mql': 'InpPeriodMA', 'py': 'InpPeriodMA', 'param': 'InpPeriodMA', 'type': 'uint', 'default': 60, 'label': 'MA Period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'MA Method', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'InpOverbought', 'py': 'InpOverbought', 'param': 'InpOverbought', 'type': 'double', 'default': 80.0, 'label': 'Overbought', 'sinput': False}, {'mql': 'InpOversold', 'py': 'InpOversold', 'param': 'InpOversold', 'type': 'double', 'default': 20.0, 'label': 'Oversold', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 30)  # Period
InpPeriodMA = _input('InpPeriodMA', 60)  # MA Period
InpMethod = _input('InpMethod', MODE_SMA)  # MA Method
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
InpOverbought = _input('InpOverbought', 80.0)  # Overbought
InpOversold = _input('InpOversold', 20.0)  # Oversold
BufferTII = Arr(0, 0.0)
BufferMA1 = Arr(0, 0.0)
BufferMAP = Arr(0, 0.0)
BufferUP = Arr(0, 0.0)
BufferDN = Arr(0, 0.0)
BufferPos = Arr(0, 0.0)
BufferNeg = Arr(0, 0.0)
period_tii = 0
period_ma = 0
handle_ma1 = 0
handle_maP = 0
overbought = 0.0
oversold = 0.0

def OnInit():
    global handle_ma1, handle_maP, overbought, oversold, period_ma, period_tii
    period_tii = (2 if (InpPeriod < 2) else InpPeriod)
    period_ma = (1 if (InpPeriodMA < 1) else InpPeriodMA)
    oversold = (0 if (InpOversold < 0) else 99.9 if (InpOversold > 99.9) else InpOversold)
    overbought = (100 if (InpOverbought > 100) else 0.1 if (InpOverbought < 0.1) else InpOverbought)
    if overbought <= oversold:
        overbought = oversold + 0.1
    if oversold >= overbought:
        oversold = overbought - 0.1
    SetIndexBuffer(0, BufferTII, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMA1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferMAP, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferUP, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferDN, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferPos, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferNeg, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Trend Intensity Index (' + _str(period_tii) + ',' + _str(period_ma) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, overbought)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, 50.0)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, oversold)
    IndicatorSetString(INDICATOR_LEVELTEXT, 0, 'Overbought')
    IndicatorSetString(INDICATOR_LEVELTEXT, 2, 'Oversold')
    ArraySetAsSeries(BufferTII, True)
    ArraySetAsSeries(BufferMA1, True)
    ArraySetAsSeries(BufferMAP, True)
    ArraySetAsSeries(BufferUP, True)
    ArraySetAsSeries(BufferDN, True)
    ArraySetAsSeries(BufferPos, True)
    ArraySetAsSeries(BufferNeg, True)
    ResetLastError()
    handle_ma1 = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma1 == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_maP = iMA(None, PERIOD_CURRENT, period_ma, 0, InpMethod, InpAppliedPrice)
    if handle_maP == INVALID_HANDLE:
        Print('The iMA(', _str(period_ma), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4 or Point() == 0:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferTII, EMPTY_VALUE)
        ArrayInitialize(BufferMA1, 0)
        ArrayInitialize(BufferMAP, 0)
        ArrayInitialize(BufferUP, 0)
        ArrayInitialize(BufferDN, 0)
        ArrayInitialize(BufferPos, 0)
        ArrayInitialize(BufferNeg, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma1, 0, 0, count, BufferMA1)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_maP, 0, 0, count, BufferMAP)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        Pr = BufferMA1[i]
        MA = BufferMAP[i]
        if Pr > MA:
            BufferUP[i] = Pr - MA
            BufferDN[i] = 0.0
        else:
            if Pr < MA:
                BufferUP[i] = 0.0
                BufferDN[i] = MA - Pr
            else:
                BufferUP[i] = 0.0
                BufferDN[i] = 0.0
    if SimpleMAOnBuffer(rates_total, prev_calculated, period_ma, period_tii, BufferUP, BufferPos) == 0:
        return 0
    if SimpleMAOnBuffer(rates_total, prev_calculated, period_ma, period_tii, BufferDN, BufferNeg) == 0:
        return 0
    for i in range(limit, 0 - 1, -1):
        pos = BufferPos[i]
        neg = BufferNeg[i]
        BufferTII[i] = (_fdiv(100.0 * pos, pos + neg) if ((pos + neg) != 0) else EMPTY_VALUE)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TII(_MQL5Indicator):
    name = 'TII'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 30,  # Period
        'InpPeriodMA': 60,  # MA Period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # MA Method
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'InpOverbought': 80.0,  # Overbought
        'InpOversold': 20.0,  # Oversold
    }

