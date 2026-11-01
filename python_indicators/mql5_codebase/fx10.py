"""fx10 — converted from MQL5: MQL5 Indicators/Fx10/fx10.mq5

Copyright: Copyright © 2000-2007, palanka; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2000-2007, palanka', 'link': '', 'version': '1.01', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711935], 2: [65280]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'Fx10 Sell', 2: 'Fx10 Buy'}, 'levels': [], 'description': [], 'name': 'fx10', 'source': 'MQL5 Indicators/Fx10/fx10.mq5', 'folder': 'Fx10', 'inputs': [{'mql': 'ParmMult', 'py': 'ParmMult', 'param': 'ParmMult', 'type': 'double', 'default': 2.0, 'label': 'multiply the standard parameters by this scale factor', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ParmMult = _input('ParmMult', 2.0)  # multiply the standard parameters by this scale factor
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
min_rates_total = 0
MA5_Handle = 0
MA10_Handle = 0
RSI_Handle = 0
STO_Handle = 0
MACD_Handle = 0
ATR_Handle = 0

def OnInit():
    global ATR_Handle, MA10_Handle, MA5_Handle, MACD_Handle, RSI_Handle, STO_Handle, min_rates_total
    min_rates_total = _int((ParmMult * 26) + 1)
    MA5_Handle = iMA(None, 0, _int(ParmMult * 5), 0, MODE_LWMA, PRICE_CLOSE)
    if MA5_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iMA5 indicator')
    MA10_Handle = iMA(None, 0, _int(ParmMult * 10), 0, MODE_SMA, PRICE_CLOSE)
    if MA10_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iMA10 indicator')
    RSI_Handle = iRSI(None, 0, _int(ParmMult * 14), PRICE_CLOSE)
    if RSI_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iRSI indicator')
    STO_Handle = iStochastic(None, 0, _int(5 * ParmMult), _int(3 * ParmMult), _int(3 * ParmMult), MODE_SMA, STO_LOWHIGH)
    if STO_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iStochastic indicator')
    MACD_Handle = iMACD(None, 0, _int(12 * ParmMult), _int(26 * ParmMult), _int(9 * ParmMult), PRICE_CLOSE)
    if MACD_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iMACD indicator')
    ATR_Handle = iATR(None, 0, 15)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the ATR indicator')
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 119)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(SellBuffer, True)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 119)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(BuyBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'Fx10'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (((((BarsCalculated(MA5_Handle) < rates_total or BarsCalculated(MA10_Handle) < rates_total) or BarsCalculated(RSI_Handle) < rates_total) or BarsCalculated(STO_Handle) < rates_total) or BarsCalculated(MACD_Handle) < rates_total) or BarsCalculated(ATR_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    MA5 = Arr(0, 0.0)
    MA10 = Arr(0, 0.0)
    RSI = Arr(0, 0.0)
    STO = Arr(0, 0.0)
    MACD = Arr(0, 0.0)
    STOS = Arr(0, 0.0)
    MACDS = Arr(0, 0.0)
    ATR = Arr(0, 0.0)
    RsiUp = False
    RsiDn = False
    StochUp = False
    StochDn = False
    MacdUp = False
    MacdDn = False
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(MA5_Handle, 0, 0, to_copy, MA5) <= 0:
        return 0
    if CopyBuffer(MA10_Handle, 0, 0, to_copy, MA10) <= 0:
        return 0
    if CopyBuffer(RSI_Handle, 0, 0, to_copy, RSI) <= 0:
        return 0
    if CopyBuffer(STO_Handle, 0, 0, to_copy, STO) <= 0:
        return 0
    if CopyBuffer(STO_Handle, 1, 0, to_copy, STOS) <= 0:
        return 0
    if CopyBuffer(MACD_Handle, 0, 0, to_copy, MACD) <= 0:
        return 0
    if CopyBuffer(MACD_Handle, 1, 0, to_copy, MACDS) <= 0:
        return 0
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    ArraySetAsSeries(MA5, True)
    ArraySetAsSeries(MA10, True)
    ArraySetAsSeries(RSI, True)
    ArraySetAsSeries(STO, True)
    ArraySetAsSeries(STOS, True)
    ArraySetAsSeries(MACD, True)
    ArraySetAsSeries(MACDS, True)
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        if MA5[bar] > MA10[bar]:
            RsiUp = RSI[bar] >= 55.0
            StochUp = STO[bar] > STOS[bar]
            MacdUp = MACD[bar] > MACDS[bar]
            if (StochUp and RsiUp) and MacdUp:
                BuyBuffer[bar] = low[bar] - ((ATR[bar] * 3) / 8)
        if MA5[bar] < MA10[bar]:
            RsiDn = RSI[bar] <= 45.0
            StochDn = STO[bar] < STOS[bar]
            MacdDn = MACD[bar] < MACDS[bar]
            if (StochDn and RsiDn) and MacdDn:
                SellBuffer[bar] = high[bar] + ((ATR[bar] * 3) / 8)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Fx10(_MQL5Indicator):
    name = 'fx10'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ParmMult': 2.0,  # multiply the standard parameters by this scale factor
    }

