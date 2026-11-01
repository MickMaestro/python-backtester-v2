"""SVE_ARSI — converted from MQL5: MQL5 Indicators/SVE_ARSI/SVE_ARSI.mq5

Sylvain Vervoort's Asymmetrical RSI
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 8, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [11829830]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'SVeARSI'}, 'levels': [], 'description': ["Sylvain Vervoort's Asymmetrical RSI"], 'name': 'SVE_ARSI', 'source': 'MQL5 Indicators/SVE_ARSI/SVE_ARSI.mq5', 'folder': 'SVE_ARSI', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'InpOverbought', 'py': 'InpOverbought', 'param': 'InpOverbought', 'type': 'double', 'default': 70.0, 'label': 'Overbought', 'sinput': False}, {'mql': 'InpOversold', 'py': 'InpOversold', 'param': 'InpOversold', 'type': 'double', 'default': 30.0, 'label': 'Oversold', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 14)  # Period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
InpOverbought = _input('InpOverbought', 70.0)  # Overbought
InpOversold = _input('InpOversold', 30.0)  # Oversold
BufferARSI = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
BufferUp = Arr(0, 0.0)
BufferDn = Arr(0, 0.0)
BufferUpCnt = Arr(0, 0.0)
BufferAvgUp = Arr(0, 0.0)
BufferAvgDn = Arr(0, 0.0)
BufferAvgUpCnt = Arr(0, 0.0)
overbought = 0.0
oversold = 0.0
period_ind = 0
period2 = 0
handle_ma = 0

def OnInit():
    global handle_ma, overbought, oversold, period2, period_ind
    period_ind = (2 if (InpPeriod < 2) else InpPeriod)
    period2 = (2 * period_ind) - 1
    overbought = (100 if (InpOverbought > 100) else 0.1 if (InpOverbought < 0.1) else InpOverbought)
    oversold = (0 if (InpOversold < 0) else (overbought - 0.1) if (InpOversold >= overbought) else InpOversold)
    SetIndexBuffer(0, BufferARSI, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferUp, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferDn, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferUpCnt, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferAvgUp, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferAvgDn, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferAvgUpCnt, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'SVeARSI (' + _str(period_ind) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, _fdiv(overbought, Point()))
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, _fdiv(oversold, Point()))
    IndicatorSetString(INDICATOR_LEVELTEXT, 0, 'Overbought')
    IndicatorSetString(INDICATOR_LEVELTEXT, 1, 'Oversold')
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, period_ind - 1)
    ArraySetAsSeries(BufferARSI, True)
    ArraySetAsSeries(BufferMA, True)
    ArraySetAsSeries(BufferUp, True)
    ArraySetAsSeries(BufferDn, True)
    ArraySetAsSeries(BufferUpCnt, True)
    ArraySetAsSeries(BufferAvgUp, True)
    ArraySetAsSeries(BufferAvgDn, True)
    ArraySetAsSeries(BufferAvgUpCnt, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(1) by ', EnumToString(InpAppliedPrice, 'ENUM_APPLIED_PRICE'), ' object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period_ind, 4) or Point() == 0:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferARSI, EMPTY_VALUE)
        ArrayInitialize(BufferMA, 0)
        ArrayInitialize(BufferUp, 0)
        ArrayInitialize(BufferDn, 0)
        ArrayInitialize(BufferUpCnt, 0)
        ArrayInitialize(BufferAvgUp, 0)
        ArrayInitialize(BufferAvgDn, 0)
        ArrayInitialize(BufferAvgUpCnt, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        ROC = _fdiv(BufferMA[i] - BufferMA[i + 1], Point())
        BufferUp[i] = fmax(ROC, 0)
        BufferDn[i] = fabs(fmin(ROC, 0))
        BufferUpCnt[i] = (0 if (ROC < 0) else 1)
    if SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_ind, BufferUpCnt, BufferAvgUpCnt) == 0:
        return 0
    if ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period2, BufferUp, BufferAvgUp) == 0:
        return 0
    if ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period2, BufferDn, BufferAvgDn) == 0:
        return 0
    for i in range(limit, 0 - 1, -1):
        up = floor((BufferAvgUpCnt[i] * period_ind) + 0.5)
        dn = period_ind - up
        upmove = (0 if (up == 0) else BufferUp[i] if (up == 1) else BufferAvgUp[i])
        dnmove = (0 if (dn == 0) else BufferDn[i] if (dn == 1) else BufferAvgDn[i])
        BufferARSI[i] = (_fdiv(100.0, Point()) if (dnmove == 0) else _fdiv(100.0 - _fdiv(100.0, 1.0 + _fdiv(upmove, dnmove)), Point()))
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SVEARSI(_MQL5Indicator):
    name = 'SVE_ARSI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 14,  # Period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'InpOverbought': 70.0,  # Overbought
        'InpOversold': 30.0,  # Oversold
    }

