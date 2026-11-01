"""js-stohgbbcrsi — converted from MQL5: MQL5 Indicators/JS-Stoh-BB-RSI/js-stohgbbcrsi.mq5

X2MA Bollinger Bands
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 5}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}, 'colors': {1: [16711680], 2: [8421376], 3: [14822282], 4: [255], 5: [255]}, 'widths': {1: 1, 2: 1, 3: 2, 4: 1, 5: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'labels': {1: 'Stochastic', 2: 'RSI', 3: 'Stochastic Signal', 4: '+2Sigma Stochastic', 5: '-2Sigma Stochastic'}, 'levels': [80.0, 70.0, 50.0, 30.0, 20.0], 'description': ['X2MA Bollinger Bands'], 'name': 'js-stohgbbcrsi', 'source': 'MQL5 Indicators/JS-Stoh-BB-RSI/js-stohgbbcrsi.mq5', 'folder': 'JS-Stoh-BB-RSI', 'inputs': [{'mql': 'STO_KPeriod', 'py': 'STO_KPeriod', 'param': 'STO_KPeriod', 'type': 'uint', 'default': 5, 'label': 'K period of stochastic', 'sinput': False}, {'mql': 'STO_DPeriod', 'py': 'STO_DPeriod', 'param': 'STO_DPeriod', 'type': 'uint', 'default': 3, 'label': 'D period of stochastic', 'sinput': False}, {'mql': 'STO_Slowing', 'py': 'STO_Slowing', 'param': 'STO_Slowing', 'type': 'uint', 'default': 3, 'label': 'Slowing of stochastic', 'sinput': False}, {'mql': 'STO_Method', 'py': 'STO_Method', 'param': 'STO_Method', 'type': 'int', 'default': 0, 'label': 'smoothing type of stochastic', 'sinput': False}, {'mql': 'STO_Price', 'py': 'STO_Price', 'param': 'STO_Price', 'type': 'int', 'default': 0, 'label': 'stochastic calculation method', 'sinput': False}, {'mql': 'BandsPeriod', 'py': 'BandsPeriod', 'param': 'BandsPeriod', 'type': 'uint', 'default': 10, 'label': 'period of averaging of BB', 'sinput': False}, {'mql': 'BandsDeviation', 'py': 'BandsDeviation', 'param': 'BandsDeviation', 'type': 'double', 'default': 1.0, 'label': 'deviation', 'sinput': False}, {'mql': 'RSI_Period', 'py': 'RSI_Period', 'param': 'RSI_Period', 'type': 'uint', 'default': 8, 'label': 'RSI indicator period', 'sinput': False}, {'mql': 'RSI_Price', 'py': 'RSI_Price', 'param': 'RSI_Price', 'type': 'int', 'default': 1, 'label': 'price type of RSI indicator', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
STO_KPeriod = _input('STO_KPeriod', 5)  # K period of stochastic
STO_DPeriod = _input('STO_DPeriod', 3)  # D period of stochastic
STO_Slowing = _input('STO_Slowing', 3)  # Slowing of stochastic
STO_Method = _input('STO_Method', MODE_SMA)  # smoothing type of stochastic
STO_Price = _input('STO_Price', STO_LOWHIGH)  # stochastic calculation method
BandsPeriod = _input('BandsPeriod', 10)  # period of averaging of BB
BandsDeviation = _input('BandsDeviation', 1.0)  # deviation
RSI_Period = _input('RSI_Period', 8)  # RSI indicator period
RSI_Price = _input('RSI_Price', PRICE_CLOSE)  # price type of RSI indicator
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
ExtLineBuffer1 = Arr(0, 0.0)
ExtLineBuffer2 = Arr(0, 0.0)
ExtLineBuffer3 = Arr(0, 0.0)
ExtLineBuffer4 = Arr(0, 0.0)
ExtLineBuffer5 = Arr(0, 0.0)
RSI_Handle = 0
STO_Handle = 0
min_rates_total = 0
min_rates_sto = 0

def OnInit():
    global RSI_Handle, STO_Handle, min_rates_sto, min_rates_total
    min_rates_sto = _int(STO_KPeriod + STO_DPeriod + STO_Slowing + 1)
    min_rates_ = _int(min_rates_sto + BandsDeviation)
    min_rates_total = _int(MathMax(min_rates_, RSI_Period))
    RSI_Handle = iRSI(None, PERIOD_CURRENT, RSI_Period, RSI_Price)
    if RSI_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iRSI indicator')
    STO_Handle = iStochastic(None, 0, STO_KPeriod, STO_DPeriod, STO_Slowing, STO_Method, STO_Price)
    if STO_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iStochastic indicator')
    SetIndexBuffer(0, ExtLineBuffer1, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(ExtLineBuffer1, True)
    SetIndexBuffer(1, ExtLineBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(ExtLineBuffer2, True)
    SetIndexBuffer(2, ExtLineBuffer3, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(ExtLineBuffer3, True)
    SetIndexBuffer(3, ExtLineBuffer4, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(ExtLineBuffer4, True)
    SetIndexBuffer(4, ExtLineBuffer5, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(ExtLineBuffer5, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'JS-Stoh+BB+RSI')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (BarsCalculated(STO_Handle) < rates_total or BarsCalculated(RSI_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    to_copy = 0
    xmaxbar = 0
    smaxbar = 0
    stoh = 0.0
    xstoh = 0.0
    stdev = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1
    else:
        limit = rates_total - prev_calculated
    xmaxbar = rates_total - min_rates_sto - 1
    smaxbar = xmaxbar - _int(BandsPeriod)
    to_copy = limit + 1
    if CopyBuffer(STO_Handle, MAIN_LINE, 0, to_copy, ExtLineBuffer1) <= 0:
        return 0
    if CopyBuffer(RSI_Handle, MAIN_LINE, 0, to_copy, ExtLineBuffer2) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        stoh = ExtLineBuffer1[bar]
        xstoh = XMA.XMASeries(xmaxbar, prev_calculated, rates_total, MODE_SMA, 0, BandsPeriod, stoh, bar, True)
        ExtLineBuffer3[bar] = xstoh
        stdev = STD.StdDevSeries(smaxbar, prev_calculated, rates_total, BandsPeriod, BandsDeviation, stoh, xstoh, bar, True)
        ExtLineBuffer4[bar] = xstoh + stdev
        ExtLineBuffer5[bar] = xstoh - stdev
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- global variables initialised from expressions
XMA = _alloc(CXMA)
XMA.__init__()
STD = _alloc(CStdDeviation)
STD.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class JsStohgbbcrsi(_MQL5Indicator):
    name = 'js-stohgbbcrsi'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'STO_KPeriod': 5,  # K period of stochastic
        'STO_DPeriod': 3,  # D period of stochastic
        'STO_Slowing': 3,  # Slowing of stochastic
        'STO_Method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # smoothing type of stochastic
        'STO_Price': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),  # stochastic calculation method
        'BandsPeriod': 10,  # period of averaging of BB
        'BandsDeviation': 1.0,  # deviation
        'RSI_Period': 8,  # RSI indicator period
        'RSI_Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # price type of RSI indicator
        'Shift': 0,  # horizontal shift of the indicator in bars
    }

