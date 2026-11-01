"""3d_oscilator — converted from MQL5: MQL5 Indicators/3D_Oscilator/3d_oscilator.mq5

Copyright: Author - Luis Damiani. Nikolay Kositsin - Conversion only; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Author - Luis Damiani. Nikolay Kositsin - Conversion only', 'link': '', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 5, 4: 5}, 'colors': {1: [15570276], 2: [42495], 3: [16711935], 4: [65280]}, 'widths': {1: 1, 2: 1, 3: 4, 4: 4}, 'styles': {}, 'labels': {1: '3D Oscillator', 2: 'Signal line', 3: 'Sell', 4: 'Buy'}, 'levels': [], 'description': [], 'name': '3d_oscilator', 'source': 'MQL5 Indicators/3D_Oscilator/3d_oscilator.mq5', 'folder': '3D_Oscilator', 'inputs': [{'mql': 'D1RSIPer', 'py': 'D1RSIPer', 'param': 'D1RSIPer', 'type': 'int', 'default': 13, 'label': '', 'sinput': False}, {'mql': 'D2StochPer', 'py': 'D2StochPer', 'param': 'D2StochPer', 'type': 'int', 'default': 8, 'label': '', 'sinput': False}, {'mql': 'D3tunnelPer', 'py': 'D3tunnelPer', 'param': 'D3tunnelPer', 'type': 'int', 'default': 8, 'label': '', 'sinput': False}, {'mql': 'hot', 'py': 'hot', 'param': 'hot', 'type': 'double', 'default': 0.4, 'label': '', 'sinput': False}, {'mql': 'sigsmooth', 'py': 'sigsmooth', 'param': 'sigsmooth', 'type': 'int', 'default': 4, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
D1RSIPer = _input('D1RSIPer', 13)
D2StochPer = _input('D2StochPer', 8)
D3tunnelPer = _input('D3tunnelPer', 8)
hot = _input('hot', 0.4)
sigsmooth = _input('sigsmooth', 4)
BuyBuffer = Arr(0, 0.0)
SellBuffer = Arr(0, 0.0)
IndBuffer = Arr(0, 0.0)
SigBuffer = Arr(0, 0.0)
sk = 0.0
sk2 = 0.0
ss = 0
StartBars = 0
RSI_Handle = 0
CCI_Handle = 0

def OnInit():
    global CCI_Handle, RSI_Handle, StartBars, sk, sk2, ss
    ss = sigsmooth
    if ss < 2:
        ss = 2
    sk = _fdiv(2.0, ss + 1.0)
    sk2 = _fdiv(2.0, (ss * 0.8) + 1.0)
    StartBars = _int(D1RSIPer + D2StochPer + D2StochPer + hot + sigsmooth)
    RSI_Handle = iRSI(None, 0, D1RSIPer, PRICE_CLOSE)
    if RSI_Handle == INVALID_HANDLE:
        Print(' Failed to get the handle of the iRSI indicator')
    CCI_Handle = iCCI(None, 0, D3tunnelPer, PRICE_TYPICAL)
    if CCI_Handle == INVALID_HANDLE:
        Print(' Failed to get the handle of the iCCI indicator')
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetString(0, PLOT_LABEL, '3D Oscillator')
    ArraySetAsSeries(IndBuffer, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(1, SigBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetString(1, PLOT_LABEL, 'Signal line')
    ArraySetAsSeries(SigBuffer, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(2, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetString(2, PLOT_LABEL, 'Sell')
    PlotIndexSetInteger(2, PLOT_ARROW, 159)
    ArraySetAsSeries(SellBuffer, True)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(3, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetString(3, PLOT_LABEL, 'Signal line1Buy')
    PlotIndexSetInteger(3, PLOT_ARROW, 159)
    ArraySetAsSeries(BuyBuffer, True)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = '3D Oscillator'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (BarsCalculated(RSI_Handle) < rates_total or BarsCalculated(CCI_Handle) < rates_total) or rates_total < StartBars:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    rsi = 0.0
    maxrsi = 0.0
    minrsi = 0.0
    storsi = 0.0
    E3D = 0.0
    RSI = Arr(0, 0.0)
    CCI = Arr(0, 0.0)
    rangrsi = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        to_copy = rates_total
        limit = rates_total - StartBars - 1
    else:
        limit = rates_total - prev_calculated
        to_copy = limit + D2StochPer + 3
    ArraySetAsSeries(RSI, True)
    ArraySetAsSeries(CCI, True)
    if CopyBuffer(RSI_Handle, 0, 0, to_copy, RSI) <= 0:
        return 0
    if CopyBuffer(CCI_Handle, 0, 0, to_copy, CCI) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        rsi = RSI[bar]
        maxrsi = rsi
        minrsi = rsi
        for iii in range(bar + D2StochPer, bar - 1, -1):
            rsi = RSI[iii]
            if rsi > maxrsi:
                maxrsi = rsi
            if rsi < minrsi:
                minrsi = rsi
        rangrsi = maxrsi - minrsi
        if rangrsi == 0:
            storsi = 0.0
        else:
            storsi = _fdiv(rsi - minrsi, (maxrsi - minrsi) * 200) - 100
        E3D = (hot * CCI[bar]) + ((1.0 - hot) * storsi)
        IndBuffer[bar] = (sk * E3D) + ((1.0 - sk) * IndBuffer[bar + 1])
        SigBuffer[bar] = (sk2 * IndBuffer[bar + 1]) + ((1.0 - sk2) * SigBuffer[bar + 1])
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        if IndBuffer[bar] > SigBuffer[bar] and IndBuffer[bar + 1] < SigBuffer[bar + 1]:
            BuyBuffer[bar] = SigBuffer[bar] - 15
        if IndBuffer[bar] < SigBuffer[bar] and IndBuffer[bar + 1] > SigBuffer[bar + 1]:
            SellBuffer[bar] = SigBuffer[bar] + 15
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Ind3dOscilator(_MQL5Indicator):
    name = '3d_oscilator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'D1RSIPer': 13,
        'D2StochPer': 8,
        'D3tunnelPer': 8,
        'hot': 0.4,
        'sigsmooth': 4,
    }

