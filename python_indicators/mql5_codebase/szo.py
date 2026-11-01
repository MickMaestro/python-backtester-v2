"""SZO — converted from MQL5: MQL5 Indicators/SZO/SZO.mq5

Sentiment Zone Oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [255], 2: [16711680], 3: [16711680]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'SZO', 2: 'Top', 3: 'Bottom'}, 'levels': [], 'description': ['Sentiment Zone Oscillator'], 'name': 'SZO', 'source': 'MQL5 Indicators/SZO/SZO.mq5', 'folder': 'SZO', 'inputs': [{'mql': 'InpPeriodSZO', 'py': 'InpPeriodSZO', 'param': 'InpPeriodSZO', 'type': 'uint', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'InpPeriodDLev', 'py': 'InpPeriodDLev', 'param': 'InpPeriodDLev', 'type': 'uint', 'default': 30, 'label': 'Dynamic levels period', 'sinput': False}, {'mql': 'InpPercentDLev', 'py': 'InpPercentDLev', 'param': 'InpPercentDLev', 'type': 'double', 'default': 95.0, 'label': 'Dynamic levels percent', 'sinput': False}, {'mql': 'InpOverbought', 'py': 'InpOverbought', 'param': 'InpOverbought', 'type': 'double', 'default': 7.0, 'label': 'Overbought', 'sinput': False}, {'mql': 'InpOversold', 'py': 'InpOversold', 'param': 'InpOversold', 'type': 'double', 'default': -7.0, 'label': 'Oversold', 'sinput': False}, {'mql': 'InpShowDLev', 'py': 'InpShowDLev', 'param': 'InpShowDLev', 'type': 'int', 'default': 1, 'label': 'Show dynamic levels', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpPeriodSZO = _input('InpPeriodSZO', 14)  # Period
InpPeriodDLev = _input('InpPeriodDLev', 30)  # Dynamic levels period
InpPercentDLev = _input('InpPercentDLev', 95.0)  # Dynamic levels percent
InpOverbought = _input('InpOverbought', 7.0)  # Overbought
InpOversold = _input('InpOversold', -7.0)  # Oversold
InpShowDLev = _input('InpShowDLev', INPUT_YES)  # Show dynamic levels
BufferSZO = Arr(0, 0.0)
BufferTop = Arr(0, 0.0)
BufferBottom = Arr(0, 0.0)
BufferR = Arr(0, 0.0)
BufferEMA1 = Arr(0, 0.0)
BufferEMA2 = Arr(0, 0.0)
BufferEMA3 = Arr(0, 0.0)
overbought = 0.0
oversold = 0.0
percent_dl = 0.0
period_dl = 0
period_szo = 0

def OnInit():
    global overbought, oversold, percent_dl, period_dl, period_szo
    period_szo = (1 if (InpPeriodSZO < 1) else InpPeriodSZO)
    period_dl = (2 if (InpPeriodDLev < 2) else InpPeriodDLev)
    percent_dl = (100 if (InpPercentDLev < 1) else (100 - InpPercentDLev) if (InpPercentDLev < 50) else InpPercentDLev)
    oversold = (0 if (InpOversold > 0) else InpOversold)
    overbought = (0 if (InpOverbought < 0) else InpOverbought)
    if overbought <= oversold:
        overbought = oversold + 0.1
    if oversold >= overbought:
        oversold = overbought - 0.1
    SetIndexBuffer(0, BufferSZO, INDICATOR_DATA)
    SetIndexBuffer(1, BufferTop, INDICATOR_DATA)
    SetIndexBuffer(2, BufferBottom, INDICATOR_DATA)
    SetIndexBuffer(3, BufferR, INDICATOR_DATA)
    SetIndexBuffer(4, BufferEMA1, INDICATOR_DATA)
    SetIndexBuffer(5, BufferEMA2, INDICATOR_DATA)
    SetIndexBuffer(6, BufferEMA3, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'SZO(' + _str(period_szo) + ',' + _str(period_dl) + ',' + DoubleToString(percent_dl, 1) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, overbought)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, oversold)
    ArraySetAsSeries(BufferSZO, True)
    ArraySetAsSeries(BufferTop, True)
    ArraySetAsSeries(BufferBottom, True)
    ArraySetAsSeries(BufferR, True)
    ArraySetAsSeries(BufferEMA1, True)
    ArraySetAsSeries(BufferEMA2, True)
    ArraySetAsSeries(BufferEMA3, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < (period_szo * 2):
        return 0
    ArraySetAsSeries(close, True)
    limit = rates_total - prev_calculated
    limit1 = limit
    limit2 = limit
    if limit > 1:
        limit = rates_total - 2
        limit1 = limit - (period_szo * 3)
        limit2 = limit - (period_szo * 3) - period_dl
        ArrayInitialize(BufferSZO, 0)
        ArrayInitialize(BufferTop, EMPTY_VALUE)
        ArrayInitialize(BufferBottom, EMPTY_VALUE)
        ArrayInitialize(BufferR, 0)
        ArrayInitialize(BufferEMA1, 0)
        ArrayInitialize(BufferEMA2, 0)
        ArrayInitialize(BufferEMA3, 0)
    for i in range(limit, 0 - 1, -1):
        BufferR[i] = (1 if (close[i] > close[i + 1]) else -1)
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_szo, BufferR, BufferEMA1)
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_szo, BufferEMA1, BufferEMA2)
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_szo, BufferEMA2, BufferEMA3)
    for i in range(limit1, 0 - 1, -1):
        BufferSZO[i] = 100.0 * _fdiv((3 * BufferEMA1[i]) - (3 * BufferEMA2[i]) + BufferEMA3[i], period_szo)
    if InpShowDLev:
        for i in range(limit2, 0 - 1, -1):
            hlp = BufferSZO[i]
            llp = BufferSZO[i]
            for j in range(period_dl - 1, 0 - 1, -1):
                if hlp < BufferSZO[i + j]:
                    hlp = BufferSZO[i + j]
                if llp > BufferSZO[i + j]:
                    llp = BufferSZO[i + j]
            range_ = hlp - llp
            range_p = range_ * (percent_dl / 100.0)
            BufferTop[i] = llp + range_p
            BufferBottom[i] = hlp - range_p
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SZO(_MQL5Indicator):
    name = 'SZO'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodSZO': 14,  # Period
        'InpPeriodDLev': 30,  # Dynamic levels period
        'InpPercentDLev': 95.0,  # Dynamic levels percent
        'InpOverbought': 7.0,  # Overbought
        'InpOversold': -7.0,  # Oversold
        'InpShowDLev': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show dynamic levels
    }

