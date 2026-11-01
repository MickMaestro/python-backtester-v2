"""Blau_Directional_Trend_Index — converted from MQL5: MQL5 Indicators/Blau_Directional_Trend_Index/Blau_Directional_Trend_Index.mq5

William Blau Directional Trend Index
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 9, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [2263842]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'DTIndex'}, 'levels': [], 'description': ['William Blau Directional Trend Index'], 'name': 'Blau_Directional_Trend_Index', 'source': 'MQL5 Indicators/Blau_Directional_Trend_Index/Blau_Directional_Trend_Index.mq5', 'folder': 'Blau_Directional_Trend_Index', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 2, 'label': 'Period', 'sinput': False}, {'mql': 'InpPeriodSmooth1', 'py': 'InpPeriodSmooth1', 'param': 'InpPeriodSmooth1', 'type': 'uint', 'default': 20, 'label': 'First smoothing period', 'sinput': False}, {'mql': 'InpPeriodSmooth2', 'py': 'InpPeriodSmooth2', 'param': 'InpPeriodSmooth2', 'type': 'uint', 'default': 5, 'label': 'Second smoothing period', 'sinput': False}, {'mql': 'InpPeriodSmooth3', 'py': 'InpPeriodSmooth3', 'param': 'InpPeriodSmooth3', 'type': 'uint', 'default': 3, 'label': 'Third smoothing period', 'sinput': False}, {'mql': 'InpLevelUP', 'py': 'InpLevelUP', 'param': 'InpLevelUP', 'type': 'double', 'default': 25.0, 'label': 'Upper level', 'sinput': False}, {'mql': 'InpLevelDN', 'py': 'InpLevelDN', 'param': 'InpLevelDN', 'type': 'double', 'default': -25.0, 'label': 'Lower level', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 2)  # Period
InpPeriodSmooth1 = _input('InpPeriodSmooth1', 20)  # First smoothing period
InpPeriodSmooth2 = _input('InpPeriodSmooth2', 5)  # Second smoothing period
InpPeriodSmooth3 = _input('InpPeriodSmooth3', 3)  # Third smoothing period
InpLevelUP = _input('InpLevelUP', 25.0)  # Upper level
InpLevelDN = _input('InpLevelDN', -25.0)  # Lower level
BufferDTI = Arr(0, 0.0)
BufferUDM = Arr(0, 0.0)
BufferUDM_MA1 = Arr(0, 0.0)
BufferUDM_MA2 = Arr(0, 0.0)
BufferUDM_MA3 = Arr(0, 0.0)
BufferADM = Arr(0, 0.0)
BufferADM_MA1 = Arr(0, 0.0)
BufferADM_MA2 = Arr(0, 0.0)
BufferADM_MA3 = Arr(0, 0.0)
level_up = 0.0
level_dn = 0.0
period_ind = 0
period_sm1 = 0
period_sm2 = 0
period_sm3 = 0

def OnInit():
    global level_dn, level_up, period_ind, period_sm1, period_sm2, period_sm3
    period_ind = (1 if (InpPeriod < 1) else InpPeriod)
    period_sm1 = (2 if (InpPeriodSmooth1 < 2) else InpPeriodSmooth1)
    period_sm2 = (2 if (InpPeriodSmooth2 < 2) else InpPeriodSmooth2)
    period_sm3 = (2 if (InpPeriodSmooth3 < 2) else InpPeriodSmooth3)
    level_up = (0.1 if (InpLevelUP < 0.1) else InpLevelUP)
    level_dn = ((-InpLevelDN) if (InpLevelDN > 0) else -0.1 if (InpLevelDN > -0.1) else InpLevelDN)
    SetIndexBuffer(0, BufferDTI, INDICATOR_DATA)
    SetIndexBuffer(1, BufferUDM, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferUDM_MA1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferUDM_MA2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferUDM_MA3, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferADM, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferADM_MA1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferADM_MA2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, BufferADM_MA3, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'BDTI(' + _str(period_ind) + ',' + _str(period_sm1) + ',' + _str(period_sm2) + ',' + _str(period_sm3) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, level_up)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, level_dn)
    ArraySetAsSeries(BufferDTI, True)
    ArraySetAsSeries(BufferUDM, True)
    ArraySetAsSeries(BufferUDM_MA1, True)
    ArraySetAsSeries(BufferUDM_MA2, True)
    ArraySetAsSeries(BufferUDM_MA3, True)
    ArraySetAsSeries(BufferADM, True)
    ArraySetAsSeries(BufferADM_MA1, True)
    ArraySetAsSeries(BufferADM_MA2, True)
    ArraySetAsSeries(BufferADM_MA3, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < period_ind:
        return 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_ind - 1
        ArrayInitialize(BufferDTI, EMPTY_VALUE)
        ArrayInitialize(BufferUDM, 0)
        ArrayInitialize(BufferUDM_MA1, 0)
        ArrayInitialize(BufferUDM_MA2, 0)
        ArrayInitialize(BufferUDM_MA3, 0)
        ArrayInitialize(BufferADM, 0)
        ArrayInitialize(BufferADM_MA1, 0)
        ArrayInitialize(BufferADM_MA2, 0)
        ArrayInitialize(BufferADM_MA3, 0)
    for i in range(limit, 0 - 1, -1):
        H = high[i] - high[i + period_ind]
        if H < 0:
            H = 0.0
        L = low[i + period_ind] - low[i]
        if L < 0:
            L = 0.0
        BufferUDM[i] = H - L
        BufferADM[i] = fabs(BufferUDM[i])
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_sm1, BufferUDM, BufferUDM_MA1)
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_sm1, BufferADM, BufferADM_MA1)
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_sm2, BufferUDM_MA1, BufferUDM_MA2)
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_sm2, BufferADM_MA1, BufferADM_MA2)
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_sm3, BufferUDM_MA2, BufferUDM_MA3)
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_sm3, BufferADM_MA2, BufferADM_MA3)
    for i in range(limit, 0 - 1, -1):
        BufferDTI[i] = _fdiv(100.0 * BufferUDM_MA3[i], (BufferADM_MA3[i] if (BufferADM_MA3[i] != 0) else DBL_MIN))
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BlauDirectionalTrendIndex(_MQL5Indicator):
    name = 'Blau_Directional_Trend_Index'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 2,  # Period
        'InpPeriodSmooth1': 20,  # First smoothing period
        'InpPeriodSmooth2': 5,  # Second smoothing period
        'InpPeriodSmooth3': 3,  # Third smoothing period
        'InpLevelUP': 25.0,  # Upper level
        'InpLevelDN': -25.0,  # Lower level
    }

