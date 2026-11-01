"""BBMA ZoneZeroLoss (ZZL) Oma Ally — converted from MQL5: MQL5 Indicators/BBMA ZoneZeroLoss (ZZL) Grandma Ally/BBMA ZoneZeroLoss (ZZL) Oma Ally.mq5

Copyright: Copyright © 2025, Alexander Piechotta; Link: alepie@outlook.de; Version: 1.0

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright © 2025, Alexander Piechotta', 'link': 'alepie@outlook.de', 'version': '1.0', 'window': 'separate', 'indicator_buffers': 10, 'indicator_plots': 2}, 'types': {1: 10, 2: 10}, 'colors': {1: [4294967295, 32768, 255], 2: [4294967295, 32768, 255]}, 'widths': {1: 5, 2: 5}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Zero Loss Zone UP', 2: 'Zero Loss Zone DOWN'}, 'levels': [], 'description': [], 'name': 'BBMA ZoneZeroLoss (ZZL) Oma Ally', 'source': 'MQL5 Indicators/BBMA ZoneZeroLoss (ZZL) Grandma Ally/BBMA ZoneZeroLoss (ZZL) Oma Ally.mq5', 'folder': 'BBMA ZoneZeroLoss (ZZL) Grandma Ally', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpBandsPeriod = 20  # Period
InpEMA50Period = 50
InpMa5Period = 5  # Period
InpMa10Period = 10
HistogramBufferUp = Arr(0, 0.0)
HistogramColorsUp = Arr(0, 0.0)
HistogramBufferDown = Arr(0, 0.0)
HistogramColorDown = Arr(0, 0.0)
Mahi5Buffer = Arr(0, 0.0)
Mahi10Buffer = Arr(0, 0.0)
Malo5Buffer = Arr(0, 0.0)
Malo10Buffer = Arr(0, 0.0)
MidBBBuffer = Arr(0, 0.0)
EMA50Buffer = Arr(0, 0.0)
m_digits = -1

def OnInit():
    global m_digits
    m_digits = Digits()
    if m_digits < 0:
        m_digits = 0
    SetIndexBuffer(0, HistogramBufferUp, INDICATOR_DATA)
    SetIndexBuffer(1, HistogramColorsUp, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, HistogramBufferDown, INDICATOR_DATA)
    SetIndexBuffer(3, HistogramColorDown, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, MidBBBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, EMA50Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, Mahi10Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, Mahi5Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, Malo10Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, Malo5Buffer, INDICATOR_CALCULATIONS)
    IndicatorSetDouble(INDICATOR_MINIMUM, 0.0)
    IndicatorSetDouble(INDICATOR_MAXIMUM, 1.0)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0.0)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetString(INDICATOR_SHORTNAME, 'BBMA ZoneZeroLoss (ZZL) Oma Ally')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    limit = prev_calculated - 1
    if prev_calculated == 0:
        limit = 0
    SimpleMAOnBuffer(rates_total, prev_calculated, 0, InpBandsPeriod, close, MidBBBuffer)
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, InpEMA50Period, close, EMA50Buffer)
    LinearWeightedMAOnBuffer_1(rates_total, prev_calculated, 0, InpMa10Period, high, Mahi10Buffer)
    LinearWeightedMAOnBuffer_1(rates_total, prev_calculated, 0, InpMa5Period, high, Mahi5Buffer)
    LinearWeightedMAOnBuffer_1(rates_total, prev_calculated, 0, InpMa10Period, low, Malo10Buffer)
    LinearWeightedMAOnBuffer_1(rates_total, prev_calculated, 0, InpMa5Period, low, Malo5Buffer)
    for i in range(limit, rates_total):
        HistogramBufferDown[i] = 0.0
        HistogramColorDown[i] = 0.0
        HistogramBufferUp[i] = 0.0
        HistogramColorsUp[i] = 0.0
        if (((EMA50Buffer[i] >= MidBBBuffer[i] and Mahi10Buffer[i] <= MidBBBuffer[i]) and Mahi5Buffer[i] <= MidBBBuffer[i]) and Malo10Buffer[i] <= MidBBBuffer[i]) and Malo5Buffer[i] <= MidBBBuffer[i]:
            HistogramBufferDown[i] = 1.0
            HistogramColorDown[i] = 2.0
        if (((EMA50Buffer[i] <= MidBBBuffer[i] and Mahi10Buffer[i] >= MidBBBuffer[i]) and Mahi5Buffer[i] >= MidBBBuffer[i]) and Malo10Buffer[i] >= MidBBBuffer[i]) and Malo5Buffer[i] >= MidBBBuffer[i]:
            HistogramBufferUp[i] = 1.0
            HistogramColorsUp[i] = 1.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BBMAZoneZeroLossZZLOmaAlly(_MQL5Indicator):
    name = 'BBMA ZoneZeroLoss (ZZL) Oma Ally'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

