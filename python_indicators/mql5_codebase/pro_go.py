"""Pro_Go — converted from MQL5: MQL5 Indicators/Pro_Go/Pro_Go.mq5

Williams Pro-Go indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 10, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [32768], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Professional', 2: 'Public'}, 'levels': [], 'description': ['Williams Pro-Go indicator'], 'name': 'Pro_Go', 'source': 'MQL5 Indicators/Pro_Go/Pro_Go.mq5', 'folder': 'Pro_Go', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 7, 'label': 'Period', 'sinput': False}, {'mql': 'InpLevelTop', 'py': 'InpLevelTop', 'param': 'InpLevelTop', 'type': 'double', 'default': 75.0, 'label': 'Overbought', 'sinput': False}, {'mql': 'InpLevelBottom', 'py': 'InpLevelBottom', 'param': 'InpLevelBottom', 'type': 'double', 'default': 25.0, 'label': 'Oversold', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 7)  # Period
InpLevelTop = _input('InpLevelTop', 75.0)  # Overbought
InpLevelBottom = _input('InpLevelBottom', 25.0)  # Oversold
BufferProf = Arr(0, 0.0)
BufferPublic = Arr(0, 0.0)
BufferRaw1 = Arr(0, 0.0)
BufferRaw2 = Arr(0, 0.0)
BufferRaw3 = Arr(0, 0.0)
BufferRaw4 = Arr(0, 0.0)
BufferMA1 = Arr(0, 0.0)
BufferMA2 = Arr(0, 0.0)
BufferMAO = Arr(0, 0.0)
BufferMAC = Arr(0, 0.0)
lev_top = 0.0
lev_bottom = 0.0
period_ma = 0
handle_mao = 0
handle_mac = 0

def OnInit():
    global handle_mac, handle_mao, lev_bottom, lev_top, period_ma
    period_ma = (1 if (InpPeriod < 1) else InpPeriod)
    lev_top = (100 if (InpLevelTop > 100) else 1 if (InpLevelTop < 1) else 1 if (InpLevelTop < 1) else InpLevelTop)
    lev_bottom = (0 if (InpLevelBottom < 0) else (lev_top - 1) if (InpLevelBottom >= lev_top) else InpLevelBottom)
    SetIndexBuffer(0, BufferProf, INDICATOR_DATA)
    SetIndexBuffer(1, BufferPublic, INDICATOR_DATA)
    SetIndexBuffer(2, BufferRaw1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferRaw2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferRaw3, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferRaw4, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferMA1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferMA2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, BufferMAO, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, BufferMAC, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Pro Go (' + _str(period_ma) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, lev_top)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, lev_bottom)
    ArraySetAsSeries(BufferProf, True)
    ArraySetAsSeries(BufferPublic, True)
    ArraySetAsSeries(BufferRaw1, True)
    ArraySetAsSeries(BufferRaw2, True)
    ArraySetAsSeries(BufferRaw3, True)
    ArraySetAsSeries(BufferRaw4, True)
    ArraySetAsSeries(BufferMA1, True)
    ArraySetAsSeries(BufferMA2, True)
    ArraySetAsSeries(BufferMAO, True)
    ArraySetAsSeries(BufferMAC, True)
    ResetLastError()
    handle_mao = iMA(None, PERIOD_CURRENT, period_ma, 0, MODE_SMA, PRICE_OPEN)
    if handle_mao == INVALID_HANDLE:
        Print('The iMA(', _str(period_ma), ') by PRICE_OPEN object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_mac = iMA(None, PERIOD_CURRENT, period_ma, 0, MODE_SMA, PRICE_CLOSE)
    if handle_mac == INVALID_HANDLE:
        Print('The iMA(', _str(period_ma), ') by PRICE_CLOSE object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period_ma, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_ma - 2
        ArrayInitialize(BufferProf, EMPTY_VALUE)
        ArrayInitialize(BufferPublic, EMPTY_VALUE)
        ArrayInitialize(BufferRaw1, 0)
        ArrayInitialize(BufferRaw2, 0)
        ArrayInitialize(BufferRaw3, 0)
        ArrayInitialize(BufferRaw4, 0)
        ArrayInitialize(BufferMA1, 0)
        ArrayInitialize(BufferMA2, 0)
        ArrayInitialize(BufferMAO, 0)
        ArrayInitialize(BufferMAC, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_mao, 0, 0, count, BufferMAO)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_mac, 0, 0, count, BufferMAC)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferMA1[i] = BufferMAO[i] - BufferMAC[i]
        BufferMA2[i] = BufferMAO[i] - BufferMAC[i + 1]
        bh = ArrayMaximum(BufferMA1, i, period_ma)
        bl = ArrayMinimum(BufferMA1, i, period_ma)
        if bh == WRONG_VALUE or bl == WRONG_VALUE:
            continue
        LLV = BufferMA1[bh]
        HHV = BufferMA1[bl]
        BufferRaw1[i] = BufferMA1[i] - LLV
        BufferRaw2[i] = HHV - LLV
        bl = ArrayMinimum(BufferMA2, i, period_ma)
        bh = ArrayMaximum(BufferMA2, i, period_ma)
        if bh == WRONG_VALUE or bl == WRONG_VALUE:
            continue
        LLV = BufferMA2[bl]
        HHV = BufferMA2[bh]
        BufferRaw3[i] = BufferMA2[i] - LLV
        BufferRaw4[i] = HHV - LLV
    for i in range(limit, 0 - 1, -1):
        Avg2 = GetSMA(rates_total, i, period_ma, BufferRaw2)
        Avg4 = GetSMA(rates_total, i, period_ma, BufferRaw4)
        BufferProf[i] = (_fdiv(100.0 * GetSMA(rates_total, i, period_ma, BufferRaw1), Avg2) if (Avg2 != 0) else 0)
        BufferPublic[i] = (_fdiv(100.0 * GetSMA(rates_total, i, period_ma, BufferRaw3), Avg4) if (Avg4 != 0) else 0)
    return rates_total

def GetSMA(rates_total, index, period, price, as_series=True):
    result = 0.0
    check_index = ((index <= (rates_total - period - 1)) if as_series else (index >= (period - 1)))
    if period < 1 or (not check_index):
        return 0.0
    for i in range(0, period):
        result = result + (price[index + i] if as_series else price[index - i])
    return _fdiv(result, period)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ProGo(_MQL5Indicator):
    name = 'Pro_Go'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 7,  # Period
        'InpLevelTop': 75.0,  # Overbought
        'InpLevelBottom': 25.0,  # Oversold
    }

