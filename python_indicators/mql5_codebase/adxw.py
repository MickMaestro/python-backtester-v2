"""adxw — converted from MQL5: MQL5 Indicators/Average Directional Movement Index Wilder/adxw.mq5

Average Directional Movement Index
by Welles Wilder
Copyright: 2009, MetaQuotes Software Corp.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': '2009, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'window': 'separate', 'indicator_buffers': 10, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [11186720], 2: [3329434], 3: [11788021]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 2, 3: 2}, 'labels': {1: 'ADX Wilder', 2: '+DI', 3: '-DI'}, 'levels': [], 'description': ['Average Directional Movement Index', 'by Welles Wilder'], 'name': 'adxw', 'source': 'MQL5 Indicators/Average Directional Movement Index Wilder/adxw.mq5', 'folder': 'Average Directional Movement Index Wilder', 'inputs': [{'mql': 'InpPeriodADXW', 'py': 'InpPeriodADXW', 'param': 'InpPeriodADXW', 'type': 'int', 'default': 14, 'label': 'Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriodADXW = _input('InpPeriodADXW', 14)  # Period
ExtADXWBuffer = Arr(0, 0.0)
ExtPDIBuffer = Arr(0, 0.0)
ExtNDIBuffer = Arr(0, 0.0)
ExtPDSBuffer = Arr(0, 0.0)
ExtNDSBuffer = Arr(0, 0.0)
ExtPDBuffer = Arr(0, 0.0)
ExtNDBuffer = Arr(0, 0.0)
ExtTRBuffer = Arr(0, 0.0)
ExtATRBuffer = Arr(0, 0.0)
ExtDXBuffer = Arr(0, 0.0)
ExtADXWPeriod = 0

def OnInit():
    global ExtADXWPeriod
    if InpPeriodADXW >= 100 or InpPeriodADXW <= 0:
        ExtADXWPeriod = 14
        printf('Incorrect value for input variable InpPeriodADXW=%d. Indicator will use value=%d for calculations.', InpPeriodADXW, ExtADXWPeriod)
    else:
        ExtADXWPeriod = InpPeriodADXW
    SetIndexBuffer(0, ExtADXWBuffer)
    SetIndexBuffer(1, ExtPDIBuffer)
    SetIndexBuffer(2, ExtNDIBuffer)
    SetIndexBuffer(3, ExtPDBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, ExtNDBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, ExtDXBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, ExtTRBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, ExtATRBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, ExtPDSBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, ExtNDSBuffer, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, _int(ExtADXWPeriod << 1))
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, ExtADXWPeriod + 1)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, ExtADXWPeriod + 1)
    short_name = 'ADX Wilder(' + _str(ExtADXWPeriod) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    PlotIndexSetString(0, PLOT_LABEL, short_name)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    if rates_total < ExtADXWPeriod:
        return 0
    start = 0
    if prev_calculated > 1:
        start = prev_calculated - 1
    else:
        start = 1
        for i in range(0, ExtADXWPeriod):
            ExtADXWBuffer[i] = 0.0
            ExtPDIBuffer[i] = 0.0
            ExtNDIBuffer[i] = 0.0
            ExtPDSBuffer[i] = 0.0
            ExtNDSBuffer[i] = 0.0
            ExtPDBuffer[i] = 0.0
            ExtNDBuffer[i] = 0.0
            ExtTRBuffer[i] = 0.0
            ExtATRBuffer[i] = 0.0
            ExtDXBuffer[i] = 0.0
    for i in range(start, rates_total):
        Hi = High[i]
        prevHi = High[i - 1]
        Lo = Low[i]
        prevLo = Low[i - 1]
        prevCl = Close[i - 1]
        dTmpP = Hi - prevHi
        dTmpN = prevLo - Lo
        if dTmpP < 0.0:
            dTmpP = 0.0
        if dTmpN < 0.0:
            dTmpN = 0.0
        if dTmpN == dTmpP:
            dTmpN = 0.0
            dTmpP = 0.0
        else:
            if dTmpP < dTmpN:
                dTmpP = 0.0
            else:
                dTmpN = 0.0
        ExtPDBuffer[i] = dTmpP
        ExtNDBuffer[i] = dTmpN
        tr = MathMax(MathMax(MathAbs(Hi - Lo), MathAbs(Hi - prevCl)), MathAbs(Lo - prevCl))
        ExtTRBuffer[i] = tr
        if i < ExtADXWPeriod:
            ExtATRBuffer[i] = 0.0
            ExtPDIBuffer[i] = 0.0
            ExtNDIBuffer[i] = 0.0
        else:
            ExtATRBuffer[i] = SmoothedMA(i, ExtADXWPeriod, ExtATRBuffer[i - 1], ExtTRBuffer)
            ExtPDSBuffer[i] = SmoothedMA(i, ExtADXWPeriod, ExtPDSBuffer[i - 1], ExtPDBuffer)
            ExtNDSBuffer[i] = SmoothedMA(i, ExtADXWPeriod, ExtNDSBuffer[i - 1], ExtNDBuffer)
        if ExtATRBuffer[i] != 0.0:
            ExtPDIBuffer[i] = _fdiv(100.0 * ExtPDSBuffer[i], ExtATRBuffer[i])
            ExtNDIBuffer[i] = _fdiv(100.0 * ExtNDSBuffer[i], ExtATRBuffer[i])
        else:
            ExtPDIBuffer[i] = 0.0
            ExtNDIBuffer[i] = 0.0
        dTmp = ExtPDIBuffer[i] + ExtNDIBuffer[i]
        if dTmp != 0.0:
            dTmp = 100.0 * MathAbs(_fdiv(ExtPDIBuffer[i] - ExtNDIBuffer[i], dTmp))
        else:
            dTmp = 0.0
        ExtDXBuffer[i] = dTmp
        ExtADXWBuffer[i] = SmoothedMA(i, ExtADXWPeriod, ExtADXWBuffer[i - 1], ExtDXBuffer)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Adxw(_MQL5Indicator):
    name = 'adxw'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodADXW': 14,  # Period
    }

