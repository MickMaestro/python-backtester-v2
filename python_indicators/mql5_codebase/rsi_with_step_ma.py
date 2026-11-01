"""RSI_With_Step_MA — converted from MQL5: MQL5 Indicators/RSI_With_Step_MA/RSI_With_Step_MA.mq5

RSI with step MA oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [5737262]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'SRSI'}, 'levels': [], 'description': ['RSI with step MA oscillator'], 'name': 'RSI_With_Step_MA', 'source': 'MQL5 Indicators/RSI_With_Step_MA/RSI_With_Step_MA.mq5', 'folder': 'RSI_With_Step_MA', 'inputs': [{'mql': 'InpPeriodRSI', 'py': 'InpPeriodRSI', 'param': 'InpPeriodRSI', 'type': 'uint', 'default': 14, 'label': 'RSI period', 'sinput': False}, {'mql': 'InpStep', 'py': 'InpStep', 'param': 'InpStep', 'type': 'int', 'default': 5, 'label': 'Step', 'sinput': False}, {'mql': 'InpPeriodMA', 'py': 'InpPeriodMA', 'param': 'InpPeriodMA', 'type': 'uint', 'default': 6, 'label': 'MA period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'MA method', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'MA applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodRSI = _input('InpPeriodRSI', 14)  # RSI period
InpStep = _input('InpStep', 5)  # Step
InpPeriodMA = _input('InpPeriodMA', 6)  # MA period
InpMethod = _input('InpMethod', MODE_SMA)  # MA method
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # MA applied price
BufferRSI = Arr(0, 0.0)
BufferPos = Arr(0, 0.0)
BufferNeg = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
period_rsi = 0
period_ma = 0
step = 0
handle_ma = 0

def OnInit():
    global handle_ma, period_ma, period_rsi, step
    period_rsi = (1 if (InpPeriodRSI < 1) else InpPeriodRSI)
    period_ma = (1 if (InpPeriodMA < 1) else InpPeriodMA)
    step = (1 if (InpStep < 1) else InpStep)
    SetIndexBuffer(0, BufferRSI, INDICATOR_DATA)
    SetIndexBuffer(1, BufferPos, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferNeg, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferMA, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'SRSI(' + _str(period_rsi) + ',' + _str(step) + ',' + _str(period_ma) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, 30)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, 50)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, 70)
    ArraySetAsSeries(BufferRSI, True)
    ArraySetAsSeries(BufferPos, True)
    ArraySetAsSeries(BufferNeg, True)
    ArraySetAsSeries(BufferMA, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, period_ma, 0, InpMethod, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(', _str(period_ma), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    beg = (period_ma * 2) - 2 + step
    if limit > 1:
        limit = rates_total - beg - 1
        ArrayInitialize(BufferRSI, EMPTY_VALUE)
        ArrayInitialize(BufferPos, 0)
        ArrayInitialize(BufferNeg, 0)
        ArrayInitialize(BufferMA, 0)
    copied = 0
    count = (1 if (limit == 0) else rates_total)
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    sump = 0.0
    sumn = 0.0
    positive = 0.0
    negative = 0.0
    diff = 0.0
    for i in range(limit, 0 - 1, -1):
        if i == (rates_total - beg - 1):
            sump = 0.0
            sumn = 0.0
            for j in range(i + period_ma - 1, i - 1, -1):
                diff = BufferMA[j] - (BufferMA[j + step] if (BufferMA[j + step] != EMPTY_VALUE) else 0)
                if diff >= 0:
                    sump = sump + diff
                else:
                    sumn = sumn - diff
            positive = _fdiv(sump, period_rsi)
            negative = _fdiv(sumn, period_rsi)
        else:
            diff = BufferMA[i] - BufferMA[i + step]
            if diff >= 0:
                sump = diff
            else:
                sumn = -diff
            positive = _fdiv((BufferPos[i + 1] * (period_rsi - 1)) + sump, period_rsi)
            negative = _fdiv((BufferNeg[i + 1] * (period_rsi - 1)) + sumn, period_rsi)
        BufferPos[i] = positive
        BufferNeg[i] = negative
        BufferRSI[i] = (0 if (negative == 0) else (100.0 - _fdiv(100.0, 1.0 + _fdiv(positive, negative))))
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RSIWithStepMA(_MQL5Indicator):
    name = 'RSI_With_Step_MA'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodRSI': 14,  # RSI period
        'InpStep': 5,  # Step
        'InpPeriodMA': 6,  # MA period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # MA method
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # MA applied price
    }

