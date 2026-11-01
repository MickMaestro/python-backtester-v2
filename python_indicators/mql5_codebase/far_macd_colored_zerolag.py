"""Far-MACD-Colored-ZeroLag — converted from MQL5: MQL5 Indicators/Colored Zerolag MACD/Far-MACD-Colored-ZeroLag.mq5

Original code by : RD - marynarz15@wp.pl \\n
Join our telegram : https://telegram.me/FXCOFOREX
\\n
Change log : 2016.11.23-Fixed some bugs in colored indicator-By Farzin.
Change log : 2016.11.28_12.06-MQL5 version-By Farzin.
Change log : 2016.12.06-MQL5 version-Recoded IMAonArray for reading all history candles.
Copyright: Copyright 2014-2017, PersiansDream Informatics Group; Link: http://my.pdhost.net/cart.php; Version: 612.069

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2014-2017, PersiansDream Informatics Group', 'link': 'http://my.pdhost.net/cart.php', 'version': '612.069', 'window': 'separate', 'indicator_buffers': 10, 'indicator_plots': 4}, 'types': {}, 'colors': {1: [0], 2: [65280], 3: [255], 4: [16711680]}, 'widths': {2: 2, 3: 2, 4: 2}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Original code by : RD - marynarz15@wp.pl \\n', 'Join our telegram : https://telegram.me/FXCOFOREX', '\\n', 'Change log : 2016.11.23-Fixed some bugs in colored indicator-By Farzin.', 'Change log : 2016.11.28_12.06-MQL5 version-By Farzin.', 'Change log : 2016.12.06-MQL5 version-Recoded IMAonArray for reading all history candles.'], 'name': 'Far-MACD-Colored-ZeroLag', 'source': 'MQL5 Indicators/Colored Zerolag MACD/Far-MACD-Colored-ZeroLag.mq5', 'folder': 'Colored Zerolag MACD', 'inputs': [{'mql': 'FastEMA', 'py': 'FastEMA', 'param': 'FastEMA', 'type': 'int', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'SlowEMA', 'py': 'SlowEMA', 'param': 'SlowEMA', 'type': 'int', 'default': 26, 'label': '', 'sinput': False}, {'mql': 'SignalEMA', 'py': 'SignalEMA', 'param': 'SignalEMA', 'type': 'int', 'default': 9, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
FastEMA = _input('FastEMA', 12)
SlowEMA = _input('SlowEMA', 26)
SignalEMA = _input('SignalEMA', 9)
FastEMAHandle = 0
SlowEMAHandle = 0
MACDBufferZeroLag = Arr(0, 0.0)
FastEMABuffer = Arr(0, 0.0)
SlowEMABuffer = Arr(0, 0.0)
EMApArray = Arr(0, 0.0)
EMAqArray = Arr(0, 0.0)
SignalEMAArray = Arr(0, 0.0)
SignalEMABuffer = Arr(0, 0.0)
SignalBuffer = Arr(0, 0.0)
Buffer1 = Arr(0, 0.0)
Buffer2 = Arr(0, 0.0)

def OnInit():
    global FastEMAHandle, SlowEMAHandle
    MACDresult = SetIndexBuffer(0, MACDBufferZeroLag, INDICATOR_DATA)
    SetIndexBuffer(1, Buffer1, INDICATOR_DATA)
    SetIndexBuffer(2, Buffer2, INDICATOR_DATA)
    SetIndexBuffer(3, SignalBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, FastEMABuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, SlowEMABuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, EMApArray, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, EMAqArray, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, SignalEMAArray, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, SignalEMABuffer, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_NONE)
    PlotIndexSetInteger(1, PLOT_DRAW_TYPE, DRAW_HISTOGRAM)
    PlotIndexSetInteger(2, PLOT_DRAW_TYPE, DRAW_HISTOGRAM)
    PlotIndexSetInteger(3, PLOT_DRAW_TYPE, DRAW_LINE)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, SlowEMA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, SlowEMA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, SlowEMA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, SlowEMA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Far-ZeroLag MACD Colored(' + _str(FastEMA) + ',' + _str(SlowEMA) + ',' + _str(SignalEMA) + ')')
    MACDplotResult = PlotIndexSetString(0, PLOT_LABEL, 'MACD')
    PlotIndexSetString(1, PLOT_LABEL, 'MACD-Growing')
    PlotIndexSetString(2, PLOT_LABEL, 'MACD-Decreasing')
    PlotIndexSetString(3, PLOT_LABEL, 'Signal')
    FastEMAHandle = iMA(None, PERIOD_CURRENT, FastEMA, 0, MODE_EMA, PRICE_CLOSE)
    SlowEMAHandle = iMA(None, PERIOD_CURRENT, SlowEMA, 0, MODE_EMA, PRICE_CLOSE)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    Print('OnDeinit', '_Uninitalization reason code = ', reason)
    Print('OnDeinit', '_UninitReason = ', getUninitReasonText(0))

def getUninitReasonText(reasonCode):
    text = ''
    _sw1 = reasonCode
    if _sw1 == REASON_PROGRAM:
        text = 'Expert Advisor terminated its operation by calling the ExpertRemove() function'
    elif _sw1 == REASON_ACCOUNT:
        text = 'Account was changed'
    elif _sw1 == REASON_CHARTCHANGE:
        text = 'Symbol or timeframe was changed'
    elif _sw1 == REASON_CHARTCLOSE:
        text = 'Chart was closed'
    elif _sw1 == REASON_PARAMETERS:
        text = 'Input-parameter was changed'
    elif _sw1 == REASON_RECOMPILE:
        text = 'Program ' + 'Far-MACD-Colored-ZeroLag.mq5' + ' was recompiled'
    elif _sw1 == REASON_REMOVE:
        text = 'Program ' + 'Far-MACD-Colored-ZeroLag.mq5' + ' was removed from chart'
    elif _sw1 == REASON_TEMPLATE:
        text = 'New template was applied to chart'
    else:
        text = 'Another reason'
    return text

def iMAOnArrayMQL4(array, dstArray, period, shift):
    pr = _fdiv(2.0, period + 1)
    if shift == (Bars(Symbol(), Period()) - 1):
        dstArray[shift] = array[shift]
    if shift < (Bars(Symbol(), Period()) - 1):
        dstArray[shift] = NormalizeDouble((array[shift] * pr) + (dstArray[shift + 1] * (1 - pr)), 6)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < SlowEMA:
        Print(_str(176) + '-Error : Not enough Data is available.')
        return 0
    calculated = BarsCalculated(FastEMAHandle)
    if calculated < rates_total:
        Print('Not all data of FastEMAHandle is calculated (', calculated, 'bars ). Error', GetLastError())
        return 0
    SlowEMAcalculated = BarsCalculated(SlowEMAHandle)
    if SlowEMAcalculated < rates_total:
        Print('Not all data of SlowEMAHandle is calculated (', SlowEMAcalculated, 'bars ). Error', GetLastError())
        return 0
    to_copy = 0
    if prev_calculated > rates_total or prev_calculated < 0:
        to_copy = rates_total
    else:
        to_copy = rates_total - prev_calculated
        if prev_calculated > 0:
            to_copy += 1
    if False:
        Print(_str(201) + '-Stop Flag is active')
        return 0
    if CopyBuffer(FastEMAHandle, 0, 0, to_copy, FastEMABuffer) <= 0:
        Print('Error : Getting fast EMA is failed! Error', GetLastError())
        return 0
    if CopyBuffer(SlowEMAHandle, 0, 0, to_copy, SlowEMABuffer) <= 0:
        Print('Error : Getting slow EMA is failed! Error', GetLastError())
        return 0
    if prev_calculated == 0:
        SignalInitZero = ArrayInitialize(SignalBuffer, 0)
        Buffer1InitZero = ArrayInitialize(Buffer1, 0)
        Buffer2InitZero = ArrayInitialize(Buffer2, 0)
    ZeroLagEMAp = 0.0
    ZeroLagEMAq = 0.0
    CandleLimiter = 0
    if prev_calculated > 0:
        CandleLimiter = rates_total - 3
    for i in range(rates_total - 1, CandleLimiter, -1):
        iMAOnArrayMQL4(FastEMABuffer, EMApArray, FastEMA, i)
        ZeroLagEMAp = FastEMABuffer[i] + FastEMABuffer[i] - EMApArray[i]
        iMAOnArrayMQL4(SlowEMABuffer, EMAqArray, SlowEMA, i)
        ZeroLagEMAq = SlowEMABuffer[i] + SlowEMABuffer[i] - EMAqArray[i]
        MACDBufferZeroLag[i] = ZeroLagEMAp - ZeroLagEMAq
        iMAOnArrayMQL4(MACDBufferZeroLag, SignalEMAArray, SignalEMA, i)
        iMAOnArrayMQL4(SignalEMAArray, SignalEMABuffer, SignalEMA, i)
        SignalBuffer[i] = (2 * SignalEMAArray[i]) - SignalEMABuffer[i]
    up = True
    prev = 0.0
    current = 0.0
    for i in range(rates_total - 1, CandleLimiter, -1):
        current = MACDBufferZeroLag[i]
        prev = MACDBufferZeroLag[i - 1]
        if current > prev:
            up = True
        if current < prev:
            up = False
        if not up:
            Buffer2[i] = current
            Buffer1[i] = 0.0
        else:
            Buffer1[i] = current
            Buffer2[i] = 0.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FarMACDColoredZeroLag(_MQL5Indicator):
    name = 'Far-MACD-Colored-ZeroLag'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'FastEMA': 12,
        'SlowEMA': 26,
        'SignalEMA': 9,
    }

