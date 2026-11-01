"""BB_OsMA — converted from MQL5: MQL5 Indicators/BB_OsMA/BB_OsMA.mq5

BB_OsMA indicator is the Forex indicators for MT5.
BB_OsMA indicator is the OsMA indicator in the form of spheroid,
with a deviation as the upper and lower bands.
Copyright: Copyright 2016, MetaQuotes Ltd. ~ By 3rjfx ~ Created: 2016/01/25; Link: https://www.mql5.com/en/users/3rjfx; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2016, MetaQuotes Ltd. ~ By 3rjfx ~ Created: 2016/01/25', 'link': 'https://www.mql5.com/en/users/3rjfx', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 11, 'indicator_plots': 4}, 'types': {1: 5, 2: 5, 3: 1, 4: 1, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0}, 'colors': {1: [16776960], 2: [65535], 3: [16748574], 4: [255]}, 'widths': {1: 2, 2: 2, 3: 1, 4: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'OsMAUps', 2: 'OsMADown', 3: 'UpperBand', 4: 'LowerBand'}, 'levels': [], 'description': ['BB_OsMA indicator is the Forex indicators for MT5.', 'BB_OsMA indicator is the OsMA indicator in the form of spheroid,', 'with a deviation as the upper and lower bands.'], 'name': 'BB_OsMA', 'source': 'MQL5 Indicators/BB_OsMA/BB_OsMA.mq5', 'folder': 'BB_OsMA', 'inputs': [{'mql': 'eprice', 'py': 'eprice', 'param': 'eprice', 'type': 'int', 'default': 7, 'label': 'Select MA Applied price', 'sinput': False}, {'mql': 'OsMAFastEMA', 'py': 'OsMAFastEMA', 'param': 'OsMAFastEMA', 'type': 'int', 'default': 12, 'label': 'Fast EMA Period', 'sinput': False}, {'mql': 'OsMASlowEMA', 'py': 'OsMASlowEMA', 'param': 'OsMASlowEMA', 'type': 'int', 'default': 26, 'label': 'Slow EMA Period', 'sinput': False}, {'mql': 'OsMASignalEMA', 'py': 'OsMASignalEMA', 'param': 'OsMASignalEMA', 'type': 'int', 'default': 9, 'label': 'Signal EMA Period', 'sinput': False}, {'mql': 'StdDev', 'py': 'StdDev', 'param': 'StdDev', 'type': 'double', 'default': 2.0, 'label': 'Standard Deviation', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
eprice = _input('eprice', PRICE_WEIGHTED)  # Select MA Applied price
OsMAFastEMA = _input('OsMAFastEMA', 12)  # Fast EMA Period
OsMASlowEMA = _input('OsMASlowEMA', 26)  # Slow EMA Period
OsMASignalEMA = _input('OsMASignalEMA', 9)  # Signal EMA Period
StdDev = _input('StdDev', 2.0)  # Standard Deviation
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
arrcode = 159
OsMAFast = 0
OsMASlow = 0
hStdDev = 0

def OnInit():
    global OsMAFast, OsMASlow, hStdDev
    SetIndexBuffer(0, OsMABuffUp, INDICATOR_DATA)
    SetIndexBuffer(1, OsMABuffDn, INDICATOR_DATA)
    SetIndexBuffer(2, OsMAUpBand, INDICATOR_DATA)
    SetIndexBuffer(3, OsMALoBand, INDICATOR_DATA)
    SetIndexBuffer(4, OsMABuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, exOsMAMacd, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, exOsMASign, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, OsMAStdDev, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, OsMAAvg, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, OsMAFastBuffers, INDICATOR_CALCULATIONS)
    SetIndexBuffer(10, OsMASlowBuffers, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_ARROW, arrcode)
    PlotIndexSetInteger(1, PLOT_ARROW, arrcode)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, OsAvgPeriod)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, OsAvgPeriod)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, OsAvgPeriod)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, OsAvgPeriod)
    shortname = 'BB_OsMA(' + _str(OsMAFastEMA) + ',' + _str(OsMASlowEMA) + ',' + _str(OsMASignalEMA) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    if OsMAFastEMA >= OsMASlowEMA:
        return INIT_FAILED
    OsMAFast = iMA(Symbol(), PERIOD_CURRENT, OsMAFastEMA, 0, MODE_EMA, eprice)
    if OsMAFast == INVALID_HANDLE:
        printf('Error creating indicator OsMAFastEMA for ', Symbol())
        return INIT_FAILED
    OsMASlow = iMA(Symbol(), PERIOD_CURRENT, OsMASlowEMA, 0, MODE_EMA, eprice)
    if OsMASlow == INVALID_HANDLE:
        printf('Error creating indicator OsMASlowEMA for ', Symbol())
        return INIT_FAILED
    hStdDev = iStdDev(Symbol(), 0, OsAvgPeriod, 0, MODE_SMA, eprice)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectsDeleteAll(ChartID(), 0, -1)
    GlobalVariablesDeleteAll()
    return

def OnCalculate(rates_total, prev_calculated, begin, price):
    ResetLastError()
    x = 0
    xlimit = 0
    OsMADiv = _idiv(OsMASlowEMA, OsMAFastEMA)
    if rates_total <= OsMASignalEMA:
        return 0
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
    if CopyBuffer(hStdDev, 0, 0, to_copy, OsMAStdDev) < 0:
        Print('Getting OsMAStdDev buffers is failed! Error', GetLastError())
        return 0
    if prev_calculated == 0:
        xlimit = 0
    else:
        xlimit = prev_calculated - 2
    x = calculated - 1
    for x in range(x, 0 - 1, -1):
        exOsMAMacd[x] = OsMAFastBuffers[x] - OsMASlowBuffers[x]
    else:
        x = _range_end(x, 0 - 1, -1)
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, OsMASignalEMA, exOsMAMacd, exOsMASign)
    x = calculated - 1
    for x in range(x, 0 - 1, -1):
        OsMABuffer[x] = (exOsMAMacd[x] - exOsMASign[x]) * OsMADiv
    else:
        x = _range_end(x, 0 - 1, -1)
    SimpleMAOnBuffer(rates_total, prev_calculated, 0, OsAvgPeriod, OsMABuffer, OsMAAvg)
    ArraySetAsSeries(OsMAFastBuffers, True)
    ArraySetAsSeries(OsMASlowBuffers, True)
    ArraySetAsSeries(exOsMAMacd, True)
    ArraySetAsSeries(exOsMASign, True)
    ArraySetAsSeries(OsMAUpBand, True)
    ArraySetAsSeries(OsMALoBand, True)
    ArraySetAsSeries(OsMABuffUp, True)
    ArraySetAsSeries(OsMABuffDn, True)
    ArraySetAsSeries(OsMAAvg, True)
    ArraySetAsSeries(OsMABuffer, True)
    ArraySetAsSeries(OsMAStdDev, True)
    x = calculated - 2
    for x in range(x, 0 - 1, -1):
        if OsMABuffer[x] > OsMABuffer[x + 1]:
            OsMABuffUp[x] = OsMABuffer[x]
            OsMABuffDn[x] = EMPTY_VALUE
        if OsMABuffer[x] < OsMABuffer[x + 1]:
            OsMABuffDn[x] = OsMABuffer[x]
            OsMABuffUp[x] = EMPTY_VALUE
        OsMAUpBand[x] = OsMAAvg[x] + (StdDev * OsMAStdDev[x])
        OsMALoBand[x] = OsMAAvg[x] - (StdDev * OsMAStdDev[x])
    else:
        x = _range_end(x, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BBOsMA(_MQL5Indicator):
    name = 'BB_OsMA'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'eprice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=7),  # Select MA Applied price
        'OsMAFastEMA': 12,  # Fast EMA Period
        'OsMASlowEMA': 26,  # Slow EMA Period
        'OsMASignalEMA': 9,  # Signal EMA Period
        'StdDev': 2.0,  # Standard Deviation
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

