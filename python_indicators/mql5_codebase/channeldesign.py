"""ChannelDesign — converted from MQL5: MQL5 Indicators/Channel design indicator/ChannelDesign.mq5

Copyright: Copyright 2018, Murilo Fregonesi Falleiros.; Version: 1.20

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, Murilo Fregonesi Falleiros.', 'version': '1.20', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 2, 2: 2}, 'colors': {1: [42495], 2: [42495]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'resistance', 2: 'support'}, 'levels': [], 'description': [], 'name': 'ChannelDesign', 'source': 'MQL5 Indicators/Channel design indicator/ChannelDesign.mq5', 'folder': 'Channel design indicator', 'inputs': [{'mql': 'barsChannel', 'py': 'barsChannel', 'param': 'barsChannel', 'type': 'int', 'default': 200, 'label': 'Channel creation length', 'sinput': False}, {'mql': 'barsMulti', 'py': 'barsMulti', 'param': 'barsMulti', 'type': 'int', 'default': 5, 'label': 'Channel bars to peak/valley', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
barsChannel = _input('barsChannel', 200)  # Channel creation length
barsMulti = _input('barsMulti', 5)  # Channel bars to peak/valley
resiBuffer = Arr(0, 0.0)
suppBuffer = Arr(0, 0.0)
priceExp = 0.0  # Expected price
priceAct = 0.0  # Actual price
m_res = 0.0  # Channel resistance slope
m_sup = 0.0  # Channel support slopes

def OnInit():
    SetIndexBuffer(0, resiBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, suppBuffer, INDICATOR_DATA)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ArrayFree(resiBuffer)
    ArrayFree(suppBuffer)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global m_res, m_sup, priceAct, priceExp
    if rates_total > prev_calculated:
        iPeak = 0
        iVall = 0
        peakValue = Arr(0, 0.0)
        vallValue = Arr(0, 0.0)
        peakIndex = Arr(0, 0)
        vallIndex = Arr(0, 0)
        inBarsRange = rates_total - barsChannel + barsMulti
        if inBarsRange < 0:
            inBarsRange = 0
        for i in range(inBarsRange, rates_total - barsMulti - 1):
            if i == ArrayMaximum(high, i - barsMulti, (2 * barsMulti) + 1):
                ArrayCopy(peakValue, high, iPeak, i, 1)
                ArrayResize(peakIndex, ArraySize(peakValue), 0)
                peakIndex[iPeak] = i
                iPeak += 1
            if i == ArrayMinimum(low, i - barsMulti, (2 * barsMulti) + 1):
                ArrayCopy(vallValue, low, iVall, i, 1)
                ArrayResize(vallIndex, ArraySize(vallValue), 0)
                vallIndex[iVall] = i
                iVall += 1
        if iPeak > 1:
            m_res = _fdiv(peakValue[iPeak - 1] - peakValue[iPeak - 2], peakIndex[iPeak - 1] - peakIndex[iPeak - 2])
            if iPeak > 2:
                for i in range(iPeak - 3, 0 - 1, -1):
                    priceAct = peakValue[i]
                    priceExp = peakValue[iPeak - 1] - (m_res * (peakIndex[iPeak - 1] - peakIndex[i]))
                    if priceExp < priceAct:
                        m_res = _fdiv(peakValue[iPeak - 1] - peakValue[i], peakIndex[iPeak - 1] - peakIndex[i])
        if iVall > 1:
            m_sup = _fdiv(vallValue[iVall - 1] - vallValue[iVall - 2], vallIndex[iVall - 1] - vallIndex[iVall - 2])
            if iVall > 2:
                for i in range(iVall - 3, 0 - 1, -1):
                    priceAct = vallValue[i]
                    priceExp = vallValue[iVall - 1] - (m_sup * (vallIndex[iVall - 1] - vallIndex[i]))
                    if priceExp > priceAct:
                        m_sup = _fdiv(vallValue[iVall - 1] - vallValue[i], vallIndex[iVall - 1] - vallIndex[i])
        if iPeak > 1:
            resiBuffer[peakIndex[iPeak - 1]] = peakValue[iPeak - 1]
            leftLim = peakIndex[iPeak - 1] - 1 - (barsChannel * 2)
            if leftLim < 0:
                leftLim = 0
            for i in range(peakIndex[iPeak - 1] - 1, leftLim, -1):
                resiBuffer[i] = peakValue[iPeak - 1] - (m_res * (peakIndex[iPeak - 1] - i))
            for i in range(peakIndex[iPeak - 1] + 1, rates_total):
                resiBuffer[i] = (m_res * (i - peakIndex[iPeak - 1])) + peakValue[iPeak - 1]
        if iVall > 1:
            suppBuffer[vallIndex[iVall - 1]] = vallValue[iVall - 1]
            leftLim = vallIndex[iVall - 1] - 1 - (barsChannel * 2)
            if leftLim < 0:
                leftLim = 0
            for i in range(vallIndex[iVall - 1] - 1, leftLim, -1):
                suppBuffer[i] = vallValue[iVall - 1] - (m_sup * (vallIndex[iVall - 1] - i))
            for i in range(vallIndex[iVall - 1] + 1, rates_total):
                suppBuffer[i] = (m_sup * (i - vallIndex[iVall - 1])) + vallValue[iVall - 1]
        for i in range(rates_total - barsChannel, 0 - 1, -1):
            resiBuffer[i] = 0.0
            suppBuffer[i] = 0.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ChannelDesign(_MQL5Indicator):
    name = 'ChannelDesign'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'barsChannel': 200,  # Channel creation length
        'barsMulti': 5,  # Channel bars to peak/valley
    }

