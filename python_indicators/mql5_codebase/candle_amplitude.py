"""Candle_Amplitude — converted from MQL5: MQL5 Indicators/Candle_Amplitude/Candle_Amplitude.mq5

Candle Amplitude oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 8, 2: 1}, 'colors': {1: [32768, 255, 11119017], 2: [16711680]}, 'widths': {1: 2, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Amplitude', 2: 'Signal'}, 'levels': [], 'description': ['Candle Amplitude oscillator'], 'name': 'Candle_Amplitude', 'source': 'MQL5 Indicators/Candle_Amplitude/Candle_Amplitude.mq5', 'folder': 'Candle_Amplitude', 'inputs': [{'mql': 'InpMode', 'py': 'InpMode', 'param': 'InpMode', 'type': 'int', 'default': 0, 'label': 'Calculation mode', 'sinput': False}, {'mql': 'InpPeriodSm', 'py': 'InpPeriodSm', 'param': 'InpPeriodSm', 'type': 'uint', 'default': 10, 'label': 'Signal period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_MODE
MODE_HL = 0
MODE_OC = 1
_enum('ENUM_MODE', {0: 'MODE_HL', 1: 'MODE_OC'})

# ---- inputs and global variables
InpMode = _input('InpMode', MODE_HL)  # Calculation mode
InpPeriodSm = _input('InpPeriodSm', 10)  # Signal period
BufferMain = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferSignal = Arr(0, 0.0)
period_sm = 0

def OnInit():
    global period_sm
    period_sm = (1 if (InpPeriodSm < 1) else InpPeriodSm)
    SetIndexBuffer(0, BufferMain, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferSignal, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Candle Amplitude (' + 'Mode ' + ModeToString() + ', period ' + _str(period_sm) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    ArraySetAsSeries(BufferMain, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferSignal, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < fmax(period_sm, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_sm - 2
        ArrayInitialize(BufferMain, EMPTY_VALUE)
        ArrayInitialize(BufferSignal, EMPTY_VALUE)
    for i in range(limit, 0 - 1, -1):
        BufferMain[i] = _fdiv(((high[i] - low[i]) if (InpMode == MODE_HL) else (close[i] - open[i])), Point())
        c0 = ((high[i] - low[i]) if (InpMode == MODE_HL) else fabs(close[i] - open[i]))
        c1 = ((high[i + 1] - low[i + 1]) if (InpMode == MODE_HL) else fabs(close[i + 1] - open[i + 1]))
        BufferColors[i] = (0 if (c0 > c1) else 1 if (c0 < c1) else 2)
        BufferSignal[i] = GetSMA(rates_total, i, period_sm, BufferMain)
    return rates_total

def GetSMA(rates_total, index, period, price, as_series=True):
    result = 0.0
    check_index = ((index <= (rates_total - period - 1)) if as_series else (index >= (period - 1)))
    if period < 1 or (not check_index):
        return 0.0
    for i in range(0, period):
        result = result + (price[index + i] if as_series else price[index - i])
    return _fdiv(result, period)

def ModeToString():
    return ('High/Low' if (InpMode == MODE_HL) else 'Open/Close')


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CandleAmplitude(_MQL5Indicator):
    name = 'Candle_Amplitude'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpMode': _Choice({0: 'High/Low', 1: 'Open/Close'}, default=0),  # Calculation mode
        'InpPeriodSm': 10,  # Signal period
    }

