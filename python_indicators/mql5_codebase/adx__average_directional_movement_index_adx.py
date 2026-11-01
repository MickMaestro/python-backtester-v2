"""adx — converted from MQL5: MQL5 Indicators/Average Directional Movement Index (ADX)/adx.mq5

Average Directional Movement Index
Copyright: 2009, MetaQuotes Software Corp.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': '2009, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [11186720], 2: [3329434], 3: [11788021]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 2, 3: 2}, 'labels': {1: 'ADX', 2: '+DI', 3: '-DI'}, 'levels': [], 'description': ['Average Directional Movement Index'], 'name': 'adx', 'source': 'MQL5 Indicators/Average Directional Movement Index (ADX)/adx.mq5', 'folder': 'Average Directional Movement Index (ADX)', 'inputs': [{'mql': 'InpPeriodADX', 'py': 'InpPeriodADX', 'param': 'InpPeriodADX', 'type': 'int', 'default': 14, 'label': 'Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriodADX = _input('InpPeriodADX', 14)  # Period
ExtADXBuffer = Arr(0, 0.0)
ExtPDIBuffer = Arr(0, 0.0)
ExtNDIBuffer = Arr(0, 0.0)
ExtPDBuffer = Arr(0, 0.0)
ExtNDBuffer = Arr(0, 0.0)
ExtTmpBuffer = Arr(0, 0.0)
ExtADXPeriod = 0

def OnInit():
    global ExtADXPeriod
    if InpPeriodADX >= 100 or InpPeriodADX <= 0:
        ExtADXPeriod = 14
        printf('Incorrect value for input variable Period_ADX=%d. Indicator will use value=%d for calculations.', InpPeriodADX, ExtADXPeriod)
    else:
        ExtADXPeriod = InpPeriodADX
    SetIndexBuffer(0, ExtADXBuffer)
    SetIndexBuffer(1, ExtPDIBuffer)
    SetIndexBuffer(2, ExtNDIBuffer)
    SetIndexBuffer(3, ExtPDBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, ExtNDBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, ExtTmpBuffer, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, _int(ExtADXPeriod << 1))
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, ExtADXPeriod)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, ExtADXPeriod)
    short_name = 'ADX(' + _str(ExtADXPeriod) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    PlotIndexSetString(0, PLOT_LABEL, short_name)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    if rates_total < ExtADXPeriod:
        return 0
    start = 0
    if prev_calculated > 1:
        start = prev_calculated - 1
    else:
        start = 1
        ExtPDIBuffer[0] = 0.0
        ExtNDIBuffer[0] = 0.0
        ExtADXBuffer[0] = 0.0
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
        if dTmpP > dTmpN:
            dTmpN = 0.0
        else:
            if dTmpP < dTmpN:
                dTmpP = 0.0
            else:
                dTmpP = 0.0
                dTmpN = 0.0
        tr = MathMax(MathMax(MathAbs(Hi - Lo), MathAbs(Hi - prevCl)), MathAbs(Lo - prevCl))
        if tr != 0.0:
            ExtPDBuffer[i] = _fdiv(100.0 * dTmpP, tr)
            ExtNDBuffer[i] = _fdiv(100.0 * dTmpN, tr)
        else:
            ExtPDBuffer[i] = 0.0
            ExtNDBuffer[i] = 0.0
        ExtPDIBuffer[i] = ExponentialMA(i, ExtADXPeriod, ExtPDIBuffer[i - 1], ExtPDBuffer)
        ExtNDIBuffer[i] = ExponentialMA(i, ExtADXPeriod, ExtNDIBuffer[i - 1], ExtNDBuffer)
        dTmp = ExtPDIBuffer[i] + ExtNDIBuffer[i]
        if dTmp != 0.0:
            dTmp = 100.0 * MathAbs(_fdiv(ExtPDIBuffer[i] - ExtNDIBuffer[i], dTmp))
        else:
            dTmp = 0.0
        ExtTmpBuffer[i] = dTmp
        ExtADXBuffer[i] = ExponentialMA(i, ExtADXPeriod, ExtADXBuffer[i - 1], ExtTmpBuffer)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Adx(_MQL5Indicator):
    name = 'adx'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodADX': 14,  # Period
    }

