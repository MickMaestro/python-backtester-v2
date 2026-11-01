"""Heiken_Ashi_Zone_Trade — converted from MQL5: MQL5 Indicators/Heiken_Ashi_Zone_Trade/Heiken_Ashi_Zone_Trade.mq5

Heiken Ashi Zone Trade
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 13, 'indicator_plots': 4}, 'types': {1: 5, 2: 5, 3: 5, 4: 17}, 'colors': {1: [32768], 2: [255], 3: [11119017], 4: [32768, 65407, 255, 42495, 13882323, 16443110, 11119017]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'Bullish zone', 2: 'Bearish zone', 3: 'Neutral zone', 4: 'Open;High;Low;Close'}, 'levels': [], 'description': ['Heiken Ashi Zone Trade'], 'name': 'Heiken_Ashi_Zone_Trade', 'source': 'MQL5 Indicators/Heiken_Ashi_Zone_Trade/Heiken_Ashi_Zone_Trade.mq5', 'folder': 'Heiken_Ashi_Zone_Trade', 'inputs': [{'mql': 'InpSource', 'py': 'InpSource', 'param': 'InpSource', 'type': 'int', 'default': 0, 'label': 'Data source', 'sinput': False}, {'mql': 'InpPeriodFast', 'py': 'InpPeriodFast', 'param': 'InpPeriodFast', 'type': 'uint', 'default': 5, 'label': 'Fast MA period', 'sinput': False}, {'mql': 'InpPeriodSlow', 'py': 'InpPeriodSlow', 'param': 'InpPeriodSlow', 'type': 'uint', 'default': 35, 'label': 'Slow MA period', 'sinput': False}, {'mql': 'InpPeriodAC', 'py': 'InpPeriodAC', 'param': 'InpPeriodAC', 'type': 'uint', 'default': 5, 'label': 'AC period', 'sinput': False}, {'mql': 'InpMode', 'py': 'InpMode', 'param': 'InpMode', 'type': 'int', 'default': 2, 'label': 'Calculating method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_CALC_SOURCE
SOURCE_PRICE = 0
SOURCE_HA = 1
_enum('ENUM_CALC_SOURCE', {0: 'SOURCE_PRICE', 1: 'SOURCE_HA'})

# enum ENUM_CALC_MODE
MODE_AO = 0
MODE_AC = 1
MODE_AOAC = 2
_enum('ENUM_CALC_MODE', {0: 'MODE_AO', 1: 'MODE_AC', 2: 'MODE_AOAC'})

# ---- inputs and global variables
InpSource = _input('InpSource', SOURCE_PRICE)  # Data source
InpPeriodFast = _input('InpPeriodFast', 5)  # Fast MA period
InpPeriodSlow = _input('InpPeriodSlow', 35)  # Slow MA period
InpPeriodAC = _input('InpPeriodAC', 5)  # AC period
InpMode = _input('InpMode', MODE_AOAC)  # Calculating method
BufferUP = Arr(0, 0.0)
BufferDN = Arr(0, 0.0)
BufferNL = Arr(0, 0.0)
BufferCandleOpen = Arr(0, 0.0)
BufferCandleHigh = Arr(0, 0.0)
BufferCandleLow = Arr(0, 0.0)
BufferCandleClose = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferHA_O = Arr(0, 0.0)
BufferHA_C = Arr(0, 0.0)
BufferHA_M = Arr(0, 0.0)
BufferAO = Arr(0, 0.0)
BufferAC = Arr(0, 0.0)
period_fast = 0
period_slow = 0
period_ac = 0

def OnInit():
    global period_ac, period_fast, period_slow
    period_fast = (1 if (InpPeriodFast < 1) else InpPeriodFast)
    period_slow = ((period_fast + 1) if (InpPeriodSlow == period_fast) else 1 if (InpPeriodSlow < 1) else InpPeriodSlow)
    period_ac = (1 if (InpPeriodAC < 1) else InpPeriodAC)
    SetIndexBuffer(0, BufferUP, INDICATOR_DATA)
    SetIndexBuffer(1, BufferDN, INDICATOR_DATA)
    SetIndexBuffer(2, BufferNL, INDICATOR_DATA)
    SetIndexBuffer(3, BufferCandleOpen, INDICATOR_DATA)
    SetIndexBuffer(4, BufferCandleHigh, INDICATOR_DATA)
    SetIndexBuffer(5, BufferCandleLow, INDICATOR_DATA)
    SetIndexBuffer(6, BufferCandleClose, INDICATOR_DATA)
    SetIndexBuffer(7, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(8, BufferHA_O, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, BufferHA_C, INDICATOR_CALCULATIONS)
    SetIndexBuffer(10, BufferHA_M, INDICATOR_CALCULATIONS)
    SetIndexBuffer(11, BufferAO, INDICATOR_CALCULATIONS)
    SetIndexBuffer(12, BufferAC, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_ARROW, 32)
    PlotIndexSetInteger(1, PLOT_ARROW, 32)
    PlotIndexSetInteger(2, PLOT_ARROW, 32)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Heiken Ashi Zone Trade (' + _str(period_fast) + ',' + _str(period_slow) + ',' + _str(period_ac) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(3, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(BufferUP, True)
    ArraySetAsSeries(BufferDN, True)
    ArraySetAsSeries(BufferNL, True)
    ArraySetAsSeries(BufferCandleOpen, True)
    ArraySetAsSeries(BufferCandleHigh, True)
    ArraySetAsSeries(BufferCandleLow, True)
    ArraySetAsSeries(BufferCandleClose, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferHA_O, True)
    ArraySetAsSeries(BufferHA_C, True)
    ArraySetAsSeries(BufferHA_M, True)
    ArraySetAsSeries(BufferAO, True)
    ArraySetAsSeries(BufferAC, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferUP, EMPTY_VALUE)
        ArrayInitialize(BufferDN, EMPTY_VALUE)
        ArrayInitialize(BufferNL, EMPTY_VALUE)
        ArrayInitialize(BufferCandleOpen, EMPTY_VALUE)
        ArrayInitialize(BufferCandleHigh, EMPTY_VALUE)
        ArrayInitialize(BufferCandleLow, EMPTY_VALUE)
        ArrayInitialize(BufferCandleClose, EMPTY_VALUE)
        ArrayInitialize(BufferColors, 6)
        ArrayInitialize(BufferHA_O, 0)
        ArrayInitialize(BufferHA_C, 0)
        ArrayInitialize(BufferHA_M, 0)
        ArrayInitialize(BufferAO, 0)
        ArrayInitialize(BufferAC, 0)
    for i in range(limit, 0 - 1, -1):
        if InpSource == SOURCE_HA:
            BufferHA_O[i] = (((open[i + 1] + close[i + 1]) / 2.0) if (i == (rates_total - 2)) else ((BufferHA_O[i + 1] + BufferHA_C[i + 1]) / 2.0))
            BufferHA_C[i] = (open[i] + high[i] + low[i] + close[i]) / 4.0
            HA_H = fmax(BufferHA_O[i], fmax(BufferHA_C[i], high[i]))
            HA_L = fmin(BufferHA_O[i], fmin(BufferHA_C[i], low[i]))
            BufferHA_M[i] = (HA_H + HA_L) / 2.0
        else:
            BufferHA_M[i] = (high[i] + low[i]) / 2.0
    for i in range(limit, 0 - 1, -1):
        BufferAO[i] = GetSMA(rates_total, i, period_fast, BufferHA_M) - GetSMA(rates_total, i, period_slow, BufferHA_M)
        BufferAC[i] = BufferAO[i] - GetSMA(rates_total, i, period_ac, BufferAO)
    for i in range(limit, 0 - 1, -1):
        ao = (True if (BufferAO[i] > BufferAO[i + 1]) else False)
        ac = (True if (BufferAC[i] > BufferAC[i + 1]) else False)
        BufferNL[i] = EMPTY_VALUE
        BufferDN[i] = BufferNL[i]
        BufferUP[i] = BufferDN[i]
        BufferCandleOpen[i] = open[i]
        BufferCandleHigh[i] = high[i]
        BufferCandleLow[i] = low[i]
        BufferCandleClose[i] = close[i]
        if InpMode == MODE_AO:
            if ao:
                BufferUP[i] = open[i]
                BufferColors[i] = (0 if (open[i] < close[i]) else 1 if (open[i] > close[i]) else 6)
            else:
                if not ao:
                    BufferDN[i] = open[i]
                    BufferColors[i] = (2 if (open[i] > close[i]) else 3 if (open[i] < close[i]) else 6)
                else:
                    BufferNL[i] = open[i]
                    BufferColors[i] = (4 if (open[i] < close[i]) else 5 if (open[i] > close[i]) else 6)
        else:
            if InpMode == MODE_AC:
                if ac:
                    BufferUP[i] = open[i]
                    BufferColors[i] = (0 if (open[i] < close[i]) else 1 if (open[i] > close[i]) else 6)
                else:
                    if not ac:
                        BufferDN[i] = open[i]
                        BufferColors[i] = (2 if (open[i] > close[i]) else 3 if (open[i] < close[i]) else 6)
                    else:
                        BufferNL[i] = open[i]
                        BufferColors[i] = (4 if (open[i] < close[i]) else 5 if (open[i] > close[i]) else 6)
            else:
                if ao and ac:
                    BufferUP[i] = open[i]
                    BufferColors[i] = (0 if (open[i] < close[i]) else 1 if (open[i] > close[i]) else 6)
                else:
                    if (not ao) and (not ac):
                        BufferDN[i] = open[i]
                        BufferColors[i] = (2 if (open[i] > close[i]) else 3 if (open[i] < close[i]) else 6)
                    else:
                        BufferNL[i] = open[i]
                        BufferColors[i] = (4 if (open[i] < close[i]) else 5 if (open[i] > close[i]) else 6)
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


class HeikenAshiZoneTrade(_MQL5Indicator):
    name = 'Heiken_Ashi_Zone_Trade'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpSource': _Choice({0: 'Price', 1: 'Heiken Ashi'}, default=0),  # Data source
        'InpPeriodFast': 5,  # Fast MA period
        'InpPeriodSlow': 35,  # Slow MA period
        'InpPeriodAC': 5,  # AC period
        'InpMode': _Choice({0: 'AO', 1: 'AC', 2: 'AO+AC'}, default=2),  # Calculating method
    }

