"""Smoothed_CCI — converted from MQL5: MQL5 Indicators/Smoothed_CCI/Smoothed_CCI.mq5

Smoothed CCI
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'SCCI'}, 'levels': [], 'description': ['Smoothed CCI'], 'name': 'Smoothed_CCI', 'source': 'MQL5 Indicators/Smoothed_CCI/Smoothed_CCI.mq5', 'folder': 'Smoothed_CCI', 'inputs': [{'mql': 'InpPeriodCCI', 'py': 'InpPeriodCCI', 'param': 'InpPeriodCCI', 'type': 'uint', 'default': 14, 'label': 'CCI period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 6, 'label': 'Applied price', 'sinput': False}, {'mql': 'InpUsePreSmoothing', 'py': 'InpUsePreSmoothing', 'param': 'InpUsePreSmoothing', 'type': 'int', 'default': 0, 'label': 'Use pre-smoothing', 'sinput': False}, {'mql': 'InpPeriodPre', 'py': 'InpPeriodPre', 'param': 'InpPeriodPre', 'type': 'uint', 'default': 14, 'label': 'Pre-smoothing period', 'sinput': False}, {'mql': 'InpMethodPre', 'py': 'InpMethodPre', 'param': 'InpMethodPre', 'type': 'int', 'default': 0, 'label': 'Pre-smoothing method', 'sinput': False}, {'mql': 'InpUsePostSmoothing', 'py': 'InpUsePostSmoothing', 'param': 'InpUsePostSmoothing', 'type': 'int', 'default': 0, 'label': 'Use post-smoothing', 'sinput': False}, {'mql': 'InpPeriodPost', 'py': 'InpPeriodPost', 'param': 'InpPeriodPost', 'type': 'uint', 'default': 14, 'label': 'Post-smoothing period', 'sinput': False}, {'mql': 'InpMethodPost', 'py': 'InpMethodPost', 'param': 'InpMethodPost', 'type': 'int', 'default': 0, 'label': 'Post-smoothing method', 'sinput': False}, {'mql': 'InpOverbought', 'py': 'InpOverbought', 'param': 'InpOverbought', 'type': 'double', 'default': 100.0, 'label': 'Overbought', 'sinput': False}, {'mql': 'InpOversold', 'py': 'InpOversold', 'param': 'InpOversold', 'type': 'double', 'default': -100.0, 'label': 'Oversild', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpPeriodCCI = _input('InpPeriodCCI', 14)  # CCI period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_TYPICAL)  # Applied price
InpUsePreSmoothing = _input('InpUsePreSmoothing', INPUT_NO)  # Use pre-smoothing
InpPeriodPre = _input('InpPeriodPre', 14)  # Pre-smoothing period
InpMethodPre = _input('InpMethodPre', MODE_SMA)  # Pre-smoothing method
InpUsePostSmoothing = _input('InpUsePostSmoothing', INPUT_NO)  # Use post-smoothing
InpPeriodPost = _input('InpPeriodPost', 14)  # Post-smoothing period
InpMethodPost = _input('InpMethodPost', MODE_SMA)  # Post-smoothing method
InpOverbought = _input('InpOverbought', 100.0)  # Overbought
InpOversold = _input('InpOversold', -100.0)  # Oversild
BufferSCCI = Arr(0, 0.0)
BufferSource = Arr(0, 0.0)
BufferRes = Arr(0, 0.0)
BufferSpTmpCCI = Arr(0, 0.0)
BufferDTmpCCI = Arr(0, 0.0)
BufferMTmpCCI = Arr(0, 0.0)
overbought = 0.0
oversold = 0.0
period_pre = 0
period_cci = 0
period_post = 0
period_max = 0
handle_ma1 = 0
handle_maP = 0
weight_sum = 0

def OnInit():
    global handle_ma1, handle_maP, overbought, oversold, period_cci, period_max, period_post, period_pre
    period_cci = (2 if (InpPeriodCCI < 2) else InpPeriodCCI)
    period_pre = (2 if (InpPeriodPre < 2) else InpPeriodPre)
    period_post = (2 if (InpPeriodPost < 2) else InpPeriodPost)
    period_max = fmax(period_cci, fmax(period_pre, period_post))
    overbought = (0.1 if (fabs(InpOverbought) < 0.1) else 100.0 if (InpOverbought > 100.0) else fabs(InpOverbought))
    oversold = (-0.1 if ((-fabs(InpOversold)) > -0.1) else -100.0 if ((-fabs(InpOversold)) < -100.0) else (-fabs(InpOversold)))
    SetIndexBuffer(0, BufferSCCI, INDICATOR_DATA)
    SetIndexBuffer(1, BufferSource, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferRes, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferSpTmpCCI, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferDTmpCCI, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferMTmpCCI, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Smoothed CCI (' + _str(period_cci) + ',' + _str(period_pre) + ',' + _str(period_post) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, overbought)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, oversold)
    IndicatorSetString(INDICATOR_LEVELTEXT, 0, 'Overbought')
    IndicatorSetString(INDICATOR_LEVELTEXT, 1, 'Oversold')
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, period_max)
    ArraySetAsSeries(BufferSCCI, True)
    ArraySetAsSeries(BufferSource, True)
    ArraySetAsSeries(BufferRes, True)
    ArraySetAsSeries(BufferSpTmpCCI, True)
    ArraySetAsSeries(BufferDTmpCCI, True)
    ArraySetAsSeries(BufferMTmpCCI, True)
    ResetLastError()
    handle_ma1 = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma1 == INVALID_HANDLE:
        Print('The iMA(1) by ', EnumToString(InpAppliedPrice, 'ENUM_APPLIED_PRICE'), ' object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_maP = iMA(None, PERIOD_CURRENT, period_pre, 0, MODE_SMA, InpAppliedPrice)
    if handle_maP == INVALID_HANDLE:
        Print('The iMA(', _str(period_pre), ') by ', EnumToString(InpAppliedPrice, 'ENUM_APPLIED_PRICE'), ' object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period_max, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_max - 1
        ArrayInitialize(BufferSCCI, EMPTY_VALUE)
        ArrayInitialize(BufferSource, 0)
        ArrayInitialize(BufferRes, 0)
        ArrayInitialize(BufferSpTmpCCI, 0)
        ArrayInitialize(BufferDTmpCCI, 0)
        ArrayInitialize(BufferMTmpCCI, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    if not InpUsePreSmoothing:
        copied = CopyBuffer(handle_ma1, 0, 0, count, BufferSource)
    else:
        copied = CopyBuffer(handle_maP, 0, 0, count, BufferSource)
    if copied != count:
        return 0
    begin = (period_pre if InpUsePreSmoothing else 0)
    if CCIOnArray(rates_total, prev_calculated, begin, period_cci, BufferSource, BufferSpTmpCCI, BufferDTmpCCI, BufferMTmpCCI, BufferRes) == 0:
        return 0
    if not InpUsePostSmoothing:
        for i in range(limit, 0 - 1, -1):
            BufferSCCI[i] = BufferRes[i]
    else:
        begin = (period_cci if InpUsePreSmoothing else 0)
        _sw1 = InpMethodPost
        if _sw1 == MODE_EMA:
            if ExponentialMAOnBuffer(rates_total, prev_calculated, begin, period_post, BufferRes, BufferSCCI) == 0:
                return 0
        elif _sw1 == MODE_SMMA:
            if SmoothedMAOnBuffer(rates_total, prev_calculated, begin, period_post, BufferRes, BufferSCCI) == 0:
                return 0
        elif _sw1 == MODE_LWMA:
            if LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, begin, period_post, BufferRes, BufferSCCI, _GlobRef(globals(), 'weight_sum')) == 0:
                return 0
        else:
            if SimpleMAOnBuffer(rates_total, prev_calculated, begin, period_post, BufferRes, BufferSCCI) == 0:
                return 0
    return rates_total

def CCIOnArray(rates_total, prev_calculated, begin, period, price, buffer_sp, buffer_d, buffer_m, buffer_cci):
    i = 0
    j = 0
    dTmp = 0.0
    dMul = _fdiv(0.015, period)
    StartCalcPosition = period - 1 + begin
    if period < 2 or rates_total < StartCalcPosition:
        return 0
    as_series_price = ArrayGetAsSeries(price)
    as_series_cci = ArrayGetAsSeries(buffer_cci)
    if as_series_price:
        ArraySetAsSeries(price, False)
    if as_series_cci:
        ArraySetAsSeries(buffer_cci, False)
        ArraySetAsSeries(buffer_sp, False)
        ArraySetAsSeries(buffer_d, False)
        ArraySetAsSeries(buffer_m, False)
    pos = prev_calculated - 1
    if pos < StartCalcPosition:
        pos = StartCalcPosition
    i = pos
    for i in range(i, rates_total):
        buffer_sp[i] = SimpleMA(i, period, price)
        dTmp = 0.0
        j = 0
        for j in range(j, period):
            dTmp += fabs(price[i - j] - buffer_sp[i])
        else:
            j = _range_end(j, period, 1)
        buffer_d[i] = dTmp * dMul
        buffer_m[i] = price[i] - buffer_sp[i]
        if buffer_d[i] != 0.0:
            buffer_cci[i] = _fdiv(buffer_m[i], buffer_d[i])
        else:
            buffer_cci[i] = 0.0
    else:
        i = _range_end(i, rates_total, 1)
    if as_series_price:
        ArraySetAsSeries(price, True)
    if as_series_cci:
        ArraySetAsSeries(buffer_cci, True)
        ArraySetAsSeries(buffer_sp, True)
        ArraySetAsSeries(buffer_d, True)
        ArraySetAsSeries(buffer_m, True)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SmoothedCCI(_MQL5Indicator):
    name = 'Smoothed_CCI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodCCI': 14,  # CCI period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=6),  # Applied price
        'InpUsePreSmoothing': _Choice({1: 'Yes', 0: 'No'}, default=0),  # Use pre-smoothing
        'InpPeriodPre': 14,  # Pre-smoothing period
        'InpMethodPre': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Pre-smoothing method
        'InpUsePostSmoothing': _Choice({1: 'Yes', 0: 'No'}, default=0),  # Use post-smoothing
        'InpPeriodPost': 14,  # Post-smoothing period
        'InpMethodPost': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Post-smoothing method
        'InpOverbought': 100.0,  # Overbought
        'InpOversold': -100.0,  # Oversild
    }

