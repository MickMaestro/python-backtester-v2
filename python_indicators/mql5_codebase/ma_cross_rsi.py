"""MA_Cross_RSI — converted from MQL5: MQL5 Indicators/Custom MA Cross with RSI Indicator for MT5/MA_Cross_RSI.mq5

Copyright: Copyright 2023, MetaQuotes Ltd.; Link: https://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2023, MetaQuotes Ltd.', 'link': 'https://www.mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [3329330]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'RSI'}, 'levels': [], 'description': [], 'name': 'MA_Cross_RSI', 'source': 'MQL5 Indicators/Custom MA Cross with RSI Indicator for MT5/MA_Cross_RSI.mq5', 'folder': 'Custom MA Cross with RSI Indicator for MT5', 'inputs': [{'mql': 'InpFastMAPeriod', 'py': 'InpFastMAPeriod', 'param': 'InpFastMAPeriod', 'type': 'int', 'default': 7, 'label': '', 'sinput': False}, {'mql': 'InpSlowMAPeriod', 'py': 'InpSlowMAPeriod', 'param': 'InpSlowMAPeriod', 'type': 'int', 'default': 21, 'label': '', 'sinput': False}, {'mql': 'InpRSIPeriod', 'py': 'InpRSIPeriod', 'param': 'InpRSIPeriod', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'InpPriceType', 'py': 'InpPriceType', 'param': 'InpPriceType', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpFastMAPeriod = _input('InpFastMAPeriod', 7)
InpSlowMAPeriod = _input('InpSlowMAPeriod', 21)
InpRSIPeriod = _input('InpRSIPeriod', 14)
InpPriceType = _input('InpPriceType', PRICE_CLOSE)
rsi_Buffer = Arr(0, 0.0)
ma_Handle = 0  # Fast MA (on chart)
sma_Handle = 0  # Slow MA (on chart)
rsi_Handle = 0  # RSI (in separate window)

def OnInit():
    global ma_Handle, rsi_Handle, sma_Handle
    ma_Handle = iMA(Symbol(), Period(), InpFastMAPeriod, 0, MODE_EMA, InpPriceType)
    sma_Handle = iMA(Symbol(), Period(), InpSlowMAPeriod, 0, MODE_EMA, InpPriceType)
    SetIndexBuffer(0, rsi_Buffer, INDICATOR_DATA)
    PlotIndexSetString(0, PLOT_LABEL, 'RSI (' + _str(InpRSIPeriod) + ')')
    rsi_Handle = iRSI(Symbol(), Period(), InpRSIPeriod, InpPriceType)
    if (ma_Handle == INVALID_HANDLE or sma_Handle == INVALID_HANDLE) or rsi_Handle == INVALID_HANDLE:
        Alert('Error creating indicator handles - error: ', GetLastError())
        return INIT_FAILED
    ChartIndicatorAdd(0, 0, ma_Handle)
    ChartIndicatorAdd(0, 0, sma_Handle)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, 30.0)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, 70.0)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrSilver)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrSilver)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DOT)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_last_print
    if (ma_Handle == INVALID_HANDLE or sma_Handle == INVALID_HANDLE) or rsi_Handle == INVALID_HANDLE:
        return 0
    to_copy = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        to_copy = rates_total
    else:
        to_copy = rates_total - prev_calculated + 1
    if CopyBuffer(rsi_Handle, 0, 0, to_copy, rsi_Buffer) <= 0:
        return 0
    if (TimeCurrent() - _s_OnCalculate_last_print) > 60:
        ma_val = Arr(1, 0.0, dyn=False)
        sma_val = Arr(1, 0.0, dyn=False)
        rsi_val = Arr(1, 0.0, dyn=False)
        CopyBuffer(ma_Handle, 0, 0, 1, ma_val)
        CopyBuffer(sma_Handle, 0, 0, 1, sma_val)
        Print('Fast MA(', InpFastMAPeriod, ') = ', ma_val[0], ' | Slow MA(', InpSlowMAPeriod, ') = ', sma_val[0], ' | RSI(', InpRSIPeriod, ') = ', rsi_Buffer[0])
        _s_OnCalculate_last_print = TimeCurrent()
    return rates_total

def OnDeinit(reason):
    if ma_Handle != INVALID_HANDLE:
        IndicatorRelease(ma_Handle)
    if sma_Handle != INVALID_HANDLE:
        IndicatorRelease(sma_Handle)
    if rsi_Handle != INVALID_HANDLE:
        IndicatorRelease(rsi_Handle)
    ChartIndicatorDelete(0, 0, 'Moving Average (' + _str(InpFastMAPeriod) + ')')
    ChartIndicatorDelete(0, 0, 'Moving Average (' + _str(InpSlowMAPeriod) + ')')

# ---- static local variables
_s_OnCalculate_last_print = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MACrossRSI(_MQL5Indicator):
    name = 'MA_Cross_RSI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpFastMAPeriod': 7,
        'InpSlowMAPeriod': 21,
        'InpRSIPeriod': 14,
        'InpPriceType': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
    }

