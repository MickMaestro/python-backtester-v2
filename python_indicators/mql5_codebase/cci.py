"""cci — converted from MQL5: MQL5 Indicators/Commodity Channel Index (CCI)/cci.mq5

Commodity Channel Index
Copyright: 2009, MetaQuotes Software Corp.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': '2009, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [11186720]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [-100.0, 100.0], 'description': ['Commodity Channel Index'], 'name': 'cci', 'source': 'MQL5 Indicators/Commodity Channel Index (CCI)/cci.mq5', 'folder': 'Commodity Channel Index (CCI)', 'inputs': [{'mql': 'InpCCIPeriod', 'py': 'InpCCIPeriod', 'param': 'InpCCIPeriod', 'type': 'int', 'default': 14, 'label': 'Period', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpCCIPeriod = _input('InpCCIPeriod', 14)  # Period
ExtCCIPeriod = 0
ExtSPBuffer = Arr(0, 0.0)
ExtDBuffer = Arr(0, 0.0)
ExtMBuffer = Arr(0, 0.0)
ExtCCIBuffer = Arr(0, 0.0)

def OnInit():
    global ExtCCIPeriod
    if InpCCIPeriod <= 0:
        ExtCCIPeriod = 14
        printf('Incorrect value for input variable InpCCIPeriod=%d. Indicator will use value=%d for calculations.', InpCCIPeriod, ExtCCIPeriod)
    else:
        ExtCCIPeriod = InpCCIPeriod
    SetIndexBuffer(0, ExtCCIBuffer)
    SetIndexBuffer(1, ExtDBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, ExtMBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, ExtSPBuffer, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'CCI(' + _str(ExtCCIPeriod) + ')')
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, ExtCCIPeriod - 1)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)

def OnCalculate(rates_total, prev_calculated, begin, price):
    i = 0
    j = 0
    dTmp = 0.0
    dMul = _fdiv(0.015, ExtCCIPeriod)
    StartCalcPosition = ExtCCIPeriod - 1 + begin
    if rates_total < StartCalcPosition:
        return 0
    if begin > 0:
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, StartCalcPosition + (ExtCCIPeriod - 1))
    pos = prev_calculated - 1
    if pos < StartCalcPosition:
        pos = StartCalcPosition
    i = pos
    for i in range(i, rates_total):
        ExtSPBuffer[i] = SimpleMA(i, ExtCCIPeriod, price)
        dTmp = 0.0
        j = 0
        for j in range(j, ExtCCIPeriod):
            dTmp += MathAbs(price[i - j] - ExtSPBuffer[i])
        else:
            j = _range_end(j, ExtCCIPeriod, 1)
        ExtDBuffer[i] = dTmp * dMul
        ExtMBuffer[i] = price[i] - ExtSPBuffer[i]
        if ExtDBuffer[i] != 0.0:
            ExtCCIBuffer[i] = _fdiv(ExtMBuffer[i], ExtDBuffer[i])
        else:
            ExtCCIBuffer[i] = 0.0
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Cci(_MQL5Indicator):
    name = 'cci'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpCCIPeriod': 14,  # Period
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

