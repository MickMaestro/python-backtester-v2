"""divergence — converted from MQL5: MQL5 Indicators/Divergence/divergence.mq5

Divergence
Copyright: Copyright © 2005, Pavel Kulko; Link: polk@alba.dp.ua; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, Pavel Kulko', 'link': 'polk@alba.dp.ua', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 10, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [255, 16711935, 16711680, 65280]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Divergence Candles Open'}, 'levels': [], 'description': ['Divergence'], 'name': 'divergence', 'source': 'MQL5 Indicators/Divergence/divergence.mq5', 'folder': 'Divergence', 'inputs': [{'mql': 'ind', 'py': 'ind', 'param': 'ind', 'type': 'int', 'default': 0, 'label': 'indicator', 'sinput': False}, {'mql': 'pds', 'py': 'pds', 'param': 'pds', 'type': 'uint', 'default': 10, 'label': 'indicator periods', 'sinput': False}, {'mql': 'f', 'py': 'f', 'param': 'f', 'type': 'int', 'default': 0, 'label': 'price field', 'sinput': False}, {'mql': 'dCh', 'py': 'dCh', 'param': 'dCh', 'type': 'double', 'default': 0.0, 'label': 'peak/trough depth minimum (0-1)', 'sinput': False}, {'mql': 'xshift', 'py': 'xshift', 'param': 'xshift', 'type': 'uint', 'default': 0, 'label': 'shift signals back to match divergences', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum INDMODE
MODE_MACD = 0
MODE_RSI = 1
MODE_ADX = 2
MODE_Momentum = 3
_enum('INDMODE', {0: 'MODE_MACD', 1: 'MODE_RSI', 2: 'MODE_ADX', 3: 'MODE_Momentum'})

# enum PRICEMODE
MODE_CLOSE = 0
MODE_HIGHLOW = 1
_enum('PRICEMODE', {0: 'MODE_CLOSE', 1: 'MODE_HIGHLOW'})

# ---- inputs and global variables
ind = _input('ind', MODE_MACD)  # indicator
pds = _input('pds', 10)  # indicator periods
f = _input('f', MODE_CLOSE)  # price field
dCh = _input('dCh', 0.0)  # peak/trough depth minimum (0-1)
xshift = _input('xshift', 0)  # shift signals back to match divergences
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
R1 = Arr(0, 0.0)
R2 = Arr(0, 0.0)
y = Arr(0, 0.0)
xd = Arr(0, 0.0)
xu = Arr(0, 0.0)
Ch = 0.0
fCh = 0.0
min_rates_total = 0
Ind_Handle = 0

def OnInit():
    global Ch, Ind_Handle, fCh, min_rates_total
    min_rates_total = _int(pds)
    Ch = MathMax(MathMin(dCh, 1), 0)
    fCh = Ch / 100.0
    if ind != MODE_MACD:
        min_rates_total = _int(pds + 2)
    else:
        min_rates_total = 12 + 26 + 9 + 2
    _sw1 = ind
    if _sw1 == MODE_MACD:
        Ind_Handle = iMACD(None, 0, 12, 26, 9, PRICE_CLOSE)
        if Ind_Handle == INVALID_HANDLE:
            Print(' Failed to get handle of iMACD indicator')
    elif _sw1 == MODE_RSI:
        Ind_Handle = iRSI(None, 0, pds, PRICE_CLOSE)
        if Ind_Handle == INVALID_HANDLE:
            Print(' Failed to get handle of the iRSI indicator')
    elif _sw1 == MODE_ADX:
        Ind_Handle = iADX(None, 0, pds)
        if Ind_Handle == INVALID_HANDLE:
            Print(' Failed to get handle of the iADX indicator')
    elif _sw1 == MODE_Momentum:
        Ind_Handle = iMomentum(None, 0, pds, PRICE_CLOSE)
        if Ind_Handle == INVALID_HANDLE:
            Print(' Failed to get handle of the iMomentum indicator')
    SetIndexBuffer(0, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, R1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, R2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, y, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, xd, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, xu, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(ExtOpenBuffer, True)
    ArraySetAsSeries(ExtHighBuffer, True)
    ArraySetAsSeries(ExtLowBuffer, True)
    ArraySetAsSeries(ExtCloseBuffer, True)
    ArraySetAsSeries(ExtColorBuffer, True)
    ArraySetAsSeries(R1, True)
    ArraySetAsSeries(R2, True)
    ArraySetAsSeries(y, True)
    ArraySetAsSeries(xd, True)
    ArraySetAsSeries(xu, True)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'Divergence Candles'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(Ind_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    limit = 0
    to_copy = 0
    bar = 0
    CNmb1 = 0
    CNmb2 = 0
    CNmb3 = 0
    CNmb4 = 0
    Pkx1 = 0.0
    Pkx2 = 0.0
    Trx1 = 0.0
    Trx2 = 0.0
    Pky1 = 0.0
    Pky2 = 0.0
    Try1 = 0.0
    Try2 = 0.0
    Trx = False
    Pkx = False
    Try = False
    Pky = False
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1 - min_rates_total - 3
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(Ind_Handle, MAIN_LINE, 0, to_copy, y) <= 0:
        return 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(open, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if f == MODE_CLOSE:
            xu[bar] = close[bar]
            xd[bar] = close[bar]
        else:
            xu[bar] = high[bar]
            xd[bar] = low[bar]
        ExtOpenBuffer[bar] = 0.0
        ExtCloseBuffer[bar] = 0.0
        ExtHighBuffer[bar] = 0.0
        ExtLowBuffer[bar] = 0.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    bar = limit
    for bar in range(bar, 2 - 1, -1):
        CNmb1 = 0
        CNmb2 = 0
        CNmb3 = 0
        CNmb4 = 0
        for kkk in range(bar, rates_total):
            Pkx = (xu[kkk] < xu[kkk - 1] and xu[kkk - 1] > xu[kkk - 2]) and xu[kkk - 1] >= (((xu[kkk] + xu[kkk - 2]) / 2.0) * (1.0 + fCh))
            if Pkx:
                CNmb1 += 1
            if Pkx and CNmb1 == 1:
                Pkx1 = xu[kkk - 1]
            if Pkx and CNmb1 == 2:
                Pkx2 = xu[kkk - 1]
            Trx = (xd[kkk] > xd[kkk - 1] and xd[kkk - 1] < xd[kkk - 2]) and xd[kkk - 1] <= (((xd[kkk] + xd[kkk - 2]) / 2.0) * (1.0 - fCh))
            if Trx:
                CNmb2 += 1
            if Trx and CNmb2 == 1:
                Trx1 = xd[kkk - 1]
            if Trx and CNmb2 == 2:
                Trx2 = xd[kkk - 1]
            Pky = (y[kkk] < y[kkk - 1] and y[kkk - 1] > y[kkk - 2]) and y[kkk - 1] >= (((y[kkk] + y[kkk - 2]) / 2.0) * (1.0 + fCh))
            if Pky:
                CNmb3 += 1
            if Pky and CNmb3 == 1:
                Pky1 = y[kkk - 1]
            if Pky and CNmb3 == 2:
                Pky2 = y[kkk - 1]
            Try = (y[kkk] > y[kkk - 1] and y[kkk - 1] < y[kkk - 2]) and y[kkk - 1] <= (((y[kkk] + y[kkk - 2]) / 2.0) * (1.0 - fCh))
            if Try:
                CNmb4 += 1
            if Try and CNmb4 == 1:
                Try1 = y[kkk - 1]
            if Try and CNmb4 == 2:
                Try2 = y[kkk - 1]
            if ((CNmb1 >= 2 and CNmb2 >= 2) and CNmb3 >= 2) and CNmb4 >= 2:
                break
        Pkx = (xu[bar] < xu[bar - 1] and xu[bar - 1] > xu[bar - 2]) and xu[bar - 1] >= (((xu[bar] + xu[bar - 2]) / 2.0) * (1.0 + fCh))
        Trx = (xd[bar] > xd[bar - 1] and xd[bar - 1] < xd[bar - 2]) and xd[bar - 1] <= (((xd[bar] + xd[bar - 2]) / 2.0) * (1.0 - fCh))
        Pky = (y[bar] < y[bar - 1] and y[bar - 1] > y[bar - 2]) and y[bar - 1] >= (((y[bar] + y[bar - 2]) / 2.0) * (1.0 + fCh))
        Try = (y[bar] > y[bar - 1] and y[bar - 1] < y[bar - 2]) and y[bar - 1] <= (((y[bar] + y[bar - 2]) / 2.0) * (1.0 - fCh))
        R1[bar] = 0.0
        if ((Trx and Try) and Trx1 < Trx2) and Try1 > Try2:
            R1[bar] = 1.0
        R2[bar] = 0.0
        if ((Pkx and Pky) and Pkx1 > Pkx2) and Pky1 < Pky2:
            R2[bar] = 1.0
        if (R1[bar] - R2[bar]) > 0:
            ExtOpenBuffer[bar] = open[bar]
            ExtCloseBuffer[bar] = close[bar]
            ExtHighBuffer[bar] = high[bar]
            ExtLowBuffer[bar] = low[bar]
            if close[bar] > open[bar]:
                ExtColorBuffer[bar] = 3.0
            else:
                ExtColorBuffer[bar] = 2.0
        if (R1[bar] - R2[bar]) < 0:
            ExtOpenBuffer[bar] = open[bar]
            ExtCloseBuffer[bar] = close[bar]
            ExtHighBuffer[bar] = high[bar]
            ExtLowBuffer[bar] = low[bar]
            if open[bar] > close[bar]:
                ExtColorBuffer[bar] = 0.0
            else:
                ExtColorBuffer[bar] = 1.0
    else:
        bar = _range_end(bar, 2 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Divergence(_MQL5Indicator):
    name = 'divergence'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ind': _Choice({0: 'MACD', 1: 'RSI', 2: 'ADX', 3: 'Momentum'}, default=0),  # indicator
        'pds': 10,  # indicator periods
        'f': _Choice({0: 'Close', 1: 'High/Low'}, default=0),  # price field
        'dCh': 0.0,  # peak/trough depth minimum (0-1)
        'xshift': 0,  # shift signals back to match divergences
        'Shift': 0,  # horizontal shift of the indicator in bars
    }

