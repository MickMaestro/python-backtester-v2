"""BB_OsMA — converted from MQL5: MQL5 Indicators/BB_OsMA_HTF/BB_OsMA.mq5

BB_OsMA indicator is the Forex indicators for MT5.
BB_OsMA indicator is the OsMA indicator in the form of spheroid,
with a deviation as the upper and lower bands.
Copyright: 2016, MetaQuotes Software Corp. ~ By 3rjfx ~ Created: 2016/01/25; Link: https://www.mql5.com/en/users/3rjfx; Version: 1.10

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': '2016, MetaQuotes Software Corp. ~ By 3rjfx ~ Created: 2016/01/25', 'link': 'https://www.mql5.com/en/users/3rjfx', 'version': '1.10', 'window': 'separate', 'indicator_buffers': 11, 'indicator_plots': 11}, 'types': {1: 0, 2: 0, 3: 0, 4: 5, 5: 5, 6: 1, 7: 1, 8: 0, 9: 0, 10: 0, 11: 0}, 'colors': {}, 'widths': {4: 1, 5: 1, 6: 1, 7: 1}, 'styles': {4: 0, 5: 0, 6: 0, 7: 0}, 'labels': {4: 'OsMAUps', 5: 'OsMADown', 6: 'UpperBand', 7: 'LowerBand'}, 'levels': [], 'description': ['BB_OsMA indicator is the Forex indicators for MT5.', 'BB_OsMA indicator is the OsMA indicator in the form of spheroid,', 'with a deviation as the upper and lower bands.'], 'name': 'BB_OsMA', 'source': 'MQL5 Indicators/BB_OsMA_HTF/BB_OsMA.mq5', 'folder': 'BB_OsMA_HTF', 'inputs': [{'mql': 'OsMAFastEMA', 'py': 'OsMAFastEMA', 'param': 'OsMAFastEMA', 'type': 'int', 'default': 26, 'label': 'Fast EMA Period', 'sinput': False}, {'mql': 'OsMASlowEMA', 'py': 'OsMASlowEMA', 'param': 'OsMASlowEMA', 'type': 'int', 'default': 130, 'label': 'Slow EMA Period', 'sinput': False}, {'mql': 'OsMASignalEMA', 'py': 'OsMASignalEMA', 'param': 'OsMASignalEMA', 'type': 'int', 'default': 13, 'label': 'Signal SMA Period', 'sinput': False}, {'mql': 'StdDev', 'py': 'StdDev', 'param': 'StdDev', 'type': 'double', 'default': 2.0, 'label': 'Standard Deviation', 'sinput': False}, {'mql': 'OsMAColorArrowUp', 'py': 'OsMAColorArrowUp', 'param': None, 'type': 'color', 'default': 16711680, 'label': 'Arrow Up', 'sinput': False}, {'mql': 'OsMAColorArrowDn', 'py': 'OsMAColorArrowDn', 'param': None, 'type': 'color', 'default': 255, 'label': 'Arrow Down', 'sinput': False}, {'mql': 'OsMAColorLineUp', 'py': 'OsMAColorLineUp', 'param': None, 'type': 'color', 'default': 16711680, 'label': 'Line Up', 'sinput': False}, {'mql': 'OsMAColorLineDn', 'py': 'OsMAColorLineDn', 'param': None, 'type': 'color', 'default': 4294967295, 'label': 'Line Down', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
OsMAFastEMA = _input('OsMAFastEMA', 26)  # Fast EMA Period
OsMASlowEMA = _input('OsMASlowEMA', 130)  # Slow EMA Period
OsMASignalEMA = _input('OsMASignalEMA', 13)  # Signal SMA Period
StdDev = _input('StdDev', 2.0)  # Standard Deviation
OsMAColorArrowUp = _input('OsMAColorArrowUp', clrBlue)  # Arrow Up
OsMAColorArrowDn = _input('OsMAColorArrowDn', clrRed)  # Arrow Down
OsMAColorLineUp = _input('OsMAColorLineUp', clrBlue)  # Line Up
OsMAColorLineDn = _input('OsMAColorLineDn', clrNONE)  # Line Down
OsMABuffer = Arr(0, 0.0)
exOsMAMacd = Arr(0, 0.0)
exOsMASign = Arr(0, 0.0)
OsMABuffUp = Arr(0, 0.0)
OsMABuffDn = Arr(0, 0.0)
OsMAUpBand = Arr(0, 0.0)
OsMALoBand = Arr(0, 0.0)
OsMAStdDev = Arr(0, 0.0)
OsMAFastBuffers = Arr(0, 0.0)
OsMASlowBuffers = Arr(0, 0.0)
OsMAAvg = Arr(0, 0.0)
OsAvgPeriod = 20
OsMAFast = 0
OsMASlow = 0

def OnInit():
    global OsMAFast, OsMASlow
    SetIndexBuffer(0, OsMABuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(1, exOsMAMacd, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, exOsMASign, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, OsMABuffUp, INDICATOR_DATA)
    SetIndexBuffer(4, OsMABuffDn, INDICATOR_DATA)
    SetIndexBuffer(5, OsMAUpBand, INDICATOR_DATA)
    SetIndexBuffer(6, OsMALoBand, INDICATOR_DATA)
    SetIndexBuffer(7, OsMAStdDev, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, OsMAAvg, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, OsMAFastBuffers, INDICATOR_CALCULATIONS)
    SetIndexBuffer(10, OsMASlowBuffers, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(3, PLOT_ARROW, 108)
    PlotIndexSetInteger(4, PLOT_ARROW, 108)
    PlotIndexSetInteger(3, PLOT_LINE_COLOR, OsMAColorArrowUp)
    PlotIndexSetInteger(4, PLOT_LINE_COLOR, OsMAColorArrowDn)
    PlotIndexSetInteger(5, PLOT_LINE_COLOR, OsMAColorLineUp)
    PlotIndexSetInteger(6, PLOT_LINE_COLOR, OsMAColorLineDn)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, OsAvgPeriod)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, OsAvgPeriod)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, OsAvgPeriod)
    PlotIndexSetInteger(6, PLOT_DRAW_BEGIN, OsAvgPeriod)
    shortname = 'BB_OsMA(' + _str(OsMAFastEMA) + ',' + _str(OsMASlowEMA) + ',' + _str(OsMASignalEMA) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    OsMAFast = iMA(Symbol(), PERIOD_CURRENT, OsMAFastEMA, 0, MODE_EMA, PRICE_WEIGHTED)
    if OsMAFast == INVALID_HANDLE:
        printf('Error creating indicator OsMAFastEMA for ', Symbol())
        return INIT_FAILED
    OsMASlow = iMA(Symbol(), PERIOD_CURRENT, OsMASlowEMA, 0, MODE_EMA, PRICE_WEIGHTED)
    if OsMASlow == INVALID_HANDLE:
        printf('Error creating indicator OsMASlowEMA for ', Symbol())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectsDeleteAll(ChartID(), 0, -1)
    GlobalVariablesDeleteAll()
    return

def OnCalculate(rates_total, prev_calculated, begin, price):
    x = 0
    xlimit = 0
    OsMADiv = _idiv(OsMASlowEMA, OsMAFastEMA)
    if rates_total <= OsMASignalEMA:
        return 0
    ResetLastError()
    calculated = BarsCalculated(OsMAFast)
    if calculated < rates_total:
        Print('Not all data of OsMAFast is calculated (', calculated, 'bars ). Error', GetLastError())
        return 0
    calculated = BarsCalculated(OsMASlow)
    if calculated < rates_total:
        Print('Not all data of OsMASlow is calculated (', calculated, 'bars ). Error', GetLastError())
        return 0
    to_copy = 0
    if prev_calculated > rates_total or prev_calculated < 0:
        to_copy = rates_total
    else:
        to_copy = rates_total - prev_calculated
        if prev_calculated > 0:
            to_copy += 1
    if False:
        return 0
    if CopyBuffer(OsMAFast, 0, 0, to_copy, OsMAFastBuffers) < 0:
        Print('Getting ExtMaFastHandle buffers is failed! Error', GetLastError())
        return 0
    if False:
        return 0
    if CopyBuffer(OsMASlow, 0, 0, to_copy, OsMASlowBuffers) < 0:
        Print('Getting ExtMaSlowHandle buffers is failed! Error', GetLastError())
        return 0
    if prev_calculated == 0:
        xlimit = 0
    else:
        xlimit = prev_calculated - 1
    x = calculated - 1
    for x in range(x, xlimit - 1, -1):
        exOsMAMacd[x] = OsMAFastBuffers[x] - OsMASlowBuffers[x]
    else:
        x = _range_end(x, xlimit - 1, -1)
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, OsMASignalEMA, exOsMAMacd, exOsMASign)
    x = calculated - 1
    for x in range(x, xlimit - 1, -1):
        OsMABuffer[x] = (exOsMAMacd[x] - exOsMASign[x]) * OsMADiv
    else:
        x = _range_end(x, xlimit - 1, -1)
    SimpleMAOnBuffer(rates_total, prev_calculated, 0, OsAvgPeriod, OsMABuffer, OsMAAvg)
    x = calculated - 1
    for x in range(x, xlimit - 1, -1):
        OsMAStdDev[x] = iStdDevOnArray(OsMABuffer, OsAvgPeriod, x)
    else:
        x = _range_end(x, xlimit - 1, -1)
    x = calculated - 1
    for x in range(x, xlimit, -1):
        OsMAUpBand[x] = OsMAAvg[x] + (StdDev * OsMAStdDev[x])
        OsMALoBand[x] = OsMAAvg[x] - (StdDev * OsMAStdDev[x])
        OsMABuffUp[x] = OsMABuffer[x]
        OsMABuffDn[x] = OsMABuffer[x]
        if OsMABuffer[x] > OsMABuffer[x - 1]:
            OsMABuffDn[x] = EMPTY_VALUE
        if OsMABuffer[x] < OsMABuffer[x - 1]:
            OsMABuffUp[x] = EMPTY_VALUE
    else:
        x = _range_end(x, xlimit, -1)
    return rates_total

def iStdDevOnArray(MAprice, period, position):
    dTmp = 0.0
    as_series_buffer = ArrayGetAsSeries(MAprice)
    if as_series_buffer:
        ArraySetAsSeries(MAprice, False)
    if position < period:
        return dTmp
    for i in range(0, period):
        dTmp += MathPow(MAprice[position - i] - MAprice[position], 2)
    dTmp = MathSqrt(_fdiv(dTmp, period))
    if as_series_buffer:
        ArraySetAsSeries(MAprice, True)
    return dTmp


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BBOsMA(_MQL5Indicator):
    name = 'BB_OsMA'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'OsMAFastEMA': 26,  # Fast EMA Period
        'OsMASlowEMA': 130,  # Slow EMA Period
        'OsMASignalEMA': 13,  # Signal SMA Period
        'StdDev': 2.0,  # Standard Deviation
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

